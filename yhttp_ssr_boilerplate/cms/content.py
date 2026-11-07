"""Validated CMS content operations and public homepage projection."""

import re
from datetime import datetime, timezone
from urllib.parse import urlparse

from sqlalchemy import select
from yhttp.core import statuses

from ..common.models import CMSRecord, MediaAsset
from ..homepage import AGENCY, PROJECTS, SERVICES, TOOLS


KINDS = {'home', 'service', 'portfolio', 'resource', 'settings'}
ICONS = {
    'compass',
    'clapperboard',
    'message-circle',
    'trending-up',
    'camera',
    'video',
    'megaphone',
    'pen-tool',
    'aperture',
    'sparkles',
    'bar-chart',
}
RESOURCE_FORMATS = {'PDF', 'DOCX', 'XLSX', 'CSV'}
PROJECT_TYPES = {'client', 'concept'}
AVAILABILITIES = {'coming_soon', 'available'}
SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def _text(form, name, label, maximum, required=True):
    value = str(form.get(name, '')).strip()
    if required and not value:
        raise ValueError(f'{label} is required.')
    if len(value) > maximum:
        raise ValueError(f'{label} must be {maximum} characters or fewer.')
    return value


def _two_line_text(form, name, label, maximum):
    value = _text(form, name, label, maximum)
    if len(value.splitlines()) > 2:
        raise ValueError(f'{label} can use at most two lines.')
    return value


def _url(value, label, *, anchors=False, optional=True):
    if not value:
        if optional:
            return ''
        raise ValueError(f'{label} is required.')
    if value != value.strip() or '\\' in value or any(ord(char) < 32 for char in value):
        raise ValueError(f'{label} is not a valid URL.')
    parsed = urlparse(value)
    valid = (
        (anchors and value.startswith('#') and len(value) > 1)
        or (value.startswith('/') and not value.startswith('//'))
        or (parsed.scheme == 'https' and bool(parsed.netloc))
    )
    if not valid:
        raise ValueError(f'{label} must be a site path, section anchor, or HTTPS URL.')
    return value


def _asset(session, asset_id, label, *, mime_prefix=None, optional=True):
    asset_id = (asset_id or '').strip()
    if not asset_id:
        if optional:
            return ''
        raise ValueError(f'{label} is required.')
    asset = session.get(MediaAsset, asset_id)
    if asset is None:
        raise ValueError(f'{label} must reference an existing media asset.')
    if mime_prefix and not asset.mime_type.startswith(mime_prefix):
        raise ValueError(f'{label} must reference a {mime_prefix.rstrip("/")} file.')
    return asset_id


