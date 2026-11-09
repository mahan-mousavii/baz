from datetime import date

from sqlalchemy.exc import SQLAlchemyError

from .cms.content import fallback_homepage, public_homepage
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
    headline_emphasis, separator, headline_remainder = (
        headline_lines[1].partition(' ')
    )
    for key in ('resources_heading', 'about_heading', 'contact_heading'):
        page[f'{key}_lines'] = (page['home'].get(key, '').splitlines() + ['', ''])[:2]
    page.update({
        'headline_lines': headline_lines[:2],
        'headline_emphasis': headline_emphasis,
        'headline_remainder': (
            f'{separator}{headline_remainder}' if separator else ''
        ),
        'year': date.today().year,
    })
    return page
