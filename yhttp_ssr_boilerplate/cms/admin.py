"""Protected CMS pages and writes for the single site administrator."""

from datetime import datetime, timedelta, timezone
from functools import wraps
import hmac
import os
import re
import secrets
import uuid
from urllib.parse import quote

from sqlalchemy import select
from yhttp.core import guard, statuses
from yhttp.ext.auth import AccessToken

from ..common.models import AdminAuthState, CMSRecord, MediaAsset
from ..manifest import __appname__
from .content import (
    ICONS,
    KINDS,
    publish_record,
    record_status,
    referenced_asset_ids,
    validate_content,
)
from .uploads import InvalidUpload, inspect_upload
from ..rollup import app


SECTION_TO_KIND = {
    'home': 'home',
    'services': 'service',
    'portfolio': 'portfolio',
    'resources': 'resource',
    'settings': 'settings',
}
SECTION_TEXT = {
    'home': ('Homepage', 'Edit the homepage copy shown in the existing sections.'),
    'services': ('Services', 'Edit, order, archive, and publish the homepage services.'),
    'portfolio': ('Portfolio', 'Manage the two selected-work preview slots shown on the homepage.'),
    'resources': ('Free resources', 'Manage the homepage resource previews and their availability.'),
    'settings': ('General settings', 'Update the agency identity and real contact destinations.'),
}
FIELD_DEFINITIONS = {
    'home': (
        ('eyebrow', 'Hero eyebrow', 'text', 120),
        ('headline', 'Hero headline', 'textarea', 180),
        ('hero_description', 'Hero description', 'textarea', 500),
        ('primary_cta_label', 'Primary button label', 'text', 80),
        ('primary_cta_href', 'Primary button destination', 'text', 500),
        ('secondary_cta_label', 'Secondary button label', 'text', 80),
        ('secondary_cta_href', 'Secondary button destination', 'text', 500),
        ('services_heading', 'Services heading', 'text', 180),
        ('services_intro', 'Services introduction', 'textarea', 500),
        ('portfolio_heading', 'Portfolio heading', 'text', 180),
        ('portfolio_intro', 'Portfolio introduction', 'textarea', 500),
        ('resources_heading', 'Free resources heading', 'text', 180),
        ('resources_intro', 'Free resources introduction', 'textarea', 500),
        ('about_heading', 'About heading', 'text', 180),
        ('about_description', 'About description', 'textarea', 700),
        ('contact_heading', 'Contact heading', 'text', 180),
        ('contact_description', 'Contact introduction', 'textarea', 500),
    ),
    'settings': (
        ('agency_name', 'Agency name', 'text', 100),
        ('logo_asset_id', 'Logo image', 'image_asset', 36),
        ('description', 'Short agency description', 'textarea', 300),
        ('business_email', 'Business email', 'text', 254),
        ('whatsapp_url', 'WhatsApp destination', 'text', 500),
        ('instagram_url', 'Instagram URL', 'text', 500),
        ('linkedin_url', 'LinkedIn URL', 'text', 500),
        ('footer_text', 'Footer text', 'textarea', 300),
    ),
    'service': (
        ('slug', 'URL slug', 'text', 120),
        ('title', 'Title', 'text', 160),
        ('subtitle', 'Subtitle', 'text', 160),
        ('description', 'Description', 'textarea', 700),
        ('icon', 'Icon', 'icon', 32),
    ),
    'portfolio': (
        ('slug', 'URL slug', 'text', 120),
        ('title', 'Title', 'text', 160),
        ('description', 'Short description', 'textarea', 700),
        ('category', 'Category or service type', 'text', 100),
        ('project_type', 'Project type', 'project_type', 20),
        ('cover_asset_id', 'Cover image', 'image_asset', 36),
        ('cover_alt', 'Cover image alt text', 'text', 300),
        ('cover_decorative', 'Cover image is decorative', 'checkbox', 5),
        ('additional_asset_ids', 'Additional images', 'multi_image_asset', 36),
        ('featured', 'Featured', 'checkbox', 5),
    ),
    'resource': (
        ('slug', 'URL slug', 'text', 120),
        ('title', 'Title', 'text', 160),
        ('description', 'Short description', 'textarea', 700),
        ('category', 'Category', 'text', 100),
        ('format', 'Resource format', 'resource_format', 10),
        ('availability', 'Availability', 'availability', 20),
        ('cover_asset_id', 'Cover image', 'image_asset', 36),
        ('cover_alt', 'Cover image alt text', 'text', 300),
        ('cover_decorative', 'Cover image is decorative', 'checkbox', 5),
        ('file_asset_id', 'Download file', 'file_asset', 36),
        ('external_url', 'External resource URL', 'text', 500),
    ),
}
FORM_NAMES = {
    'csrf', 'action', 'record_id', 'display_order', 'visible', 'confirm_delete',
    'eyebrow', 'headline', 'hero_description', 'primary_cta_label',
    'primary_cta_href', 'secondary_cta_label', 'secondary_cta_href',
    'services_heading', 'services_intro', 'portfolio_heading', 'portfolio_intro',
    'resources_heading', 'resources_intro', 'about_heading', 'about_description',
    'contact_heading', 'contact_description', 'agency_name', 'logo_asset_id',
    'business_email', 'whatsapp_url', 'instagram_url', 'linkedin_url', 'footer_text',
    'slug', 'title', 'subtitle', 'description', 'icon', 'category', 'project_type',
    'cover_asset_id', 'cover_alt', 'cover_decorative', 'additional_asset_ids', 'featured', 'format',
    'availability', 'file_asset_id', 'external_url', 'default_alt', 'decorative', 'upload',
}
EDITOR_GUARDS = tuple(
    guard.String(name, optional=True)
    for name in sorted(FORM_NAMES - {'upload'})
)
EDITOR_GUARDS += (guard.File('upload', optional=True),)
LOGIN_FIELDS = (
    guard.String('username', length=(1, 128)),
    guard.String('password', length=(1, 1024)),
)
MEDIA_FIELDS = (
    guard.String('csrf', length=(1, 1024)),
    guard.String('action', length=(1, 20)),
    guard.String('default_alt', length=(0, 300), optional=True),
    guard.String('decorative', length=(0, 5), optional=True),
    guard.String('confirm_delete', length=(1, 5), optional=True),
    guard.File('upload', optional=True),
)
FORM_MAP = {name: name for name in FORM_NAMES}