def validate_content(kind, form, session):
    """Convert submitted plain form fields to one validated structured record."""
    if kind not in KINDS:
        raise ValueError('Unknown content type.')

    if kind == 'home':
        return {
            'eyebrow': _text(form, 'eyebrow', 'Hero eyebrow', 120),
            'headline': _two_line_text(form, 'headline', 'Hero headline', 180),
            'hero_description': _text(form, 'hero_description', 'Hero description', 500),
            'primary_cta_label': _text(form, 'primary_cta_label', 'Primary button label', 80),
            'primary_cta_href': _url(
                _text(form, 'primary_cta_href', 'Primary button destination', 500),
                'Primary button destination', anchors=True, optional=False,
            ),
            'secondary_cta_label': _text(form, 'secondary_cta_label', 'Secondary button label', 80),
            'secondary_cta_href': _url(
                _text(form, 'secondary_cta_href', 'Secondary button destination', 500),
                'Secondary button destination', anchors=True, optional=False,
            ),
            'services_heading': _text(form, 'services_heading', 'Services heading', 180),
            'services_intro': _text(form, 'services_intro', 'Services introduction', 500),
            'portfolio_heading': _text(form, 'portfolio_heading', 'Portfolio heading', 180),
            'portfolio_intro': _text(form, 'portfolio_intro', 'Portfolio introduction', 500),
            'resources_heading': _two_line_text(form, 'resources_heading', 'Resources heading', 180),
            'resources_intro': _text(form, 'resources_intro', 'Resources introduction', 500),
            'about_heading': _two_line_text(form, 'about_heading', 'About heading', 180),
            'about_description': _text(form, 'about_description', 'About description', 700),
            'contact_heading': _two_line_text(form, 'contact_heading', 'Contact heading', 180),
            'contact_description': _text(form, 'contact_description', 'Contact introduction', 500),
        }

    if kind == 'settings':
        email = _text(form, 'business_email', 'Business email', 254, required=False)
        if email and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email):
            raise ValueError('Business email is not valid.')
        return {
            'agency_name': _text(form, 'agency_name', 'Agency name', 100),
            'logo_asset_id': _asset(
                session, form.get('logo_asset_id'), 'Logo', mime_prefix='image/',
            ),
            'description': _text(form, 'description', 'Agency description', 300),
            'business_email': email,
            'whatsapp_url': _url(
                _text(form, 'whatsapp_url', 'WhatsApp destination', 500, required=False),
                'WhatsApp destination',
            ),
            'instagram_url': _url(
                _text(form, 'instagram_url', 'Instagram URL', 500, required=False),
                'Instagram URL',
            ),
            'linkedin_url': _url(
                _text(form, 'linkedin_url', 'LinkedIn URL', 500, required=False),
                'LinkedIn URL',
            ),
            'footer_text': _text(form, 'footer_text', 'Footer text', 300, required=False),
        }

    result = {
        'slug': _text(form, 'slug', 'URL slug', 120).lower(),
        'title': _text(form, 'title', 'Title', 160),
        'description': _text(form, 'description', 'Description', 700),
    }
    if not SLUG_RE.fullmatch(result['slug']):
        raise ValueError('URL slug may contain lowercase letters, numbers, and single hyphens.')

    if kind == 'service':
        icon = _text(form, 'icon', 'Icon', 32)
        if icon not in ICONS:
            raise ValueError('Select an icon from the provided list.')
        result.update({
            'subtitle': _text(form, 'subtitle', 'Subtitle', 160),
            'icon': icon,
        })
    elif kind == 'portfolio':
        project_type = _text(form, 'project_type', 'Project type', 20)
        if project_type not in PROJECT_TYPES:
            raise ValueError('Select client work or concept.')
        cover_id = _asset(
            session, form.get('cover_asset_id'), 'Cover image', mime_prefix='image/',
        )
        additional = []
        for item in form.getall('additional_asset_ids'):
            item = item.strip()
            if item:
                additional.append(
                    _asset(session, item, 'Additional image', mime_prefix='image/')
                )
        result.update({
            'category': _text(form, 'category', 'Category', 100),
            'project_type': project_type,
            'cover_asset_id': cover_id,
            'cover_alt': _text(form, 'cover_alt', 'Cover image alt text', 300, required=False),
            'cover_decorative': str(form.get('cover_decorative', '')).lower() in {'1', 'true', 'yes', 'on'},
            'additional_asset_ids': additional,
            'featured': str(form.get('featured', '')).lower() in {'1', 'true', 'yes', 'on'},
        })
    elif kind == 'resource':
        format_ = _text(form, 'format', 'Format', 10).upper()
        availability = _text(form, 'availability', 'Availability', 20)
        if format_ not in RESOURCE_FORMATS:
            raise ValueError('Select a supported download format.')
        if availability not in AVAILABILITIES:
            raise ValueError('Select an availability state.')
        cover_id = _asset(
            session, form.get('cover_asset_id'), 'Cover image', mime_prefix='image/',
        )
        file_id = _asset(session, form.get('file_asset_id'), 'Download file')
        external_url = _url(
            _text(form, 'external_url', 'External resource URL', 500, required=False),
            'External resource URL',
        )
        if file_id and external_url:
            raise ValueError('Choose either a file or an external resource URL.')
        if availability == 'available' and not (file_id or external_url):
            raise ValueError('Add a download file or external HTTPS URL before publishing as available.')
        if file_id:
            asset = session.get(MediaAsset, file_id)
            allowed = {
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'text/csv',
            }
            if asset.mime_type not in allowed:
                raise ValueError('The selected file is not an approved resource format.')
            ext = asset.original_filename.rsplit('.', 1)[-1].upper()
            if ext != format_:
                raise ValueError('The selected file format does not match the resource format.')
        result.update({
            'category': _text(form, 'category', 'Category', 100),
            'format': format_,
            'availability': availability,
            'cover_asset_id': cover_id,
            'cover_alt': _text(form, 'cover_alt', 'Cover image alt text', 300, required=False),
            'cover_decorative': str(form.get('cover_decorative', '')).lower() in {'1', 'true', 'yes', 'on'},
            'file_asset_id': file_id,
            'external_url': external_url,
        })
    return result


def record_status(record):
    if record.archived:
        return 'Archived'
    if record.published_data is None:
        return 'Draft'
    if record.draft_data != record.published_data:
        return 'Draft changes'
    return 'Published'


def publish_record(record):
    """Replace the live snapshot in one database transaction."""
    record.published_data = dict(record.draft_data)
    record.published_visible = record.draft_visible
    record.published_at = datetime.now(timezone.utc)
    record.updated_at = datetime.now(timezone.utc)
    record.archived = False


