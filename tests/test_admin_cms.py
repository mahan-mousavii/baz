import json
from io import BytesIO

import pytest
from PIL import Image
from sqlalchemy import select
from yhttp.ext.auth import AccessToken

from bddrest import response, status

from mahnil.cms.admin import FIELD_DEFINITIONS
from mahnil.cms.content import seed_records
from mahnil.common.models import CMSRecord, MediaAsset


def use_production(app, monkeypatch):
    monkeypatch.setattr(app.settings, 'env', 'production')


def admin_authorization(app, *, csrf='csrf-test'):
    token = app.auth.token_dumps(
        AccessToken(id='cms-test-session', roles=['admin'], csrf=csrf)
    )
    return f'Bearer {token}'


def test_admin_pages_and_writes_redirect_when_unauthenticated(
    httpreq,
    app,
    monkeypatch,
):
    use_production(app, monkeypatch)

    with httpreq('/admin/home'):
        assert status == 302
        assert response.headers['location'] == '/admin/login'

    with httpreq(
        '/admin/home',
        verb='POST',
        form={'csrf': 'missing', 'action': 'publish'},
    ):
        assert status == 302
        assert response.headers['location'] == '/admin/login'


def test_admin_login_requires_configured_credentials_and_creates_a_session(
    httpreq,
    app,
    monkeypatch,
):
    use_production(app, monkeypatch)
    monkeypatch.setenv('YHTTP_ADMIN_USERNAME', 'studio-owner')
    monkeypatch.setenv('YHTTP_ADMIN_PASSWORD', 'a-long-test-only-password')

    with httpreq(
        '/admin/login',
        verb='POST',
        form={
            'username': 'studio-owner',
            'password': 'a-long-test-only-password',
        },
    ):
        assert status == 303
        assert response.headers['location'] == '/admin'
        assert response.cookies['yhttp-accesstoken']


def test_admin_login_limits_repeated_failures(httpreq, app, monkeypatch):
    use_production(app, monkeypatch)
    monkeypatch.setenv('YHTTP_ADMIN_USERNAME', 'studio-owner')
    monkeypatch.setenv('YHTTP_ADMIN_PASSWORD', 'a-long-test-only-password')

    for _ in range(5):
        with httpreq(
            '/admin/login',
            verb='POST',
            form={'username': 'studio-owner', 'password': 'wrong-password'},
        ):
            assert status == 401

    with httpreq(
        '/admin/login',
        verb='POST',
        form={
            'username': 'studio-owner',
            'password': 'a-long-test-only-password',
        },
    ):
        assert status == 429


def test_admin_mutations_require_a_valid_csrf_value(httpreq, app, monkeypatch):
    use_production(app, monkeypatch)
    monkeypatch.setattr(app.auth, 'blacklist_has', lambda _: False)

    with httpreq(
        '/admin/home',
        verb='POST',
        authorization=admin_authorization(app),
        form={'csrf': 'wrong', 'action': 'publish'},
    ):
        assert status == 403


def test_saving_a_draft_keeps_the_published_homepage_unchanged(
    httpreq,
    app,
    monkeypatch,
):
    use_production(app, monkeypatch)
    monkeypatch.setattr(app.auth, 'blacklist_has', lambda _: False)
    session = app.db.session()
    with session.begin():
        seed_records(session)
        home = session.scalar(
            select(CMSRecord).where(CMSRecord.kind == 'home')
        )
        record_id = home.id
        form = dict(home.draft_data)
        old_published = home.published_data['hero_description']

    form.update({
        'csrf': 'csrf-test',
        'record_id': record_id,
        'action': 'save_draft',
        'visible': 'yes',
        'display_order': '0',
        'hero_description': 'A saved but unpublished edit.',
    })
    with httpreq(
        '/admin/home',
        verb='POST',
        authorization=admin_authorization(app),
        form=form,
    ):
        assert status == 303
        assert response.headers['location'] == '/admin/home?status=saved'

    with app.db.session() as session:
        home = session.get(CMSRecord, record_id)
        assert home.draft_data['hero_description'] == 'A saved but unpublished edit.'
        assert home.published_data['hero_description'] == old_published

    with httpreq('/'):
        assert old_published in response.text
        assert 'A saved but unpublished edit.' not in response.text


def test_media_picker_search_is_authenticated_and_returns_bounded_image_metadata(
    httpreq,
    app,
    monkeypatch,
):
    use_production(app, monkeypatch)
    monkeypatch.setattr(app.auth, 'blacklist_has', lambda _: False)
    asset_id = '8b0b0f67-0b5a-4c86-9271-4e198971e42f'
    asset = MediaAsset(
        id=asset_id,
        storage_key=asset_id,
        original_filename='cover-search.png',
        mime_type='image/png',
        file_size=120,
        width=640,
        height=400,
        alt_text='Cover',
        decorative=False,
    )
    session = app.db.session()
    with session.begin():
        session.add(asset)

    with httpreq('/admin/media/library?search=cover'):
        assert status == 302
        assert response.headers['location'] == '/admin/login'

    with httpreq(
        '/admin/media/library?search=cover&page=1',
        authorization=admin_authorization(app),
    ):
        assert status == 200
        payload = json.loads(response.text)
        assert payload['page'] == 1
        assert payload['has_more'] is False
        assert [item['filename'] for item in payload['items']] == ['cover-search.png']
        assert payload['items'][0]['preview_url'].endswith(f'/{asset_id}/preview')

    with httpreq(f'/admin/media/{asset_id}/preview'):
        assert status == 302
        assert response.headers['location'] == '/admin/login'

    with httpreq(f'/media/{asset_id}'):
        assert status == 404


