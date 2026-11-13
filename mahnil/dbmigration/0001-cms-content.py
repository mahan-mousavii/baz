"""Create the initial CMS content, media, and administrator tables."""


def upgrade(db):
    db.execute('''
        CREATE TABLE cms_records (
            id VARCHAR(36) PRIMARY KEY,
            kind VARCHAR(24) NOT NULL,
            slug VARCHAR(120) NOT NULL,
            draft_data JSON NOT NULL,
            published_data JSON,
            display_order INTEGER NOT NULL DEFAULT 0,
            draft_visible BOOLEAN NOT NULL DEFAULT TRUE,
            published_visible BOOLEAN NOT NULL DEFAULT TRUE,
            archived BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
            published_at TIMESTAMPTZ,
            CONSTRAINT uq_cms_records_kind_slug UNIQUE (kind, slug),
            CONSTRAINT ck_cms_records_kind
                CHECK (kind IN ('home', 'service', 'portfolio', 'resource', 'settings'))
        );
    ''')
    db.execute('CREATE INDEX ix_cms_records_kind ON cms_records (kind);')
    db.execute('''
        CREATE TABLE cms_media_assets (
            id VARCHAR(36) PRIMARY KEY,
            storage_key VARCHAR(255) NOT NULL UNIQUE,
            original_filename VARCHAR(255) NOT NULL,
            mime_type VARCHAR(100) NOT NULL,
            file_size INTEGER NOT NULL,
            width INTEGER,
            height INTEGER,
            alt_text TEXT NOT NULL DEFAULT '',
            decorative BOOLEAN NOT NULL DEFAULT FALSE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    db.execute('''
        CREATE TABLE cms_admin_auth_state (
            id INTEGER PRIMARY KEY,
            failures INTEGER NOT NULL DEFAULT 0,
            window_started_at TIMESTAMPTZ,
            locked_until TIMESTAMPTZ
        );
    ''')
    db.execute('''
        INSERT INTO cms_admin_auth_state (id, failures)
        VALUES (1, 0)
        ON CONFLICT (id) DO NOTHING;
    ''')


def downgrade(db):
    db.execute('DROP TABLE cms_admin_auth_state;')
    db.execute('DROP TABLE cms_media_assets;')
    db.execute('DROP TABLE cms_records;')