def redirect(location):
    raise statuses.HTTP3xx(
        303,
        headers=[('Location', location)],
        keepheaders=True,
    )


def admin_required(handler):
    authenticated = app.auth(
        roles='admin',
        unauthorized=lambda req: statuses.found('/admin/login'),
    )(handler)

    @wraps(handler)
    def wrapped(req, *args, **kwargs):
        req.response.headers['cache-control'] = 'no-store'
        req.response.headers['x-robots-tag'] = 'noindex, nofollow, noarchive'
        return authenticated(req, *args, **kwargs)

    return wrapped


def csrf_value(req):
    return getattr(req.identity, 'csrf', '') or ''


def verify_csrf(req):
    submitted = req.form.get('csrf', '')
    expected = csrf_value(req)
    if not expected or not hmac.compare_digest(str(submitted), str(expected)):
        raise statuses.forbidden(message='Your session token is missing or expired. Reload and try again.')


def _set_status(req, status):
    req.response.status = status


def _configured_credentials():
    username = os.environ.get('YHTTP_ADMIN_USERNAME', '')
    password = os.environ.get('YHTTP_ADMIN_PASSWORD', '')
    if not username or not password:
        return None
    return username, password


def _login_state(session, now):
    state = session.get(AdminAuthState, 1, with_for_update=True)
    if state is None:
        state = AdminAuthState(id=1, failures=0)
        session.add(state)
        session.flush()
    return state


def _auth_limited(session, now):
    state = _login_state(session, now)
    return state.locked_until is not None and state.locked_until > now


def _record_login_result(session, now, success):
    state = _login_state(session, now)
    if success:
        state.failures = 0
        state.window_started_at = None
        state.locked_until = None
        return False
    if state.window_started_at is None or state.window_started_at < now - timedelta(minutes=15):
        state.window_started_at = now
        state.failures = 0
    state.failures += 1
    if state.failures >= 5:
        state.failures = 0
        state.window_started_at = None
        state.locked_until = now + timedelta(minutes=15)
        return True
    return False


