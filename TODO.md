## task1
- create a yhttp ssr boilerplate project using yttp-skill.
- take a look at ../reelio to know how to create the project.
- import everything from the reelio project such as:
  - Makefile
  - www directory
  - setup.py
  - vite config
- Create a simple master.mako and index.mako
- create the tests directory just like the ../reelio/tests
- make 100% codex coverae
- use:
  - yhttp-sqlalchemy
  - yhttp-dbmanager
  and all other extensions in setup.py

## Phase 4 — Admin UX & Media Library Integration

Status: Implemented; interactive browser verification remains incomplete

### Objective

Improve the usability of the existing custom admin CMS and connect
every public content image slot to the existing Media Library.

Implement the changes, not just an audit or proposal.

### Context

- The Media Library already exists.
- Content editors currently lack library selection, image upload,
  replacement, and removal controls.
- Admin headings, labels, helper text, and inputs are visually too
  similar, making sections difficult to understand.
- Preserve the fixed-schema CMS and the public site's existing design.
- Use Roboto and Tailwind CSS v4.
- Brand palette:
  `#384661`, `#8491AF`, `#1E6F79`, `#F5DEA2`, `#153A42`.
- SEO and drag-and-drop page building are outside this phase.

### Existing fixes that must remain intact

- `admin_field.mako` declares its include arguments:
  `<%page args="field, form_id, csrf" />`.
- Request-specific CSRF values must not be overwritten by Mako globals.
- Routes supply valid session-bound CSRF values.
- Authentication, CSRF validation, escaping, and draft/publish behavior
  must remain functional.

### 1. Inspect the current implementation

- [x] Inspect admin routes, templates, field builders, content schemas,
      media storage, upload validation, and public image rendering.
- [x] Identify all public content image slots and their corresponding
      admin editors, including hardcoded content images.
- [x] Distinguish editable content images from decorative icons,
      textures, and background assets.
- [x] Reuse existing infrastructure rather than introducing a parallel
      media system.
- [x] Proceed with implementation after inspection.

### 2. Improve the Media Library

- [x] Keep Media Library clearly accessible from admin navigation.
- [x] Provide a prominent “Upload image” action.
- [x] Display thumbnails, filenames, and useful available metadata.
- [x] Support filename search.
- [x] Provide loading, empty, success, and error states.
- [x] Display supported formats and size limits matching actual
      server-side validation.
- [x] Use pagination or another bounded loading strategy where needed.

### 3. Build a reusable image-field control

Every content image slot must expose:

- [x] A descriptive label.
- [x] Current image preview or a clear empty state.
- [x] “Choose from Media Library”.
- [x] “Upload new image”.
- [x] “Remove from this section”.
- [x] Placement guidance where helpful.

Implementation requirements:

- [x] Do not require manually entered file paths, URLs, or media IDs.
- [x] Use the existing media-reference model; prefer stable IDs where
      supported while preserving compatibility with existing content.
- [x] Connect all existing content image slots to their corresponding
      admin sections.
- [x] For hardcoded content images, add only the minimal schema and
      template changes necessary to make them editable.
- [x] Preserve existing images, records, and public layouts.
- [x] Do not invent public sections or unnecessary image slots.
- [x] Document intentionally excluded decorative assets.

### 4. Implement an accessible media picker

- [x] Show thumbnails and filenames.
- [x] Support filename search.
- [x] Clearly indicate the selected image.
- [x] Provide explicit Select and Cancel actions.
- [x] Cancel must leave the original field value unchanged.
- [x] Handle loading, empty results, and request failures.
- [x] Support mobile layouts and keyboard navigation.
- [x] If using a modal, provide an accessible dialog name, focus
      management, Escape-to-close, and focus restoration.
- [x] Opening or using the picker must preserve other unsaved fields.

### 5. Support uploads inside editors

- [x] Reuse the existing authenticated, validated upload endpoint.
- [x] Add the uploaded image to the Media Library.
- [x] Select it for the active field after upload succeeds.
- [x] Update the preview without discarding other unsaved form values.
- [x] Show a busy state and useful errors.
- [x] Show percentage progress only if it is actually measurable.
- [x] Include required CSRF protection.
- [x] Avoid nested HTML forms.
- [x] If editing is cancelled after upload, the uploaded file may remain
      in the library; do not silently delete reusable media.

### 6. Preserve removal and publication semantics

- [x] Removing an image from a section clears its reference only.
- [x] Replacing an image does not delete the previous media file.
- [x] One media item can be reused across multiple sections.
- [x] Clearing one reference does not break other references.
- [x] Optional empty image slots render appropriately.
- [x] Required image slots have clear guidance and server validation.
- [x] Selecting, uploading, replacing, or removing an image does not
      automatically publish a content change.
- [x] Save Draft persists the draft selection without changing the
      public site's published image.
- [x] Publish applies the intended content and image references.
- [x] Reloading the editor restores the saved draft selection.
- [ ] Saved references and uploaded files persist across app restarts.
- [x] Draft-only media remains protected.
- [x] Authorized admins can preview draft media.
- [x] Published media remains accessible where required.
- [x] Do not expose the whole library or private storage publicly.
- [x] Do not introduce permanent media deletion in this phase.

### 7. Improve admin typography and layout

- [x] Keep Roboto, but distinguish page titles, section headings,
      labels, values, help text, errors, and status badges through
      size, weight, spacing, and contrast.
- [x] Group related fields in clearly separated cards or fieldsets.
- [x] Give sections descriptive headings and short explanations
      where useful.
- [x] Make repeated entries distinguishable using actual content
      titles or meaningful fallback labels.
