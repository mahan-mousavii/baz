from datetime import date

from sqlalchemy.exc import SQLAlchemyError

from .cms.content import fallback_homepage, public_homepage
from .homepage import DECORATIONS
from .rollup import app


@app.route(r'/')
@app.bodyguard(strict=True)
@app.queryguard(strict=True)
@app.template('index.mako')
def get(req):
    try:
        with app.db.session() as session:
            page = public_homepage(session)
    except SQLAlchemyError:
        # Keep the public homepage readable during a brief database outage;
        # the CMS still requires PostgreSQL for edits and publication.
        page = fallback_homepage()

    headline_lines = (page['home'].get('headline', '').splitlines() + ['', ''])[:2]
    for key in ('resources_heading', 'about_heading', 'contact_heading'):
        page[f'{key}_lines'] = (page['home'].get(key, '').splitlines() + ['', ''])[:2]
    page.update({
        'decorations': DECORATIONS,
        'headline_lines': headline_lines[:2],
        'year': date.today().year,
    })
    return page