@app.route(r'/admin/login')
@app.bodyguard(strict=True)
@app.queryguard(strict=True)
@app.template('admin_login.mako')
def get(req):
    req.response.headers['cache-control'] = 'no-store'
    req.response.headers['x-robots-tag'] = 'noindex, nofollow, noarchive'
    if req.identity and req.identity.authorize('admin'):
        redirect('/admin')
    return {
        'configured': bool(_configured_credentials()),
        'error': None,
        'show_navigation': False,
        'agency_name': '[Agency Name]',
    }


@app.route(r'/admin/login', verb='post')
@app.bodyguard(fields=LOGIN_FIELDS, strict=True)
@app.queryguard(strict=True)
@app.template('admin_login.mako')
def create(req):
    req.response.headers['cache-control'] = 'no-store'
    req.response.headers['x-robots-tag'] = 'noindex, nofollow, noarchive'
    credentials = _configured_credentials()
    if credentials is None:
        _set_status(req, '503 Service Unavailable')
        return {
            'configured': False,
            'error': 'Admin access has not been configured.',
            'show_navigation': False,
        }

    now = datetime.now(timezone.utc)
    username, password = req.form['username'], req.form['password']
    expected_username, expected_password = credentials
    session = app.db.session()
    with session.begin():
        if _auth_limited(session, now):
            limited = True
            valid = False
        else:
            limited = False
            username_valid = hmac.compare_digest(username, expected_username)
            password_valid = hmac.compare_digest(password, expected_password)
            valid = username_valid and password_valid
            _record_login_result(session, now, valid)

    if limited:
        _set_status(req, '429 Too Many Requests')
        return {
            'configured': True,
            'error': 'Too many sign-in attempts. Wait 15 minutes and try again.',
            'show_navigation': False,
        }
    if not valid:
        _set_status(req, '401 Unauthorized')
        return {
            'configured': True,
            'error': 'The username or password is incorrect.',
            'show_navigation': False,
        }

    app.auth.session_new(
        req,
        AccessToken(
            id=str(uuid.uuid4()),
            roles=['admin'],
            username=expected_username,
            csrf=secrets.token_urlsafe(32),
        ),
    )
    redirect('/admin')


@app.route(r'/admin/logout', verb='post')
@admin_required
@app.bodyguard(fields=(guard.String('csrf', length=(1, 1024)),), strict=True)
@app.queryguard(strict=True)
def create(req):
    verify_csrf(req)
    # Each login receives its own random token ID, so yhttp-auth can revoke only
    # this session through its blacklist rather than every admin session.
    app.auth.blacklist_add(req.identity.id)
    app.auth.session_delete(req)
    redirect('/admin/login')


@app.route(r'/admin')
@admin_required
@app.bodyguard(strict=True)
@app.queryguard(strict=True)
@app.template('admin_dashboard.mako')
def get(req):
    with app.db.session() as session:
        records = session.scalars(select(CMSRecord)).all()
    summaries = []
    for section, kind in SECTION_TO_KIND.items():
        items = [record for record in records if record.kind == kind]
        summaries.append({
            'section': section,
            'title': SECTION_TEXT[section][0],
            'count': len(items),
            'drafts': sum(
                1 for item in items
                if item.published_data is None or item.draft_data != item.published_data
            ),
            'published': sum(1 for item in items if item.published_data is not None),
        })
    return {
        'sections': summaries,
        'csrf': csrf_value(req),
        'agency_name': __appname__,
        'show_navigation': True,
    }


def _asset_choices(session, image_only=False, file_only=False):
    assets = session.scalars(
        select(MediaAsset).order_by(MediaAsset.created_at.desc())
    ).all()
    result = []
    for asset in assets:
        is_image = asset.mime_type.startswith('image/')
        if image_only and not is_image:
            continue
        if file_only and is_image:
            continue
        result.append({
            'id': asset.id,
            'label': f'{asset.original_filename} · {asset.file_size // 1024} KB',
            'mime_type': asset.mime_type,
        })
    return result


