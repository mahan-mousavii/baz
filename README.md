# YHTTP SSR Boilerplate

A server-side-rendered creative agency homepage built with YHTTP, Mako, Tailwind CSS v4, and Alpine.js. The custom CMS edits the existing homepage; it does not create additional public pages.

## Local development

The application needs PostgreSQL for content and login rate limits, Redis for yhttp-auth session checks, and Node.js/pnpm for Vite assets.

1. Create the Python environment and install project dependencies using the repository targets:

   ```sh
   make venv
   make env
   ```

   The Makefile requires `python-makelib` at `/usr/local/lib/python-makelib`. Start PostgreSQL and Redis using your local service manager.

2. Copy `.env.example` to `.env`. Set a unique administrator username and password, and generate a session signing key:

   ```sh
   python -c 'import secrets; print(secrets.token_urlsafe(48))'
   ```

   Paste that value into `YHTTP_AUTH_ACCESS_SECRET`. Keep `.env` private; it is ignored by Git. Set `DATABASE_URL` to the PostgreSQL database you created. The example targets a local PostgreSQL server and a database named `yhttp-ssr-boilerplate`; adjust it for your local authentication settings.

   Set `YHTTP_ADMIN_USERNAME` and `YHTTP_ADMIN_PASSWORD` in `.env` as well. The application does not load `.env` automatically: export its values in the same shell before starting the server. Restrict the file to your account with `chmod 600 .env`.

3. Load the local environment into the current shell and apply the versioned migration, then import the current homepage copy. Keep this shell open and start the server from it in step 4:

   ```sh
   set -a
   . ./.env
   set +a
   yhttp-ssr-boilerplate db migration upgrade
   python -m yhttp_ssr_boilerplate.seed_content
   ```

   The seed inserts the Phase 1/2 homepage, four services, two concept previews, three coming-soon resources, and general settings only when each record is absent. Running it again leaves admin edits intact.

4. Start the website and Vite:

   ```sh
   make run
   ```

   Open the public homepage at `http://127.0.0.1:8080/` and the admin panel at `http://127.0.0.1:8080/admin`. The admin login stays disabled until both `YHTTP_ADMIN_USERNAME` and `YHTTP_ADMIN_PASSWORD` are set.

## CMS workflow

- Use `/admin/home`, `/admin/services`, `/admin/portfolio`, `/admin/resources`, `/admin/media`, and `/admin/settings` to manage the homepage content.
- The image picker is available on the homepage hero visual, agency logo, portfolio cover, and resource cover fields. Select from the library, upload an image from the field, or remove that section's reference. Uploading or changing a selection does not publish it; use Save draft or Publish on the relevant entry.
- `/admin/media` is the central library for image and resource uploads. Search by filename and use the previous/next controls to browse large libraries. Supported uploads are JPG/JPEG, PNG, WEBP, PDF, DOCX, XLSX, and CSV; files are limited to 10 MB and images to 30 megapixels.
- Removing an image from an editor clears only that content reference. Replacing an image or clearing a field does not delete the library file, so media can be reused safely by multiple entries.
- Manage the conceptual homepage image under `/admin/home` > **Hero visual**. You can select an existing library image, upload a new one, set placement alt text or mark it decorative, and save it as a draft before publishing. The image is optional; existing home content stays text-only until you select and publish one.
- Save Draft stores editable changes without changing the public homepage. Publish atomically replaces the published snapshot. Archived, hidden, draft-only, and unavailable resources stay out of public output.
- Media uploads are limited to 10 MB and validated by actual file content. Supported images are JPG, PNG, and WEBP. Resource downloads are PDF, DOCX, XLSX, and CSV. SVG and executable files are rejected.
- The media directory is private. Public homepage images are served only when a published visible item references them. Available resource files are streamed through `/resources/<slug>/download`; uploads do not become public just because they exist.
- Image placements can override alt text or mark that placement decorative. The media library keeps a separate default alt value and decorative setting. Resource download files are selected from the existing file field and remain private until their resource is published as available.

The repository includes an optimized conceptual hero image at `public/images/hero-clarity-to-distinction.webp`. To use it, open `/admin/media` and upload that file, then select it under `/admin/home` > **Hero visual**. Give it descriptive alt text (for example, “Layered paper forms opening into an expressive shape”) or mark it decorative, then **Save draft** and **Publish**. The built-in image is not automatically attached or published. Clearing the Hero visual field removes the homepage reference; it does not delete the library asset. This content change needs no database migration.

## Database and migrations

The CMS uses the existing SQLAlchemy/PostgreSQL integration. Schema changes are versioned under `yhttp_ssr_boilerplate/dbmigration/` and applied with:

```sh
yhttp-ssr-boilerplate db migration upgrade
```

Do not run `db create` or `db drop` against an existing production database. Back up before deploying a schema migration.

## Production configuration

No hosting provider has been selected. The application remains host-neutral; production must provide persistent PostgreSQL, Redis, HTTPS, and a private S3-compatible bucket. Set `YHTTP_ENV=production`, `PUBLIC_URL` to the deployed HTTPS origin, `DATABASE_URL`, a random `YHTTP_AUTH_ACCESS_SECRET` of at least 32 characters, the admin credentials, and Redis connection settings. In production, media storage defaults to S3. Set `MEDIA_S3_BUCKET` and `MEDIA_S3_REGION`; set `MEDIA_S3_ENDPOINT` for a compatible non-AWS endpoint. Provide credentials through the platform secret manager or workload identity, not source files. The bucket should remain private because the app enforces publication checks before serving media.

For local development, `MEDIA_STORAGE_BACKEND=local` stores bytes beneath `MEDIA_STORAGE_DIR` (default `.var/media-private`). This directory persists across local application restarts but is not assumed to persist on a deployment host. Configure S3-compatible storage before accepting production uploads.

Admin access uses one administrator configured through environment credentials, not a database password record. To change or recover access, update the username/password in the deployment secret store and restart the app. Rotate `YHTTP_AUTH_ACCESS_SECRET` to invalidate all existing admin sessions; administrators will need to sign in again. There is no public registration or default login.

## Backups and restoration

- Back up PostgreSQL regularly with `pg_dump -Fc "$DATABASE_URL" > cms-backup.dump` and store the backup outside the application host.
- For local development, back up the media directory separately, for example with `tar -czf media-backup.tar.gz "$MEDIA_STORAGE_DIR"`. For S3-compatible storage, use the provider’s versioning or backup feature and include the bucket in the recovery plan.
- To restore, provision PostgreSQL and the media bucket/directory first, restore the database with `pg_restore --clean --if-exists -d "$DATABASE_URL" cms-backup.dump`, then restore the matching media backup. Keep the database and media backups from the same recovery point so references still resolve.

## Checks

```sh
make www-lint
make www-dist
make cover
```

The first two check and build the frontend. `make cover` runs the Python test suite and coverage report.
