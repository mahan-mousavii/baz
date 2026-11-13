"""Idempotently import the existing homepage copy into the CMS."""

from .cms.content import seed_records
from .rollup import app


def main():
    app.db.connect()
    try:
        session = app.db.session()
        with session.begin():
            count = seed_records(session)
    finally:
        app.db.disconnect()
    print(f'Inserted {count} initial CMS records; existing edits were preserved.')


if __name__ == '__main__':
    main()