def _fields_for(kind, data, asset_options):
    fields = []
    for name, label, type_, maximum in FIELD_DEFINITIONS[kind]:
        value = data.get(name, '')
        options = []
        if type_ == 'icon':
            type_ = 'select'
            options = [{'value': key, 'label': key.replace('-', ' ').title()} for key in sorted(ICONS)]
        elif type_ == 'project_type':
            type_ = 'select'
            options = [
                {'value': 'concept', 'label': 'Concept'},
                {'value': 'client', 'label': 'Client work'},
            ]
        elif type_ == 'resource_format':
            type_ = 'select'
            options = [{'value': value, 'label': value} for value in ('PDF', 'DOCX', 'XLSX', 'CSV')]
        elif type_ == 'availability':
            type_ = 'select'
            options = [
                {'value': 'coming_soon', 'label': 'Coming soon'},
                {'value': 'available', 'label': 'Available'},
            ]
        elif type_ == 'image_asset':
            type_ = 'select'
            options = [{'value': '', 'label': 'No image'}] + asset_options['images']
        elif type_ == 'file_asset':
            type_ = 'select'
            options = [{'value': '', 'label': 'No file'}] + asset_options['files']
        elif type_ == 'multi_image_asset':
            type_ = 'multi_image_asset'
            selected = set(value or [])
            options = [dict(option, selected=option['value'] in selected) for option in asset_options['images']]
        fields.append({
            'name': name,
            'label': label,
            'type': type_,
            'value': value,
            'maxlength': maximum,
            'options': options,
        })
    return fields


def _editor_context(section, req, *, error=None, notice=None):
    kind = SECTION_TO_KIND[section]
    with app.db.session() as session:
        records = session.scalars(
            select(CMSRecord)
            .where(CMSRecord.kind == kind)
            .order_by(CMSRecord.display_order, CMSRecord.created_at)
        ).all()
        options = {
            'images': [dict(value=item['id'], label=item['label']) for item in _asset_choices(session, image_only=True)],
            'files': [dict(value=item['id'], label=item['label']) for item in _asset_choices(session, file_only=True)],
        }
        entries = []
        for record in records:
            entries.append({
                'id': record.id,
                'slug': record.slug,
                'title': record.draft_data.get('title') or record.draft_data.get('agency_name') or record.slug,
                'status': record_status(record),
                'archived': record.archived,
                'display_order': record.display_order,
                'draft_visible': record.draft_visible,
                'updated_at': record.updated_at,
                'published_at': record.published_at,
                'fields': _fields_for(kind, record.draft_data, options),
            })
        is_collection = kind in {'service', 'portfolio', 'resource'}
        create_fields = _fields_for(kind, {}, options) if is_collection else []
    status_key = req.query.get('status', '')
    notice = notice or {
        'saved': 'Draft saved. The live homepage is unchanged.',
        'published': 'Changes published to the homepage.',
        'unpublished': 'Item removed from the public homepage.',
        'archived': 'Item archived and removed from the homepage.',
        'restored': 'Item restored.',
        'ordered': 'Display order updated.',
        'uploaded': 'File uploaded to the media library.',
        'updated': 'Media details updated.',
        'deleted': 'Unused media asset deleted.',
    }.get(status_key)
    title, description = SECTION_TEXT[section]
    return {
        'section': section,
        'kind': kind,
        'page_title': title,
        'description': description,
        'entries': entries,
        'create_fields': create_fields,
        'is_collection': is_collection,
        'csrf': csrf_value(req),
        'error': error,
        'notice': notice,
        'media_url': lambda asset_id: f'/media/{asset_id}',
        'agency_name': __appname__,
        'show_navigation': True,
    }


@app.route(r'/admin/(home|services|portfolio|resources|settings)')
@admin_required
@app.bodyguard(strict=True)
@app.queryguard(fields=(guard.String('status', optional=True),), strict=True)
@app.template('admin_editor.mako')
def get(req, section):
    if section not in SECTION_TO_KIND:
        raise statuses.notfound()
    return _editor_context(section, req)


def _move_record(session, record, direction):
    rows = session.scalars(
        select(CMSRecord)
        .where(CMSRecord.kind == record.kind, CMSRecord.archived.is_(False))
        .order_by(CMSRecord.display_order, CMSRecord.created_at)
        .with_for_update()
    ).all()
    index = next((i for i, item in enumerate(rows) if item.id == record.id), None)
    if index is None:
        raise ValueError('Item not found.')
    other_index = index + (-1 if direction == 'up' else 1)
    if 0 <= other_index < len(rows):
        rows[index], rows[other_index] = rows[other_index], rows[index]
        for position, item in enumerate(rows):
            item.display_order = position


