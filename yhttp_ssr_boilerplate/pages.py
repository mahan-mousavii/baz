from .rollup import app
from .homepage import AGENCY, NAVIGATION, PROJECTS, SERVICES, TOOLS


@app.route(r'/')
@app.bodyguard(strict=True)
@app.queryguard(strict=True)
@app.template('index.mako')
def get(req):
    from datetime import date

    return {
        'agency': AGENCY,
        'navigation': NAVIGATION,
        'projects': PROJECTS,
        'services': SERVICES,
        'tools': TOOLS,
        'year': date.today().year,
    }
