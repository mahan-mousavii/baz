import os
import secrets
import json

from yhttp.core import Application
from yhttp.ext import auth, dbmanager, mako, sqlalchemy as saext

from . import assets
from .common.models import BaseModel
from .manifest import __appname__, __version__


env = os.environ.get('YHTTP_ENV', 'development')
pkgdir = os.path.dirname(__file__)
prjdir = os.path.abspath(os.path.join(pkgdir, '..'))
vardir = os.path.join(prjdir, '.var')
os.makedirs(vardir, exist_ok=True)
database_url = os.environ.get(
    'DATABASE_URL', f'postgresql://:@/{__appname__}',
)
public_url = os.environ.get('PUBLIC_URL', 'http://127.0.0.1:8080')

app = Application(__version__, __appname__)
dbmanager.install(app)
saext.install(app, basemodel=BaseModel)
mako.install(app, data={
    'settings': app.settings,
    'asseturl': assets.urlresolver(app),
})
auth.install(app)

app.settings |= f'''
debug: true
env: {env}
publicurl: {json.dumps(public_url)}

assets:
  serve: true
  manifest: {vardir}/static/.vite/manifest.json
  directory: {vardir}/static/assets
  url: /assets

public:
  serve: true
  directory: {prjdir}/public
  url: /

db:
  url: {json.dumps(database_url)}
  migration:
    directory: {pkgdir}/dbmigration

mako:
  modules: {vardir}/mako
  lookup:
    - {pkgdir}/templates
'''


def auth_access_secret(environment, secret):
    if not secret:
        if environment == 'production':
            raise RuntimeError(
                'YHTTP_AUTH_ACCESS_SECRET must be configured in production.'
            )
        secret = secrets.token_urlsafe(48)
    if len(secret) < 32:
        raise RuntimeError(
            'YHTTP_AUTH_ACCESS_SECRET must be at least 32 characters.'
        )
    return secret


app.settings.auth.accesstoken.secret = auth_access_secret(
    env, os.environ.get('YHTTP_AUTH_ACCESS_SECRET'),
)
app.settings.auth.accesstoken.cookie.secure = env != 'development'
app.settings.auth.accesstoken.cookie.samesite = 'Strict'
app.settings.auth.redis.host = os.environ.get('YHTTP_AUTH_REDIS_HOST', 'localhost')
app.settings.auth.redis.port = int(os.environ.get('YHTTP_AUTH_REDIS_PORT', '6379'))
app.settings.auth.redis.db = int(os.environ.get('YHTTP_AUTH_REDIS_DB', '0'))

from .cms.storage import storage_from_environment  # noqa: E402

app.cms_storage = storage_from_environment(vardir)


@app.when
def ready(app):
    if app.settings.env == 'development':
        app.settings.assets.serve = False
        app.settings.assets.url = 'http://localhost:5173'
    elif app.settings.assets.serve:
        app.staticdirectory(
            app.settings.assets.url,
            app.settings.assets.directory,
            autoindex=False,
            exists='remove',
        )

    if app.settings.public.serve:
        app.staticdirectory(
            app.settings.public.url,
            app.settings.public.directory,
            exists='remove',
        )


from . import routes  # noqa: E402,F401
from .cms import admin  # noqa: E402,F401