@pytest.mark.parametrize('csrf', (None, 'invalid-picker-token'))
def test_editor_image_upload_requires_session_csrf(httpreq, app, monkeypatch, csrf):
    use_production(app, monkeypatch)
    monkeypatch.setattr(app.auth, 'blacklist_has', lambda _: False)
    form = {'action': 'upload'}
    if csrf:
        form['csrf'] = csrf

    with httpreq(
        '/admin/media?picker=1',
        verb='POST',
        authorization=admin_authorization(app),
        form=form,
    ):
        assert status == (400 if csrf is None else 403)


def test_editor_upload_validates_and_persists_image_in_media_library(
    httpreq,
    app,
    monkeypatch,
):
    use_production(app, monkeypatch)
    monkeypatch.setattr(app.auth, 'blacklist_has', lambda _: False)
    image = BytesIO()
    image.name = 'editor-upload.png'
    Image.new('RGB', (2, 2), color=(30, 111, 121)).save(image, format='PNG')
    image.seek(0)

    with httpreq(
        '/admin/media?picker=1',
        verb='POST',
        authorization=admin_authorization(app),
        multipart={
            'csrf': 'csrf-test',
            'action': 'upload',
            'upload': image,
        },
    ):
        assert status == 201
        payload = json.loads(response.text)
        assert payload['item']['filename'] == 'editor-upload.png'
        assert payload['item']['preview_url'].endswith('/preview')
        asset_id = payload['item']['id']

    with app.db.session() as session:
        asset = session.get(MediaAsset, asset_id)
        assert asset is not None
        assert asset.mime_type == 'image/png'
        assert asset.width == 2 and asset.height == 2


def test_image_draft_is_private_until_the_editor_publishes_it(
    httpreq,
    app,
    monkeypatch,
):
    use_production(app, monkeypatch)
    monkeypatch.setattr(app.auth, 'blacklist_has', lambda _: False)
    session = app.db.session()
    with session.begin():
        seed_records(session)
        portfolio = session.scalar(
            select(CMSRecord).where(CMSRecord.kind == 'portfolio')
        )
        old_published_id = portfolio.published_data.get('cover_asset_id', '')
        asset_id = '8b0b0f67-0b5a-4c86-9271-4e198971e42f'
        session.add(MediaAsset(
            id=asset_id,
            storage_key=asset_id,
            original_filename='new-cover.png',
            mime_type='image/png',
            file_size=120,
            width=640,
            height=400,
            alt_text='New cover',
            decorative=False,
        ))
        record_id = portfolio.id
        form = {
            name: portfolio.draft_data[name]
            for name, _, _, _ in FIELD_DEFINITIONS['portfolio']
            if name in portfolio.draft_data and name != 'additional_asset_ids'
        }

    form.update({
        'csrf': 'csrf-test',
        'record_id': record_id,
        'action': 'save_draft',
        'visible': 'yes',
        'display_order': '0',
        'cover_asset_id': asset_id,
    })
    with httpreq(
        '/admin/portfolio',
        verb='POST',
        authorization=admin_authorization(app),
        form=form,
    ):
        assert status == 303
        assert response.headers['location'] == '/admin/portfolio?status=saved'
    with app.db.session() as session:
        portfolio = session.get(CMSRecord, record_id)
        assert portfolio.draft_data['cover_asset_id'] == asset_id
        assert portfolio.published_data.get('cover_asset_id', '') == old_published_id

    with httpreq(
        '/admin/portfolio',
        authorization=admin_authorization(app),
    ):
        assert status == 200
        assert f'name="cover_asset_id" value="{asset_id}"' in response.text

    form['action'] = 'publish'
    with httpreq(
        '/admin/portfolio',
        verb='POST',
        authorization=admin_authorization(app),
        form=form,
    ):
        assert status == 303
        assert response.headers['location'] == '/admin/portfolio?status=published'
    with app.db.session() as session:
        portfolio = session.get(CMSRecord, record_id)
        assert portfolio.published_data['cover_asset_id'] == asset_id

    form.update(action='save_draft', cover_asset_id='')
    with httpreq(
        '/admin/portfolio',
        verb='POST',
        authorization=admin_authorization(app),
        form=form,
    ):
        assert status == 303
        assert response.headers['location'] == '/admin/portfolio?status=saved'
    with app.db.session() as session:
        portfolio = session.get(CMSRecord, record_id)
        assert portfolio.draft_data['cover_asset_id'] == ''
        assert portfolio.published_data['cover_asset_id'] == asset_id
        assert session.get(MediaAsset, asset_id) is not None