@app.route(r'/admin/(home|services|portfolio|resources|settings)', verb='post')
@admin_required
@app.bodyguard(fields=EDITOR_GUARDS, strict=True)
@app.queryguard(strict=True)
@app.template('admin_editor.mako')
def update(req, section):
    if section not in SECTION_TO_KIND:
        raise statuses.notfound()
    verify_csrf(req)
    kind = SECTION_TO_KIND[section]
    action = req.form.get('action', '')
    if action not in {
        'save_draft', 'publish', 'unpublish', 'archive', 'restore',
        'move_up', 'move_down',
    }:
        raise statuses.badrequest(message='Choose a valid content action.')

    error = None
    notice = None
    now = datetime.now(timezone.utc)
    try:
        session = app.db.session()
        with session.begin():
            record_id = req.form.get('record_id', '')
            record = session.get(CMSRecord, record_id) if record_id else None
            if record is not None and record.kind != kind:
                raise ValueError('Content item not found.')
            if kind in {'home', 'settings'} and record is None:
                record = session.scalar(
                    select(CMSRecord).where(
                        CMSRecord.kind == kind,
                        CMSRecord.slug == ('homepage' if kind == 'home' else 'general'),
                    )
                )
            if action in {
                'archive', 'restore', 'unpublish', 'move_up', 'move_down',
            }:
                if record is None:
                    raise ValueError('Save this item before using that action.')
                if action == 'archive':
                    record.archived = True
                    record.updated_at = now
                    notice = 'archived'
                elif action == 'restore':
                    record.archived = False
                    record.updated_at = now
                    notice = 'restored'
                elif action == 'unpublish':
                    record.published_data = None
                    record.published_at = None
                    record.published_visible = False
                    record.updated_at = now
                    notice = 'unpublished'
                else:
                    _move_record(session, record, 'up' if action == 'move_up' else 'down')
                    notice = 'ordered'
            else:
                data = validate_content(kind, req.form, session)
                slug = data.get('slug') or ('homepage' if kind == 'home' else 'general')
                duplicate = session.scalar(
                    select(CMSRecord.id).where(
                        CMSRecord.kind == kind,
                        CMSRecord.slug == slug,
                        CMSRecord.id != (record.id if record else ''),
                    )
                )
                if duplicate:
                    raise ValueError('That URL slug is already in use.')
                if record is None:
                    record = CMSRecord(
                        kind=kind,
                        slug=slug,
                        draft_data=data,
                        display_order=0,
                        draft_visible=True,
                        published_visible=False,
                        archived=False,
                        created_at=now,
                        updated_at=now,
                    )
                    session.add(record)
                    session.flush()
                else:
                    record.slug = slug
                    record.draft_data = data
                    record.updated_at = now
                    record.draft_visible = str(req.form.get('visible', '')).lower() in {'1', 'true', 'yes', 'on'}
                    if req.form.get('display_order'):
                        try:
                            order = int(req.form['display_order'])
                        except (TypeError, ValueError):
                            raise ValueError('Display order must be a whole number.')
                        if not -100000 <= order <= 100000:
                            raise ValueError('Display order must be between -100000 and 100000.')
                        record.display_order = order
                if action == 'publish':
                    publish_record(record)
                    notice = 'published'
                else:
                    notice = 'saved'
    except ValueError as exception:
        error = str(exception)

    if error:
        return _editor_context(section, req, error=error)
    redirect(f'/admin/{section}?status={notice}')


@app.route(r'/admin/media')
@admin_required
@app.bodyguard(strict=True)
@app.queryguard(fields=(guard.String('status', optional=True),), strict=True)
@app.template('admin_media.mako')
def get(req):
    with app.db.session() as session:
        assets = session.scalars(
            select(MediaAsset).order_by(MediaAsset.created_at.desc())
        ).all()
        used = referenced_asset_ids(session)
        rows = [{
            'id': asset.id,
            'filename': asset.original_filename,
            'mime_type': asset.mime_type,
            'size': asset.file_size,
            'width': asset.width,
            'height': asset.height,
            'alt_text': asset.alt_text,
            'decorative': asset.decorative,
            'created_at': asset.created_at,
            'used': asset.id in used,
        } for asset in assets]
    status_key = req.query.get('status', '')
    notice = {
        'uploaded': 'File uploaded to the media library.',
        'updated': 'Media details updated.',
        'deleted': 'Unused media asset deleted.',
    }.get(status_key)
    return {
        'assets': rows,
        'csrf': csrf_value(req),
        'agency_name': __appname__,
        'error': None,
        'notice': notice,
        'max_upload_mb': 10,
        'show_navigation': True,
    }


