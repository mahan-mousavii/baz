import functools

import bddrest
import pytest

import mahnil


pytest_plugins = ['yhttp.dev.fixtures']


@pytest.fixture
def app(freshdb, tmp_path):
    mahnil.app.settings |= f'''
db:
  url: {freshdb}
mako:
  modules: {tmp_path / 'mako'}
media:
  directory: {tmp_path / 'media'}
'''
    mahnil.app.ready()
    mahnil.app.db.create_objects()
    yield mahnil.app
    mahnil.app.shutdown()


@pytest.fixture
def httpreq(app):
    return functools.partial(bddrest.Given, app)
