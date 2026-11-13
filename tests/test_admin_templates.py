from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
from mako.lookup import TemplateLookup

from mahnil.cms.admin import (
    FIELD_DEFINITIONS,
    SECTION_TO_KIND,
    _field_groups,
    _fields_for,
)


TEMPLATE_DIRECTORY = (
    Path(__file__).parents[1] / 'mahnil' / 'templates'
)
LOOKUP = TemplateLookup(directories=[str(TEMPLATE_DIRECTORY)])
ASSET_OPTIONS = {
    'images': [
        {'value': 'image-asset-id', 'label': 'cover.jpg · 12 KB'},
    ],
    'files': [
        {'value': 'file-asset-id', 'label': 'guide.pdf · 18 KB'},
    ],
}


def _field_data(kind):
    values = {}
    for name, _, type_, _ in FIELD_DEFINITIONS[kind]:
        if type_ in {'checkbox', 'cover_decorative'}:
            values[name] = False
        elif type_ == 'multi_image_asset':
            values[name] = ['image-asset-id']
        else:
            values[name] = f'{name} value'
    if kind == 'home':
        values['headline'] = '<script>Keep this escaped</script>'
        values['hero_visual_asset_id'] = 'image-asset-id'
    if kind == 'service':
        values['icon'] = 'strategy'
    if kind == 'portfolio':
        values.update(project_type='concept', cover_asset_id='image-asset-id')
    if kind == 'resource':
        values.update(
            format='PDF',
            availability='coming_soon',
            cover_asset_id='image-asset-id',
            file_asset_id='file-asset-id',
        )
    if kind == 'settings':
        values['logo_asset_id'] = 'image-asset-id'
    return values


def _render_editor(section):
    kind = SECTION_TO_KIND[section]
    data = _field_data(kind)
    fields = _fields_for(kind, data, ASSET_OPTIONS)
    entry = {
        'id': f'{kind}-record-id',
        'title': data.get('title', data.get('agency_name', 'Homepage entry')),
        'status': 'Draft changes',
        'archived': False,
        'display_order': 0,
        'draft_visible': True,
        'updated_at': datetime(2026, 11, 7, tzinfo=timezone.utc),
        'published_at': datetime(2026, 11, 7, tzinfo=timezone.utc),
        'fields': fields,
        'field_groups': _field_groups(kind, fields),
    }
    create_fields = (
        _fields_for(kind, {}, ASSET_OPTIONS)
        if kind in {'service', 'portfolio', 'resource'}
        else []
    )
    return LOOKUP.get_template('admin_editor.mako').render(
        settings=SimpleNamespace(env='production'),
        asseturl=lambda path: f'/assets/{path}',
        agency_name='Example Agency',
        show_navigation=True,
        csrf='csrf-token',
        page_title=section.title(),
        description=f'Edit {section}.',
        error=None,
        notice=None,
        is_collection=kind in {'service', 'portfolio', 'resource'},
        section=section,
        entries=[entry],
        create_fields=create_fields,
        create_field_groups=_field_groups(kind, create_fields),
    )


@pytest.mark.parametrize(
    'section', ('home', 'services', 'portfolio', 'resources', 'settings'),
)
def test_admin_editor_sections_render_fields_through_mako_include(section):
    rendered = _render_editor(section)

    assert f'<form action="/admin/{section}"' in rendered
    assert 'name="csrf" value="csrf-token"' in rendered
    assert 'name="action" value="save_draft"' in rendered
    assert 'name="action" value="publish"' in rendered
    assert '<fieldset' in rendered
    assert 'id="' in rendered


def test_admin_editor_include_preserves_field_escaping_and_controls():
    rendered = _render_editor('home')

    assert '&lt;script&gt;Keep this escaped&lt;/script&gt;' in rendered
    assert '<script>Keep this escaped</script>' not in rendered
    assert 'name="headline"' in rendered
    assert 'name="hero_description"' in rendered


def test_home_editor_renders_the_hero_visual_media_control():
    rendered = _render_editor('home')

    assert 'Hero visual' in rendered
    assert 'name="hero_visual_asset_id" value="image-asset-id"' in rendered
    assert 'data-current-filename="cover.jpg · 12 KB"' in rendered
    assert 'name="hero_visual_alt"' in rendered
    assert 'name="hero_visual_decorative"' in rendered
    assert 'Choose from Media Library' in rendered
    assert 'Upload new image' in rendered
    assert 'Remove image' in rendered


def test_image_fields_render_library_upload_remove_and_accessible_picker_controls():
    rendered = _render_editor('portfolio')

    assert 'name="cover_asset_id" value="image-asset-id"' in rendered
    assert 'data-current-filename="cover.jpg · 12 KB"' in rendered
    assert 'Choose from Media Library' in rendered
    assert 'Upload new image' in rendered
    assert 'Remove from this section' in rendered
    assert 'aria-labelledby="portfolio-record-id-cover_asset_id-picker-title"' in rendered
    assert 'name="csrf" value="csrf-token"' in rendered
    assert 'type="text" id="portfolio-record-id-cover_asset_id"' not in rendered


def test_other_admin_templates_render_with_representative_contexts():
    common = {
        'settings': SimpleNamespace(env='production'),
        'asseturl': lambda path: f'/assets/{path}',
        'agency_name': 'Example Agency',
        'show_navigation': True,
        'csrf': 'csrf-token',
    }
    templates = {
        'admin_dashboard.mako': {
            **common,
            'sections': [{
                'section': 'home',
                'title': 'Homepage',
                'count': 1,
                'published': 1,
                'drafts': 0,
            }],
        },
        'admin_login.mako': {
            **common,
            'show_navigation': False,
            'configured': True,
            'error': None,
        },
        'admin_media.mako': {
            **common,
            'error': None,
            'notice': None,
            'max_upload_mb': 10,
            'search': '',
            'page': 1,
            'has_previous': False,
            'has_next': False,
            'result_count': 1,
            'assets': [{
                'id': 'image-asset-id',
                'filename': 'cover.jpg',
                'mime_type': 'image/jpeg',
                'size': 12000,
                'width': 640,
                'height': 400,
                'alt_text': 'A cover image',
                'decorative': False,
                'used': False,
            }],
        },
    }

    for name, context in templates.items():
        rendered = LOOKUP.get_template(name).render(**context)
        assert '<!doctype html>' in rendered
        if name != 'admin_login.mako':
            assert 'name="csrf" value="csrf-token"' in rendered
        if name == 'admin_media.mako':
            assert 'Upload image or file' in rendered
            assert '30 megapixels' in rendered