@app.route(r'/admin/media', verb='post')
@admin_required
@app.bodyguard(fields=MEDIA_FIELDS, strict=True)
@app.queryguard(strict=True)
@app.template('admin_media.mako')
def create(req):
    verify_csrf(req)
    action = req.form.get('action', '')
    if action != 'upload':
        raise statuses.badrequest(message='Choose a valid media action.')
    field = req.files.get('upload')
    if not field or not field.filename:
        return _media_context(req, error='Choose a JPG, PNG, WEBP, PDF, DOCX, XLSX, or CSV file.')
    try:
        inspected = inspect_upload(field)
    except InvalidUpload as error:
        return _media_context(req, error=str(error))

    asset_id = str(uuid.uuid4())
    try:
        app.cms_storage.put(asset_id, inspected['data'], inspected['mime_type'])
        session = app.db.session()
        with session.begin():
            session.add(MediaAsset(
                id=asset_id,
                storage_key=asset_id,
                original_filename=inspected['filename'],
                mime_type=inspected['mime_type'],
                file_size=len(inspected['data']),
                width=inspected['width'],
                height=inspected['height'],
                alt_text=(
                    '' if req.form.get('decorative') else
                    req.form.get('default_alt', '').strip()[:300]
                ),
                decorative=str(req.form.get('decorative', '')).lower() in {'1', 'true', 'yes', 'on'},
            ))
    except Exception:
        try:
            app.cms_storage.delete(asset_id)
        except Exception:
            pass
        return _media_context(
            req,
            error='The upload could not be stored. Check the media storage configuration and try again.',
        )
    redirect('/admin/media?status=uploaded')


def _media_context(req, *, error=None, notice=None):
    with app.db.session() as session:
        assets = session.scalars(
            select(MediaAsset).order_by(MediaAsset.created_at.desc())
        ).all()
        used = referenced_asset_ids(session)
        rows = [{
            'id': asset.id,
            'filename': asset.original_filename,
            'mime_type': asset.mime_type,
            'size': asset.file_size,
            'width': asset.width,
            'height': asset.height,
            'alt_text': asset.alt_text,
            'decorative': asset.decorative,
            'created_at': asset.created_at,
            'used': asset.id in used,
        } for asset in assets]
    return {
        'assets': rows,
        'csrf': csrf_value(req),
        'agency_name': __appname__,
        'error': error,
        'notice': notice,
        'max_upload_mb': 10,
        'show_navigation': True,
    }


@app.route(r'/admin/media/([0-9a-f-]{36})', verb='post')
@admin_required
@app.bodyguard(fields=(
    guard.String('csrf', length=(1, 1024)),
    guard.String('alt_text', length=(0, 300), optional=True),
    guard.String('decorative', length=(0, 5), optional=True),
), strict=True)
@app.queryguard(strict=True)
def update(req, asset_id):
    verify_csrf(req)
    session = app.db.session()
    with session.begin():
        asset = session.get(MediaAsset, asset_id)
        if asset is None:
            raise statuses.notfound()
        asset.alt_text = req.form.get('alt_text', '').strip()
        asset.decorative = str(req.form.get('decorative', '')).lower() in {'1', 'true', 'yes', 'on'}
        if asset.decorative:
            asset.alt_text = ''
    redirect('/admin/media?status=updated')