def referenced_asset_ids(session, *, published_only=False):
    result = set()
    records = session.scalars(select(CMSRecord)).all()
    for record in records:
        if published_only and (
            record.published_data is None
            or not record.published_visible
            or record.archived
        ):
            continue
        snapshots = [record.published_data] if published_only else [
            record.draft_data, record.published_data,
        ]
        for snapshot in snapshots:
            if not snapshot:
                continue
            for key in ('logo_asset_id', 'cover_asset_id', 'file_asset_id'):
                if snapshot.get(key):
                    result.add(snapshot[key])
            result.update(snapshot.get('additional_asset_ids', []))
    return result


def _initial_content():
    home = {
        'eyebrow': 'Creative Marketing Agency · Oman',
        'headline': 'Clear strategy.\nDistinctive content.',
        'hero_description': (
            'We help businesses in Oman turn ideas into thoughtful marketing, '
            'compelling content, and distinctive visual experiences.'
        ),
        'primary_cta_label': 'Explore Our Services',
        'primary_cta_href': '#services-work',
        'secondary_cta_label': 'Explore Free Tools',
        'secondary_cta_href': '#free-tools',
        'services_heading': 'From clear direction to creative execution.',
        'services_intro': 'Strategy, content, social media, and campaigns — working together for your brand.',
        'portfolio_heading': 'Selected explorations',
        'portfolio_intro': 'A feel for the possible.',
        'resources_heading': 'Practical tools.\nA clearer next step.',
        'resources_intro': 'Simple resources to help you plan your marketing, organize your content, and move forward independently.',
        'about_heading': 'A thoughtful approach\nto brand growth.',
        'about_description': 'Based in Oman, we bring marketing thinking and creative production together to help businesses communicate clearly and show up with purpose.',
        'contact_heading': 'Let’s create\nyour next move.',
        'contact_description': 'Tell us what you’re building and where you need support.',
    }
    settings = {
        'agency_name': AGENCY['name'],
        'logo_asset_id': '',
        'description': AGENCY['positioning'],
        'business_email': AGENCY['email'] or '',
        'whatsapp_url': AGENCY['whatsapp_url'] or '',
        'instagram_url': '',
        'linkedin_url': '',
        'footer_text': 'Thoughtful marketing. Distinctive creative.',
    }
    values = [
        ('home', 'homepage', home, 0),
        ('settings', 'general', settings, 0),
    ]
    for index, service in enumerate(SERVICES):
        slug = re.sub(r'[^a-z0-9]+', '-', service['title'].lower()).strip('-')
        values.append((
            'service', slug,
            {'title': service['title'], 'subtitle': service['subtitle'],
             'description': service['description'], 'icon': service['icon'],
             'slug': slug},
            index,
        ))
    for index, project in enumerate(PROJECTS):
        slug = re.sub(r'[^a-z0-9]+', '-', project['title'].lower()).strip('-')
        values.append((
            'portfolio', slug,
            {'slug': slug, 'title': project['title'],
             'description': project['type'],
             'category': project['type'].split('·')[0].strip(),
             'project_type': 'concept', 'cover_asset_id': '',
             'cover_alt': '', 'additional_asset_ids': [], 'featured': index == 0,
             'style': project['style']},
            index,
        ))
    for index, tool in enumerate(TOOLS):
        slug = re.sub(r'[^a-z0-9]+', '-', tool['title'].lower()).strip('-')
        values.append((
            'resource', slug,
            {'slug': slug, 'title': tool['title'],
             'description': tool['description'], 'category': 'Marketing',
             'format': 'PDF', 'availability': 'coming_soon',
             'cover_asset_id': '', 'cover_alt': '', 'file_asset_id': '',
             'external_url': ''},
            index,
        ))
    return values


def fallback_homepage():
    """Keep the existing homepage available before the one-time CMS seed."""
    home = _initial_content()[0][2]
    services = []
    for service in SERVICES:
        slug = re.sub(r'[^a-z0-9]+', '-', service['title'].lower()).strip('-')
        services.append(dict(service, slug=slug))
    projects = []
    for index, project in enumerate(PROJECTS):
        projects.append(dict(
            project,
            slug=f'concept-{index + 1}',
            description=project['type'],
            category=project['type'].split('·')[0].strip(),
            project_type='concept',
            cover_asset_id='',
            cover_alt='',
            cover_decorative=False,
            additional_asset_ids=[],
            featured=index == 0,
        ))
    resources = []
    for tool in TOOLS:
        slug = re.sub(r'[^a-z0-9]+', '-', tool['title'].lower()).strip('-')
        resources.append(dict(
            tool,
            slug=slug,
            category='Marketing',
            format='PDF',
            availability='coming_soon',
            cover_asset_id='',
            cover_alt='',
            cover_decorative=False,
            file_asset_id='',
            external_url='',
            download_href='',
        ))
    return {
        'agency': dict(AGENCY, logo_asset_id=None, instagram_url=None,
                       linkedin_url=None, footer_text=''),
        'home': home,
        'navigation': (
            {'label': 'Home', 'href': '#top'},
            {'label': 'Free Tools', 'href': '#free-tools'},
            {'label': 'Services & Work', 'href': '#services-work'},
            {'label': 'Contact', 'href': '#contact', 'cta': True},
        ),
        'projects': projects,
        'services': services,
        'tools': resources,
        'settings': _initial_content()[1][2],
    }


