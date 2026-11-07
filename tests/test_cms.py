from io import BytesIO
from types import SimpleNamespace

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from yhttp_ssr_boilerplate.cms.content import (
    publish_record,
    public_homepage,
    record_status,
    seed_records,
    validate_content,
)
from yhttp_ssr_boilerplate.cms.storage import MediaStorage
from yhttp_ssr_boilerplate.cms.uploads import InvalidUpload, inspect_upload
from yhttp_ssr_boilerplate.common.models import BaseModel, CMSRecord, MediaAsset


@pytest.fixture
def cms_session():
    engine = create_engine('sqlite:///:memory:')
    BaseModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


def test_seed_is_idempotent_and_keeps_admin_edits(cms_session):
    with cms_session.begin():
        assert seed_records(cms_session) == 11
        home = cms_session.scalar(
            select(CMSRecord).where(CMSRecord.kind == 'home')
        )
        home.draft_data = dict(home.draft_data, hero_description='Owner edit')

    with cms_session.begin():
        assert seed_records(cms_session) == 0
        home = cms_session.scalar(
            select(CMSRecord).where(CMSRecord.kind == 'home')
        )
        assert home.draft_data['hero_description'] == 'Owner edit'


def test_homepage_uses_published_snapshot_until_publish(cms_session):
    with cms_session.begin():
        seed_records(cms_session)
        home = cms_session.scalar(
            select(CMSRecord).where(CMSRecord.kind == 'home')
        )
        published_description = home.published_data['hero_description']
        home.draft_data = dict(home.draft_data, hero_description='Draft only')
        assert record_status(home) == 'Draft changes'

    assert public_homepage(cms_session)['home']['hero_description'] == published_description
    cms_session.rollback()

    with cms_session.begin():
        home = cms_session.scalar(
            select(CMSRecord).where(CMSRecord.kind == 'home')
        )
        publish_record(home)
        assert record_status(home) == 'Published'

    assert public_homepage(cms_session)['home']['hero_description'] == 'Draft only'


def test_unpublished_and_hidden_records_do_not_reach_public_homepage(cms_session):
    with cms_session.begin():
        seed_records(cms_session)
        service = cms_session.scalar(
            select(CMSRecord).where(CMSRecord.kind == 'service')
        )
        service.draft_data = dict(service.draft_data, title='Draft title')
        service.published_visible = False

    page = public_homepage(cms_session)
    assert len(page['services']) == 3
    assert all(service['title'] != 'Draft title' for service in page['services'])


def test_publishing_a_hidden_home_does_not_restore_hardcoded_copy(cms_session):
    with cms_session.begin():
        seed_records(cms_session)
        home = cms_session.scalar(
            select(CMSRecord).where(CMSRecord.kind == 'home')
        )
        home.published_visible = False

    page = public_homepage(cms_session)
    assert page['home']['hero_description'] == ''


def test_upload_validation_uses_file_contents_and_limits(cms_session):
    pdf = SimpleNamespace(filename='guide.pdf', file=BytesIO(b'%PDF-1.7\ncontent'))
    inspected = inspect_upload(pdf)
    assert inspected['mime_type'] == 'application/pdf'
    assert inspected['extension'] == '.pdf'

    executable = SimpleNamespace(filename='payload.exe', file=BytesIO(b'MZ'))
    with pytest.raises(InvalidUpload, match='Allowed files'):
        inspect_upload(executable)

    mislabeled = SimpleNamespace(filename='payload.pdf', file=BytesIO(b'MZ'))
    with pytest.raises(InvalidUpload, match='valid PDF'):
        inspect_upload(mislabeled)

    large_pdf = SimpleNamespace(
        filename='large.pdf',
        file=BytesIO(b'%PDF-' + (b'a' * (10 * 1024 * 1024))),
    )
    with pytest.raises(InvalidUpload, match='10 MB'):
        inspect_upload(large_pdf)


def test_local_media_storage_keeps_keys_confined_to_private_directory(tmp_path):
    storage = MediaStorage('local', tmp_path / 'private')
    key = '8b0b0f67-0b5a-4c86-9271-4e198971e42f'
    storage.put(key, b'%PDF-data', 'application/pdf')
    assert storage.get(key) == b'%PDF-data'
    storage.delete(key)
    assert not (tmp_path / 'private' / key).exists()

    with pytest.raises(ValueError, match='Invalid storage key'):
        storage.get('../private')


def test_content_validation_rejects_unsafe_destinations_and_icons(cms_session):
    home = {
        'eyebrow': 'Agency · Oman',
        'headline': 'Clear strategy.\nDistinctive content.',
        'hero_description': 'A description.',
        'primary_cta_label': 'Explore services',
        'primary_cta_href': 'javascript:alert(1)',
        'secondary_cta_label': 'Explore tools',
        'secondary_cta_href': '#free-tools',
        'services_heading': 'Services',
        'services_intro': 'Intro',
        'portfolio_heading': 'Work',
        'portfolio_intro': 'Intro',
        'resources_heading': 'Tools',
        'resources_intro': 'Intro',
        'about_heading': 'About',
        'about_description': 'Description',
        'contact_heading': 'Contact',
        'contact_description': 'Description',
    }
    with pytest.raises(ValueError, match='destination'):
        validate_content('home', home, cms_session)

    with pytest.raises(ValueError, match='icon'):
        validate_content('service', {
            'slug': 'safe-service',
            'title': 'Safe service',
            'subtitle': 'Subtitle',
            'description': 'Description',
            'icon': '<script>',
        }, cms_session)


def test_image_reference_and_default_alt_are_kept_in_the_database(cms_session):
    asset = MediaAsset(
        id='8b0b0f67-0b5a-4c86-9271-4e198971e42f',
        storage_key='8b0b0f67-0b5a-4c86-9271-4e198971e42f',
        original_filename='hero.png',
        mime_type='image/png',
        file_size=120,
        width=640,
        height=400,
        alt_text='A sample brand image',
        decorative=False,
    )
    cms_session.add(asset)
    cms_session.commit()
    assert cms_session.get(MediaAsset, asset.id).alt_text == 'A sample brand image'
