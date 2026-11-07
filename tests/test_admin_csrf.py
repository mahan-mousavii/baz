from copy import deepcopy
from html.parser import HTMLParser

import pytest
from bddrest import Given
from sqlalchemy import create_engine, select

from yhttp_ssr_boilerplate import app as application
from yhttp_ssr_boilerplate.cms.content import seed_records
from yhttp_ssr_boilerplate.common.models import CMSRecord


class CsrfInputParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'input' and attributes.get('name') == 'csrf':
            self.values.append(attributes.get('value', ''))


@pytest.fixture
def csrf_app(tmp_path, monkeypatch):
    engine = create_engine(f'sqlite:///{tmp_path / "csrf-test.sqlite"}')

    def connect(url=None):
        application.db.engine = engine
        application.db.session.configure(bind=engine)

    monkeypatch.setattr(application.db, 'connect', connect)
    monkeypatch.setattr(application.auth, 'blacklist_has', lambda _: False)
    monkeypatch.setenv('YHTTP_ADMIN_USERNAME', 'csrf-test-admin')
    monkeypatch.setenv('YHTTP_ADMIN_PASSWORD', 'csrf-test-password')
    application.settings |= (
        f"db:\n  url: sqlite:///{tmp_path / 'csrf-test.sqlite'}\n"
        f"mako:\n  modules: {tmp_path / 'mako'}\n"
    )
    application.ready()
    application.db.create_objects()
    with application.db.session() as session:
        with session.begin():
            seed_records(session)

    yield application

    application.db.session.remove()
    application.shutdown()


def _login(csrf_app):
    with Given(
        csrf_app,
        '/admin/login',
        verb='POST',
        form={
            'username': 'csrf-test-admin',
            'password': 'csrf-test-password',
        },
    ) as call:
        assert call.response.status == 303
        # bddrest exposes Set-Cookie attributes with the value; a browser sends
        # only the cookie value on the next request.
        return call.response.cookies['yhttp-accesstoken'].split(';', 1)[0]


def _form_csrf_values(html):
    parser = CsrfInputParser()
    parser.feed(html)
    return parser.values


def _home_form(csrf_app, csrf, action):
    with csrf_app.db.session() as session:
        record = session.scalar(
            select(CMSRecord).where(CMSRecord.kind == 'home')
        )
        record_id = record.id
        data = deepcopy(record.draft_data)
    data.update({
        'csrf': csrf,
        'action': action,
        'record_id': record_id,
        'visible': 'yes',
        'display_order': '0',
        'hero_description': f'Changed by a valid {action} request.',
    })
    return record_id, data


@pytest.mark.parametrize('action', ('save_draft', 'publish'))
def test_authenticated_draft_and_publish_requests_accept_session_csrf(
    csrf_app,
    action,
):
    cookie = _login(csrf_app)
    with Given(
        csrf_app,
        '/admin/home',
        cookies={'yhttp-accesstoken': cookie},
    ) as call:
        values = _form_csrf_values(call.response.text)
        assert values and values[0]
        assert all(value == values[0] for value in values)
        csrf = values[0]

    record_id, form = _home_form(csrf_app, csrf, action)
    with Given(
        csrf_app,
        '/admin/home',
        verb='POST',
        cookies={'yhttp-accesstoken': cookie},
        form=form,
    ) as call:
        status_key = 'published' if action == 'publish' else 'saved'
        assert call.response.status == 303
        assert call.response.headers['location'] == f'/admin/home?status={status_key}'

    with csrf_app.db.session() as session:
        record = session.get(CMSRecord, record_id)
        assert record.draft_data['hero_description'] == form['hero_description']
        if action == 'publish':
            assert record.published_data['hero_description'] == form['hero_description']
        else:
            assert record.published_data['hero_description'] != form['hero_description']


@pytest.mark.parametrize('csrf', (None, 'not-the-session-token'))
def test_editor_rejects_missing_or_invalid_csrf(csrf_app, csrf):
    cookie = _login(csrf_app)
    form = {'action': 'publish'}
    if csrf is not None:
        form['csrf'] = csrf

    with Given(
        csrf_app,
        '/admin/home',
        verb='POST',
        cookies={'yhttp-accesstoken': cookie},
        form=form,
    ) as call:
        assert call.response.status == 403


def test_freshly_loaded_editor_form_submits_after_login(csrf_app):
    cookie = _login(csrf_app)
    with Given(
        csrf_app,
        '/admin/home',
        cookies={'yhttp-accesstoken': cookie},
    ) as call:
        csrf_values = _form_csrf_values(call.response.text)
        assert csrf_values and csrf_values[0]

    record_id, form = _home_form(csrf_app, csrf_values[0], 'save_draft')
    with Given(
        csrf_app,
        '/admin/home',
        verb='POST',
        cookies={'yhttp-accesstoken': cookie},
        form=form,
    ) as call:
        assert call.response.status == 303
        assert call.response.headers['location'] == '/admin/home?status=saved'

    with csrf_app.db.session() as session:
        record = session.get(CMSRecord, record_id)
        assert record.draft_data['hero_description'] == form['hero_description']


@pytest.mark.parametrize(
    'section', ('home', 'services', 'portfolio', 'resources', 'settings'),
)
def test_each_editor_section_renders_the_authenticated_csrf_value(
    csrf_app,
    section,
):
    cookie = _login(csrf_app)
    with Given(
        csrf_app,
        f'/admin/{section}',
        cookies={'yhttp-accesstoken': cookie},
    ) as call:
        values = _form_csrf_values(call.response.text)
        assert values and values[0]
        assert all(value == values[0] for value in values)