def seed_records(session):
    """Insert existing homepage copy once without replacing later edits."""
    inserted = 0
    for kind, slug, data, display_order in _initial_content():
        existing = session.scalar(
            select(CMSRecord).where(CMSRecord.kind == kind, CMSRecord.slug == slug)
        )
        if existing is not None:
            continue
        session.add(CMSRecord(
            kind=kind,
            slug=slug,
            draft_data=data,
            published_data=data,
            display_order=display_order,
            draft_visible=True,
            published_visible=True,
            archived=False,
            published_at=datetime.now(timezone.utc),
        ))
        inserted += 1
    return inserted


def public_homepage(session):
    all_records = session.scalars(select(CMSRecord)).all()
    if not all_records:
        return fallback_homepage()
    records = session.scalars(
        select(CMSRecord)
        .where(
            CMSRecord.published_data.is_not(None),
            CMSRecord.published_visible.is_(True),
            CMSRecord.archived.is_(False),
        )
        .order_by(CMSRecord.display_order, CMSRecord.created_at)
    ).all()
    by_kind = {}
    for record in records:
        by_kind.setdefault(record.kind, []).append(record)

    home_record = next(iter(by_kind.get('home', [])), None)
    settings_record = next(iter(by_kind.get('settings', [])), None)
    home = (
        dict(home_record.published_data)
        if home_record
        else dict.fromkeys(_initial_content()[0][2], '')
    )
    settings = (
        dict(settings_record.published_data)
        if settings_record
        else {
            'agency_name': AGENCY['name'],
            'description': '',
            'business_email': '',
            'whatsapp_url': '',
            'logo_asset_id': '',
            'instagram_url': '',
            'linkedin_url': '',
            'footer_text': '',
        }
    )
    agency = {
        'name': settings.get('agency_name') or AGENCY['name'],
        'positioning': settings.get('description') or AGENCY['positioning'],
        'email': settings.get('business_email') or None,
        'whatsapp_url': settings.get('whatsapp_url') or None,
        'logo_asset_id': settings.get('logo_asset_id') or None,
        'instagram_url': settings.get('instagram_url') or None,
        'linkedin_url': settings.get('linkedin_url') or None,
        'footer_text': settings.get('footer_text') or '',
    }
    services = [dict(r.published_data) for r in by_kind.get('service', [])]
    portfolio_records = sorted(
        by_kind.get('portfolio', []),
        key=lambda record: (
            not bool(record.published_data.get('featured')),
            record.display_order,
            record.created_at,
        ),
    )
    projects = [dict(r.published_data) for r in portfolio_records]
    resource_rows = [r for r in by_kind.get('resource', [])]
    for index, project in enumerate(projects):
        project['number'] = f'{index + 1:02d}'
        project['type'] = 'Client work' if project.get('project_type') == 'client' else 'Concept Preview'
        project['style'] = (
            project.get('style')
            if project.get('style') in {'ritual', 'road'}
            else ('ritual' if index == 0 else 'road')
        )
    resources = [dict(record.published_data) for record in resource_rows]
    for project in projects:
        asset = session.get(MediaAsset, project.get('cover_asset_id')) if project.get('cover_asset_id') else None
        if project.get('cover_decorative'):
            project['cover_alt'] = ''
        elif not project.get('cover_alt'):
            project['cover_alt'] = asset.alt_text if asset and not asset.decorative else ''
    for resource in resources:
        asset = session.get(MediaAsset, resource.get('cover_asset_id')) if resource.get('cover_asset_id') else None
        if resource.get('cover_decorative'):
            resource['cover_alt'] = ''
        elif not resource.get('cover_alt'):
            resource['cover_alt'] = asset.alt_text if asset and not asset.decorative else ''
        resource['download_href'] = (
            f"/resources/{resource['slug']}/download"
            if resource.get('availability') == 'available' and resource.get('file_asset_id')
            else resource.get('external_url', '')
            if resource.get('availability') == 'available'
            else ''
        )
    navigation = (
        {'label': 'Home', 'href': '#top'},
        {'label': 'Free Tools', 'href': '#free-tools'},
        {'label': 'Services & Work', 'href': '#services-work'},
        {'label': 'Contact', 'href': '#contact', 'cta': True},
    )
    return {
        'agency': agency,
        'home': home,
        'navigation': navigation,
        'projects': projects,
        'services': services,
        'tools': resources,
        'settings': settings,
    }
