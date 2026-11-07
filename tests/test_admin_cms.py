from sqlalchemy import select
from yhttp.ext.auth import AccessToken

from bddrest import response, status

from yhttp_ssr_boilerplate.cms.content import seed_records
from yhttp_ssr_boilerplate.common.models import CMSRecord


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
    with app.db.session.begin() as session:
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