@app.route(r'/admin/media/([0-9a-f-]{36})/delete', verb='post')
@admin_required
@app.bodyguard(fields=(
    guard.String('csrf', length=(1, 1024)),
    guard.String('confirm_delete', length=(1, 5)),
), strict=True)
@app.queryguard(strict=True)
def delete(req, asset_id):
    verify_csrf(req)
    if req.form.get('confirm_delete') != 'yes':
        return _media_context(req, error='Confirm deletion before removing the asset.')
    session = app.db.session()
    storage_key = None
    in_use = False
    with session.begin():
        asset = session.get(MediaAsset, asset_id, with_for_update=True)
        if asset is None:
            raise statuses.notfound()
        if asset_id in referenced_asset_ids(session):
            in_use = True
        else:
            storage_key = asset.storage_key
            session.delete(asset)
    if in_use:
        return _media_context(req, error='This asset is still used by a draft or published item.')
    try:
        app.cms_storage.delete(storage_key)
    except Exception:
        return _media_context(
            req,
            error='The media record was removed, but storage cleanup failed. Check the storage provider.',
        )
    redirect('/admin/media?status=deleted')


def _asset_response(req, asset, *, attachment=False, cache='private, no-store'):
    try:
        data = app.cms_storage.get(asset['storage_key'])
    except Exception as error:
        raise statuses.serviceunavailable(message='Media storage is temporarily unavailable.') from error
    req.response.length = len(data)
    req.response.contenttype = asset['mime_type']
    req.response.headers['cache-control'] = cache
    req.response.headers['x-content-type-options'] = 'nosniff'
    if attachment:
        filename = quote(asset['original_filename'], safe='')
        req.response.headers['content-disposition'] = (
            f"attachment; filename*=UTF-8''{filename}"
        )
    yield data


@app.route(r'/admin/media/([0-9a-f-]{36})/preview')
@admin_required
@app.bodyguard(strict=True)
@app.queryguard(strict=True)
def get(req, asset_id):
    with app.db.session() as session:
        asset = session.get(MediaAsset, asset_id)
        if asset is None:
            raise statuses.notfound()
        asset_copy = {
            'storage_key': asset.storage_key,
            'mime_type': asset.mime_type,
            'original_filename': asset.original_filename,
        }
    if asset_copy['mime_type'].startswith('image/'):
        return _asset_response(req, asset_copy)
    raise statuses.forbidden()


@app.route(r'/media/([0-9a-f-]{36})')
@app.bodyguard(strict=True)
@app.queryguard(strict=True)
def get(req, asset_id):
    with app.db.session() as session:
        asset = session.get(MediaAsset, asset_id)
        if asset is None or not asset.mime_type.startswith('image/'):
            raise statuses.notfound()
        if asset_id not in referenced_asset_ids(session, published_only=True):
            raise statuses.notfound()
        asset_copy = {
            'storage_key': asset.storage_key,
            'mime_type': asset.mime_type,
            'original_filename': asset.original_filename,
        }
    return _asset_response(req, asset_copy, cache='public, max-age=300')


@app.route(r'/admin/media/([0-9a-f-]{36})/download')
@admin_required
@app.bodyguard(strict=True)
@app.queryguard(strict=True)
def get(req, asset_id):
    with app.db.session() as session:
        asset = session.get(MediaAsset, asset_id)
        if asset is None:
            raise statuses.notfound()
        asset_copy = {
            'storage_key': asset.storage_key,
            'mime_type': asset.mime_type,
            'original_filename': asset.original_filename,
        }
    return _asset_response(req, asset_copy, attachment=True)


@app.route(r'/resources/([a-z0-9-]+)/download')
@app.bodyguard(strict=True)
@app.queryguard(strict=True)
def get(req, slug):
    with app.db.session() as session:
        record = session.scalar(
            select(CMSRecord).where(
                CMSRecord.kind == 'resource',
                CMSRecord.slug == slug,
                CMSRecord.published_data.is_not(None),
                CMSRecord.published_visible.is_(True),
                CMSRecord.archived.is_(False),
            )
        )
        if record is None:
            raise statuses.notfound()
        data = record.published_data
        if data.get('availability') != 'available':
            raise statuses.notfound()
        if data.get('external_url'):
            redirect(data['external_url'])
        asset = session.get(MediaAsset, data.get('file_asset_id'))
        if asset is None or asset.mime_type.startswith('image/'):
            raise statuses.notfound()
        asset_copy = {
            'storage_key': asset.storage_key,
            'mime_type': asset.mime_type,
            'original_filename': asset.original_filename,
        }
    return _asset_response(req, asset_copy, attachment=True, cache='private, no-store')