- [x] Use consistent spacing and restrained surface/border contrast.
- [x] Avoid long, undifferentiated walls of inputs.
- [x] Keep the admin language consistent with the existing app.

### 8. Improve field guidance and navigation

- [x] Use human-readable labels, not raw schema keys.
- [x] Keep labels visible; placeholders must not replace them.
- [x] Mark required/optional fields according to actual backend rules.
- [x] Add concise helper text and examples where needed.
- [x] Display real length limits where applicable.
- [x] Associate help text and validation errors with their inputs.
- [x] Show field errors near the affected controls.
- [x] Preserve entered values when validation fails.
- [x] Make the active navigation section obvious.
- [x] Keep all existing admin sections accessible.
- [x] Provide usable mobile navigation.

### 9. Clarify save, publish, and content state

- [x] Visually distinguish Save Draft and Publish.
- [x] Explain that Save Draft does not update the public site.
- [x] Explain that Publish makes the relevant changes public.
- [x] Provide a consistent action area.
- [x] If actions are sticky, ensure they do not obscure content or focus.
- [x] Show accurate draft/published and pending-change states based
      on actual data.
- [x] Detect unsaved text and image changes.
- [x] Warn before leaving with unsaved changes where appropriate.
- [x] Do not interfere with saving, publishing, or picker interactions.
- [x] Show success only after server confirmation.
- [x] Do not invent timestamps or publication status.

### 10. Accessibility and responsive behavior

- [x] Use semantic headings, labels, fieldsets, buttons, and dialogs.
- [x] Provide visible keyboard focus and readable contrast.
- [x] Do not communicate status using color alone.
- [x] Ensure desktop and mobile layouts avoid horizontal overflow.
- [x] Respect reduced-motion preferences if animation is introduced.
- [x] Prioritize usability over decorative styling.

### 11. Security and data safety

- [x] Preserve authentication and authorization on admin/media routes.
- [x] Keep CSRF validation on all state-changing requests.
- [x] Preserve server-side upload type and size validation.
- [x] Do not trust client-provided filenames or filesystem paths.
- [x] Preserve private-media access controls.
- [x] Do not log or expose credentials, signing secrets, or tokens.
- [x] Do not reintroduce request-specific data into Mako globals.
- [x] Do not hide errors using dummy tokens or fallback content.
- [x] Do not reset the database, delete content, or overwrite edits.
- [x] Do not rotate credentials or signing secrets.
- [x] If schema changes are needed, use backward-compatible migrations
      following the project's conventions.
- [x] Do not commit or push.

### 12. Regression tests and verification

Keep existing Mako include, escaping, authentication, and CSRF tests
passing. Add appropriate coverage for:

- [x] Rendering every editor section and the Media Library.
- [ ] Restoring each image field's current reference.
- [ ] Selecting an existing image.
- [ ] Uploading and selecting a replacement.
- [ ] Cancelling selection without changing the field.
- [x] Clearing a reference without deleting the media file.
- [ ] Reusing media across multiple sections.
- [x] Saving image drafts without changing published content.
- [x] Publishing image changes.
- [x] Persistence after reload.
- [x] Rejection of invalid uploads.
- [x] Rejection of missing or invalid CSRF tokens.
- [x] Unauthorized access to protected media being denied.

Run available checks:

- [x] Backend tests.
- [x] Mako template compilation.
- [x] Python compilation/checks.
- [ ] Frontend lint.
- [x] Frontend production build.
- [ ] Browser checks of editor/picker interactions at desktop and
      mobile widths, if browser tooling is available.

Clearly distinguish database-independent tests, SQLite tests,
mocked Redis checks, live PostgreSQL/Redis tests, and actual browser
verification.

Do not claim template-rendering tests prove interactive UI behavior.
Document unavailable infrastructure and unperformed checks.

Verification notes:

- `make cover`: 42 tests passed using the project's local PostgreSQL test fixture; admin tests mock the Redis blacklist check. No live Redis service was exercised.
- All eight Mako templates compiled, including editor rendering through `admin_field.mako`.
- `python -m compileall -q yhttp_ssr_boilerplate tests` passed.
- `pnpm run build` passed. `eslint .` and focused Prettier checks passed; full `pnpm run lint` stops on pre-existing formatting in `TODO.md`.
- `make lint` remains failing because flake8 reports line-length violations across the CMS and test code, including pre-existing project files.
- Browser checks were not run because browser automation tooling is unavailable. Automated template tests do not verify dialog focus, Escape handling, cancellation, or mobile layout in a real browser.
- Public image slots mapped: agency logo in Settings, portfolio cover in Portfolio, and resource cover in Resources. Portfolio fallback illustrations remain replaceable through their existing cover fields. The code-drawn hero composition and decorative section/service icons are excluded as brand artwork; no other public image slot was found.
- No schema changes were required, so no migration is needed.

### Acceptance criteria

- Every public content image has an editor control, except explicitly
  documented decorative exclusions.
- Users can upload once and reuse a library image in multiple sections.
- Users can choose, replace, and remove section images without
  manually entering paths or losing other edits.
- Draft image changes do not affect the public site until Publish.
- Admin sections, headings, labels, guidance, and actions are clearly
  distinguishable.
- Authentication, CSRF, private media, and existing content are preserved.

### Completion report

When finished:

1. Summarize implemented UX and media improvements.
2. Explain the cause of the missing editor/library integration.
3. List changed files.
4. Map public content image slots to their admin editors.
5. Explain how to upload, choose, replace, remove, save, and publish.
6. Report tests/builds and their actual results.
7. Document required migrations or restart steps.
8. List limitations and intentionally excluded decorative assets.
9. Update this checklist honestly: leave incomplete items unchecked
   and identify checks blocked by the environment.
