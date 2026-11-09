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

# task2 — Design and Build the Homepage

## Goal
Build a minimal, aesthetic, premium homepage for a creative
marketing agency based in Oman.

The agency offers marketing strategy, digital content,
photography, video production, and AI-powered creative production.

The website also provides free marketing tools that help
business owners improve their marketing independently.

Build only the homepage in this phase.
Do not build additional pages yet.

## Step 1 — Review the Project
- Inspect the existing project and use its current framework.
- Reuse existing components where appropriate.
- Do not replace the tech stack unnecessarily.
- If no project exists, use Next.js with Tailwind CSS v4.
- Use Tailwind CSS v4 explicitly, not v3.
- Follow the v4 setup for Next.js using @tailwindcss/postcss
  and @import "tailwindcss"; in the global stylesheet.
- Use Tailwind v4's CSS-first configuration and define the
  supplied color palette and Roboto font tokens with @theme.
- Do not use legacy v3 setup patterns such as
  @tailwind base, @tailwind components, or @tailwind utilities.
- Keep the implementation simple and maintainable.

## Step 2 — Define the Visual System

Use these exact colors as global design tokens:

--color-1: #384661;
--color-2: #8491AF;
--color-3: #1E6F79;
--color-4: #F5DEA2;
--color-5: #153A42;

Suggested roles:
- Main background: color-5
- Secondary surfaces: color-1
- Primary text on dark backgrounds: color-4
- Secondary text: color-2, only where contrast is sufficient
- Accent surfaces and details: color-3
- Primary button: color-4 background with color-5 text

Use this palette consistently across the entire site.
Do not introduce unrelated colors.
Check text and button contrast; adjust pairings where necessary.

Typography:
- Use Roboto throughout the website.
- Use weights 300, 400, 500, and 700 selectively.
- Use large, elegant headings and comfortable body text.
- Avoid overly thin body text or excessive letter spacing.

Art direction:
- Minimal, editorial, refined, and quietly luxurious.
- Generous whitespace and a clear visual hierarchy.
- Restrained borders and subtle corner rounding.
- Mostly flat surfaces with minimal shadows.
- Premium through typography, spacing, and composition,
  not through excessive decoration.

Avoid:
- Neon effects
- Heavy gradients
- Glassmorphism
- Excessively rounded cards
- Busy backgrounds
- Generic startup-style illustrations
- Excessive animations

## Step 3 — Build the Header and Navigation

Use a temporary text wordmark: [Agency Name].
Keep the name easy to replace in one central configuration.

Desktop navigation:
1. Home
2. Free Tools
3. Services & Work
4. Contact

Style Contact as a restrained call-to-action.

For this homepage-only phase:
- Home links to the top of the page.
- Free Tools links to #free-tools.
- Services & Work links to #services-work.
- Contact links to #contact.

Do not create empty pages or broken navigation links.
Keep navigation configurable for future page routes.

On mobile:
- Use an accessible menu button.
- Support keyboard navigation and Escape to close.
- Close the menu after selecting a link.
- Avoid horizontal overflow.

## Step 4 — Build the Hero Section

Use English copy.

Eyebrow:
“Creative Marketing Agency · Oman”

Headline:
“Clear strategy. Distinctive content.”

Description:
“We help businesses in Oman turn ideas into thoughtful
marketing, compelling content, and distinctive visual experiences.”

Primary CTA:
“Explore Our Services”
Links to #services-work.

Secondary CTA:
“Explore Free Tools”
Links to #free-tools.

Design:
- Use a strong typographic composition.
- Keep the headline as the main visual focus.
- Use generous spacing and restrained supporting details.
- A subtle abstract composition using the brand palette is optional.
- Do not depend on stock photography or an autoplay video.
- Do not add fake client logos, statistics, or awards.

## Step 5 — Add the Services & Work Preview

Section ID: services-work

Heading:
“Strategy meets creative execution.”

Present three concise service groups:

1. Marketing Strategy
   “Clear direction for your brand, content, and campaigns.”

2. Content & Production
   “Photography, video, and digital content crafted around
   your business.”

3. AI Creative Production
   “Concept-led visuals and videos using AI as a creative tool.”

Use a clean editorial layout rather than a crowded card grid.

Below the services, add a small selected-work preview:
- Show no more than two sample project layouts.
- Label each clearly as “Concept Preview”.
- Use palette-based visual placeholders.
- Do not invent clients, testimonials, or performance results.
- Keep project titles and media easy to replace.
- Do not make placeholders look like clickable case studies.

## Step 6 — Add the Free Tools Preview

Section ID: free-tools

Heading:
“Practical tools. A clearer next step.”

Description:
“Simple resources to help you plan your marketing,
organize your content, and move forward independently.”

Show three resource previews:
1. One-Page Marketing Plan
2. 30-Day Content Calendar
3. Mobile Video Checklist

Each preview should include:
- Tool name
- One short explanation
- A small “Coming soon” label

Do not create fake download buttons.
Actual files and tool functionality will be added in a later phase.

Keep this section visually distinct but consistent with the palette.

## Step 7 — Add a Brief About Section

Keep the introduction on the homepage.
Do not create a separate About page.

Heading:
“A thoughtful approach to brand growth.”

Suggested copy:
“Based in Oman, we bring marketing thinking and creative
production together to help businesses communicate clearly
and show up with purpose.”

Use a compact, typography-led layout.
Do not invent years of experience, team size, or credentials.

## Step 8 — Add the Contact Section and Footer

Section ID: contact

Heading:
“Let’s create your next move.”

Supporting copy:
“Tell us what you’re building and where you need support.”

Include configurable fields for:
- Business email
- WhatsApp URL

If real contact details are not available:
- Show clearly marked placeholders during development.
- Do not generate fake contact details.
- Do not render active buttons with invalid destinations.

Do not build a contact form or backend in this phase.

Footer:
- Agency wordmark
- Short positioning statement
- Navigation links to the homepage sections
- Copyright with the current year

Only show social links if real URLs are provided.

## Step 9 — Make It Responsive and Accessible

- Design for mobile, tablet, and desktop.
- Use fluid typography and a consistent content width.
- Maintain comfortable spacing on small screens.
- Use semantic HTML and a single H1.
- Provide visible keyboard focus states.
- Ensure readable color contrast.
- Use sufficiently large touch targets.
- Respect prefers-reduced-motion.
- Keep hover effects and transitions subtle.
- Optimize font loading and avoid unnecessary dependencies.

## Step 10 — Verify Before Finishing

Confirm that:
- Only the homepage has been built.
- All four navigation items work.
- The mobile menu is accessible.
- No links lead to missing pages.
- There are no fake downloads or fabricated claims.
- Roboto is used consistently.
- The supplied palette is applied throughout.
- The layout has no horizontal overflow.
- Available lint and build checks pass.

Report:
1. What was implemented.
2. Which checks were run.
3. Which placeholders still need real content.

Stop after completing Phase 1.
Do not build other pages or add unrequested features.

# Phase 2 — Refine Services and Background Details

## Goal
Update the existing homepage services section and add subtle,
creative background elements.

Preserve the existing layout, navigation, Roboto typography,
brand palette, and Tailwind CSS v4 setup.
Do not rebuild the homepage or create additional pages.

## Step 1 — Update the Services Section

Use this section heading:
“From clear direction to creative execution.”

Supporting text:
“Strategy, content, social media, and campaigns — working
together for your brand.”

Replace the existing service groups with these four services:

### 1. Direction
Subtitle: Marketing & Brand Strategy
Description:
“We define your audience, sharpen your message, and build
practical marketing plans that give your brand a clear
direction — from positioning to campaign planning.”
Icon: Compass

### 2. Creation
Subtitle: Content & Visual Production
Description:
“We turn ideas into photography, video, social content,
and AI-powered visuals — bringing your brand’s personality
and message to life through thoughtful creative production.”
Icon: Clapperboard

### 3. Presence
Subtitle: Social Media Management
Description:
“We plan, create, and publish consistent social content,
keeping your brand’s voice cohesive and using performance
insights to refine its presence over time.”
Icon: MessageCircle

### 4. Growth
Subtitle: Digital Marketing & Campaigns
Description:
“We plan and manage digital campaigns that connect your
brand with relevant audiences, then measure and refine
performance to encourage meaningful enquiries and action.”
Icon: TrendingUp

## Step 2 — Refine the Services Layout

- Use four spacious editorial rows instead of a crowded card grid.
- On desktop, place the icon and service title on the left,
  with the description beside them on the right.
- Keep the descriptive subtitle directly below each service title.
- On mobile, stack the description below the title.
- Use subtle separators and generous spacing.

Typography:
- Make service titles visibly larger than the current version.
- Target approximately 30–40px on desktop and 26–32px on mobile.
- Use Roboto Medium for titles.
- Keep subtitles clear and readable at approximately 16–18px.
- Use approximately 17–18px body text with relaxed line height.
- Avoid oversized text that disrupts the page hierarchy.

Icons:
- Use consistent, minimal outline icons.
- Reuse the existing icon library if available.
- Otherwise, use lucide-react.
- Use approximately 28–36px icons with consistent stroke widths.
- Use the existing brand palette for service icons.
- Treat icons as decorative when the adjacent text gives their meaning.

Preserve the selected-work preview and existing section anchor links.

## Step 3 — Add Creative Background Elements

The current background feels too flat and uniform.
Add subtle visual details across the homepage without making it busy.

Create a reusable decorative background layer using small
outline icons related to the agency’s work, such as:
- Camera
- Video
- Clapperboard
- Megaphone
- PenTool
- Aperture
- Sparkles
- BarChart3
- MessageCircle

Visual treatment:
- Use white (#FFFFFF) ONLY as an additional decorative color.
- Keep each background icon at 10–20% opacity.
- Use thin, consistent outline strokes.
- Vary sizes subtly, approximately 20–48px.
- Use irregular spacing and slight rotations.
- Avoid an obvious grid or repeating wallpaper effect.
- Distribute them across the page, not only in the hero.
- Keep the overall effect sparse, refined, and understated.
- Position elements mainly in margins and open spaces.
- Do not place icons directly behind headings, paragraphs,
  buttons, or service content.

Implementation:
- Use deterministic positions, not random values generated on render.
- Use a small curated set of elements rather than hundreds of nodes.
- Anchor decorations to sections so they remain well positioned
  as the page height and viewport change.
- Keep decorative layers behind content and above background surfaces.
- Apply pointer-events: none and aria-hidden="true".
- Ensure decorations never block clicks or keyboard interaction.
- Reduce their number and size on mobile.
- Prevent horizontal overflow.
- Do not introduce parallax, continuous motion, or heavy animation.

## Step 4 — Verify

- Confirm all four services display correctly.
- Check desktop and mobile layouts.
- Confirm descriptions sit beside titles on desktop
  and below them on mobile.
- Ensure background decorations are visible but unobtrusive.
- Confirm navigation, links, and existing content still work.
- Keep the site minimal, premium, and readable.
- Run the available lint and production build checks.
- Report any checks that could not be run.

Complete only Phase 2.
Do not add pages, backend features, or unrelated changes.


# Phase 3 — Build a Custom Admin Panel and CMS

## Goal

Build a functional, secure, custom admin panel inside the
existing website project.

The site owner must be able to edit website text, manage
images, update services, manage portfolio items, and upload
free resources without editing code.

This must be a real CMS with persistent storage, not a UI demo.

Do not integrate a ready-made CMS such as Sanity, Payload,
Strapi, or WordPress.

Use established libraries for authentication, database access,
validation, and file storage where appropriate.
Do not invent custom authentication or cryptography.

SEO analysis and SEO editing features are out of scope
for this phase.

## Step 1 — Inspect and Plan

Inspect:
- The existing framework and project structure.
- The current homepage and its content.
- Existing dependencies.
- Any existing database, authentication, or storage setup.
- Deployment configuration, if available.

Preserve:
- The public website design and navigation.
- Roboto typography.
- The existing brand palette.
- Tailwind CSS v4.
- The decorative background elements.
- Existing public URLs and section anchors.

Before implementation, identify the database and file-storage
requirements for the intended deployment.

If the hosting environment is unknown and this affects the
architecture, ask the owner to confirm it before proceeding.
Group essential questions into one concise message.

Do not silently assume that local filesystem uploads will
persist in production.

Preferred defaults when compatible with deployment:
- PostgreSQL for content.
- Prisma for database access and migrations.
- S3-compatible object storage for uploaded files.

Reuse suitable existing infrastructure instead of replacing it.

External database or storage services are acceptable infrastructure;
they must not replace the custom admin panel.

## Step 2 — Create the Admin Routes

Create these protected admin sections:

- /admin
- /admin/home
- /admin/services
- /admin/portfolio
- /admin/resources
- /admin/media
- /admin/settings

Create:
- /admin/login

Use a shared admin layout with:
- Sidebar navigation.
- Clear page titles.
- Save and publish controls where applicable.
- Success and error messages.
- Logout.
- A link to view the public website.

Do not create additional public-facing pages in this phase.

## Step 3 — Implement Secure Authentication

Requirements:
- Single administrator role for the initial version.
- No public registration.
- No default or hardcoded credentials.
- Provide a documented, secure process to create the first admin.
- Use a maintained authentication library compatible with the project.
- If passwords are stored, use established secure password hashing.
- Use secure session handling and appropriate cookie settings.
- Protect login attempts with deployment-appropriate rate limiting.
- Follow the authentication library's CSRF protection practices.

Enforce authentication and authorization on the server for:
- Every admin page.
- Every content read intended only for admins.
- Every create, update, delete, publish, and upload operation.

Hiding links or redirecting in the browser is not sufficient.

Never expose database credentials, session secrets,
or storage write credentials to client-side code.

Exclude admin pages from indexing, but do not treat
robots directives as access control.

## Step 4 — Design the Content Models

Create typed, validated models for the following.

### A. Homepage Content

Editable fields:
- Hero eyebrow.
- Hero headline.
- Hero description.
- Primary CTA label and destination.
- Secondary CTA label and destination.
- Services section heading and introduction.
- Portfolio section heading and introduction.
- Free tools section heading and introduction.
- About heading and description.
- Contact heading and supporting text.

The layout and typography remain controlled by code.
Do not build a drag-and-drop page builder.

### B. Services

Fields:
- ID.
- Title.
- Subtitle.
- Description.
- Icon key.
- Display order.
- Visibility.
- Publication state.

Features:
- Add, edit, archive, and reorder services.
- Select an icon from a curated list of existing icons.
- Do not accept executable code or arbitrary SVG markup as icons.

### C. Portfolio Items

Fields:
- ID.
- Title.
- Short description.
- Category or service type.
- Cover image.
- Optional additional images.
- Project type: client work or concept.
- Display order.
- Featured status.
- Visibility.
- Publication state.

Features:
- Add, edit, archive, and reorder items.
- Clearly label concept projects on the public website.
- Keep the current homepage preview layout.
- Do not create public case-study pages in this phase.

### D. Free Resources

Fields:
- ID.
- Title.
- Short description.
- Resource category.
- Resource format.
- Optional cover image.
- Download file or approved external resource URL.
- Availability: coming soon or available.
- Display order.
- Visibility.
- Publication state.

Features:
- Add, edit, archive, and reorder resources.
- Show a working download or resource link only when available.
- Require a valid file or URL before publishing as available.
- Do not create fake downloads.

### E. General Settings

Fields:
- Agency name.
- Logo.
- Short agency description.
- Business email.
- WhatsApp destination.
- Social media URLs.
- Footer text.

Do not expose editable application secrets in this section.

### F. Media Assets

Store:
- Asset ID.
- Storage key.
- Original filename.
- Validated MIME type.
- File size.
- Image dimensions where applicable.
- Default alt text.
- Created timestamp.

Allow an alt-text override for each image placement,
since the same image may be used in different contexts.

Allow images to be explicitly marked decorative.

Alt-text fields are a basic accessibility requirement,
not an SEO analysis feature.

## Step 5 — Implement Persistent Content Storage

- Store content in the database.
- Store uploaded file bytes in persistent file/object storage.
- Store file references and metadata in the database.
- Do not use localStorage as the CMS database.
- Do not edit source files to save content.
- Do not rely on an ephemeral deployment filesystem.

Provide:
- Database schema.
- Versioned migrations.
- Safe initialization instructions.
- An idempotent seed/import script for existing content.

Migrate the current website content into the CMS without
overwriting future admin edits when the seed is run again.

Do not invent client projects, results, testimonials,
or contact details.

## Step 6 — Implement Media Management

Build a reusable media picker that supports:
- Uploading images.
- Viewing existing assets.
- Selecting an asset for a content field.
- Replacing an image.
- Editing default alt text.
- Showing file size and dimensions.
- Deleting unused assets with confirmation.

Validate uploads on the server:
- Use an explicit allowlist of supported formats.
- Validate actual file content where feasible,
  not only filename extensions.
- Enforce documented file-size limits.
- Use safe generated storage keys.
- Reject executable files and unsafe formats.
- Do not allow unsanitized SVG uploads.

For the initial resource library, support a narrow,
documented list of required download formats.
Do not accept arbitrary file types.

Prevent deletion of assets still referenced by draft
or published content, or require reassignment first.

Draft/private files must not become publicly accessible
merely because they were uploaded.
Use authenticated access or short-lived signed URLs
where appropriate.

Explain how published downloadable files become accessible.

## Step 7 — Add Draft and Publish Behavior

Provide a clear workflow:
- Edit.
- Save Draft.
- Publish.

Saving a draft must not change the live website.

Persist the last published version separately from
in-progress changes.

Publishing must:
- Validate the content.
- Update the published version atomically.
- Refresh the relevant public page cache.
- Show a success message only after the operation succeeds.

Also support:
- Clear draft/published status.
- Last updated and last published timestamps.
- Confirmation before destructive actions.
- An unsaved-changes warning when leaving an edited form.

Archived or unpublished items must not appear publicly.

Apply a coherent draft/publish model to homepage content,
settings, services, portfolio, and resources.

Public queries must only return published content.
Do not expose drafts through public API responses.

A visual live-preview system is not required in this phase.

## Step 8 — Connect the Public Website to the CMS

Replace hardcoded editable content with database-backed content.

Keep the existing visual design and responsive layout.
Public pages must not depend on an admin login.

Use appropriate server-side data loading.
Ensure newly published changes appear without redeploying.

Handle:
- Empty sections.
- Missing optional images.
- Unavailable resources.
- Missing contact information.
- Database or storage failures.

Do not display broken links or fake contact actions.

Use appropriate caching and publication-triggered invalidation.
Do not cache private admin responses as public content.

Use a narrow formatting model:
- Plain text by default.
- Structured fields where needed.
- No arbitrary HTML or script injection.

Validate link schemes and destinations.
Disallow javascript: and other unsafe URLs.

## Step 9 — Design the Admin Interface

The admin UI should feel related to the public website
but prioritize clarity and usability.

Use:
- Roboto.
- Tailwind CSS v4.
- The existing brand palette.
- Accessible contrast.
- Clear labels and short help text.
- Comfortable form spacing.
- Consistent buttons and icons.

The public site's decorative background is not required
inside the admin interface.

Provide:
- Loading states.
- Empty states.
- Inline validation.
- Useful error messages.
- Disabled submission buttons while requests are processing.
- Responsive layouts.
- Keyboard-accessible controls.

Use simple move-up/move-down controls for ordering if
drag-and-drop would add unnecessary complexity.

Dashboard:
- Links to content sections.
- Real counts of content items.
- Draft/published summaries where useful.

Do not add fake analytics or fabricated traffic statistics.

## Step 10 — Test the Complete Workflow

Add automated tests where practical and perform the
available integration checks.

Verify:
1. Unauthenticated users cannot access admin content.
2. Unauthenticated write and upload requests are rejected.
3. Admin login and logout work.
4. Content persists across application restarts.
5. Draft edits do not change the public website.
6. Publishing updates the website without a redeploy.
7. Uploaded images display correctly.
8. Invalid and oversized uploads are rejected.
9. Referenced media cannot be accidentally deleted.
10. Available resources have working download links.
11. Archived/unpublished items disappear after publication.
12. Unsafe input and URLs are rejected or safely handled.
13. Existing homepage navigation still works.
14. Mobile admin layouts remain usable.

Run available:
- Lint checks.
- Type checks.
- Automated tests.
- Production build.

Do not claim a check passed unless it was actually run.
Clearly report any environment-dependent checks that
could not be completed.

## Step 11 — Document Setup and Operations

Create or update project documentation covering:
- Required environment variables in .env.example.
- Local development setup.
- Database setup and migrations.
- File-storage setup.
- Initial administrator creation.
- How to change or recover admin access securely.
- How to edit and publish content.
- Deployment-specific requirements.
- Database and file backup procedures.
- Basic restoration steps.

Never put real secrets in .env.example or commit them.

If infrastructure credentials are missing:
- Complete what can safely be implemented.
- Clearly explain the remaining setup.
- Do not substitute fake persistence or pretend deployment
  is complete.

## Out of Scope

Do not implement:
- SEO scoring or content analysis.
- SEO title/meta-description editing.
- AI-generated content.
- Public registration.
- Multiple admin roles.
- A page builder.
- Payments.
- Additional public pages.
- Unrequested analytics.

## Completion Report

Summarize:
1. What was implemented.
2. Architecture and dependencies used.
3. Required owner setup.
4. Checks run and their results.
5. Remaining limitations or blockers.

Do not commit or push unless explicitly requested.


## Phase 4 — Admin UX & Media Library Integration

Status: Not started

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
  `<%page args="field, form_id" />`.
- Request-specific CSRF values must not be overwritten by Mako globals.
- Routes supply valid session-bound CSRF values.
- Authentication, CSRF validation, escaping, and draft/publish behavior
  must remain functional.

### 1. Inspect the current implementation

- [ ] Inspect admin routes, templates, field builders, content schemas,
      media storage, upload validation, and public image rendering.
- [ ] Identify all public content image slots and their corresponding
      admin editors, including hardcoded content images.
- [ ] Distinguish editable content images from decorative icons,
      textures, and background assets.
- [ ] Reuse existing infrastructure rather than introducing a parallel
      media system.
- [ ] Proceed with implementation after inspection.

### 2. Improve the Media Library

- [ ] Keep Media Library clearly accessible from admin navigation.
- [ ] Provide a prominent “Upload image” action.
- [ ] Display thumbnails, filenames, and useful available metadata.
- [ ] Support filename search.
- [ ] Provide loading, empty, success, and error states.
- [ ] Display supported formats and size limits matching actual
      server-side validation.
- [ ] Use pagination or another bounded loading strategy where needed.

### 3. Build a reusable image-field control

Every content image slot must expose:

- [ ] A descriptive label.
- [ ] Current image preview or a clear empty state.
- [ ] “Choose from Media Library”.
- [ ] “Upload new image”.
- [ ] “Remove from this section”.
- [ ] Placement guidance where helpful.

Implementation requirements:

- [ ] Do not require manually entered file paths, URLs, or media IDs.
- [ ] Use the existing media-reference model; prefer stable IDs where
      supported while preserving compatibility with existing content.
- [ ] Connect all existing content image slots to their corresponding
      admin sections.
- [ ] For hardcoded content images, add only the minimal schema and
      template changes necessary to make them editable.
- [ ] Preserve existing images, records, and public layouts.
- [ ] Do not invent public sections or unnecessary image slots.
- [ ] Document intentionally excluded decorative assets.

### 4. Implement an accessible media picker

- [ ] Show thumbnails and filenames.
- [ ] Support filename search.
- [ ] Clearly indicate the selected image.
- [ ] Provide explicit Select and Cancel actions.
- [ ] Cancel must leave the original field value unchanged.
- [ ] Handle loading, empty results, and request failures.
- [ ] Support mobile layouts and keyboard navigation.
- [ ] If using a modal, provide an accessible dialog name, focus
      management, Escape-to-close, and focus restoration.
- [ ] Opening or using the picker must preserve other unsaved fields.

### 5. Support uploads inside editors

- [ ] Reuse the existing authenticated, validated upload endpoint.
- [ ] Add the uploaded image to the Media Library.
- [ ] Select it for the active field after upload succeeds.
- [ ] Update the preview without discarding other unsaved form values.
- [ ] Show a busy state and useful errors.
- [ ] Show percentage progress only if it is actually measurable.
- [ ] Include required CSRF protection.
- [ ] Avoid nested HTML forms.
- [ ] If editing is cancelled after upload, the uploaded file may remain
      in the library; do not silently delete reusable media.

### 6. Preserve removal and publication semantics

- [ ] Removing an image from a section clears its reference only.
- [ ] Replacing an image does not delete the previous media file.
- [ ] One media item can be reused across multiple sections.
- [ ] Clearing one reference does not break other references.
- [ ] Optional empty image slots render appropriately.
- [ ] Required image slots have clear guidance and server validation.
- [ ] Selecting, uploading, replacing, or removing an image does not
      automatically publish a content change.
- [ ] Save Draft persists the draft selection without changing the
      public site's published image.
- [ ] Publish applies the intended content and image references.
- [ ] Reloading the editor restores the saved draft selection.
- [ ] Saved references and uploaded files persist across app restarts.
- [ ] Draft-only media remains protected.
- [ ] Authorized admins can preview draft media.
- [ ] Published media remains accessible where required.
- [ ] Do not expose the whole library or private storage publicly.
- [ ] Do not introduce permanent media deletion in this phase.

### 7. Improve admin typography and layout

- [ ] Keep Roboto, but distinguish page titles, section headings,
      labels, values, help text, errors, and status badges through
      size, weight, spacing, and contrast.
- [ ] Group related fields in clearly separated cards or fieldsets.
- [ ] Give sections descriptive headings and short explanations
      where useful.
- [ ] Make repeated entries distinguishable using actual content
      titles or meaningful fallback labels.
- [ ] Use consistent spacing and restrained surface/border contrast.
- [ ] Avoid long, undifferentiated walls of inputs.
- [ ] Keep the admin language consistent with the existing app.

### 8. Improve field guidance and navigation

- [ ] Use human-readable labels, not raw schema keys.
- [ ] Keep labels visible; placeholders must not replace them.
- [ ] Mark required/optional fields according to actual backend rules.
- [ ] Add concise helper text and examples where needed.
- [ ] Display real length limits where applicable.
- [ ] Associate help text and validation errors with their inputs.
- [ ] Show field errors near the affected controls.
- [ ] Preserve entered values when validation fails.
- [ ] Make the active navigation section obvious.
- [ ] Keep all existing admin sections accessible.
- [ ] Provide usable mobile navigation.

### 9. Clarify save, publish, and content state

- [ ] Visually distinguish Save Draft and Publish.
- [ ] Explain that Save Draft does not update the public site.
- [ ] Explain that Publish makes the relevant changes public.
- [ ] Provide a consistent action area.
- [ ] If actions are sticky, ensure they do not obscure content or focus.
- [ ] Show accurate draft/published and pending-change states based
      on actual data.
- [ ] Detect unsaved text and image changes.
- [ ] Warn before leaving with unsaved changes where appropriate.
- [ ] Do not interfere with saving, publishing, or picker interactions.
- [ ] Show success only after server confirmation.
- [ ] Do not invent timestamps or publication status.

### 10. Accessibility and responsive behavior

- [ ] Use semantic headings, labels, fieldsets, buttons, and dialogs.
- [ ] Provide visible keyboard focus and readable contrast.
- [ ] Do not communicate status using color alone.
- [ ] Ensure desktop and mobile layouts avoid horizontal overflow.
- [ ] Respect reduced-motion preferences if animation is introduced.
- [ ] Prioritize usability over decorative styling.

### 11. Security and data safety

- [ ] Preserve authentication and authorization on admin/media routes.
- [ ] Keep CSRF validation on all state-changing requests.
- [ ] Preserve server-side upload type and size validation.
- [ ] Do not trust client-provided filenames or filesystem paths.
- [ ] Preserve private-media access controls.
- [ ] Do not log or expose credentials, signing secrets, or tokens.
- [ ] Do not reintroduce request-specific data into Mako globals.
- [ ] Do not hide errors using dummy tokens or fallback content.
- [ ] Do not reset the database, delete content, or overwrite edits.
- [ ] Do not rotate credentials or signing secrets.
- [ ] If schema changes are needed, use backward-compatible migrations
      following the project's conventions.
- [ ] Do not commit or push.

### 12. Regression tests and verification

Keep existing Mako include, escaping, authentication, and CSRF tests
passing. Add appropriate coverage for:

- [ ] Rendering every editor section and the Media Library.
- [ ] Restoring each image field's current reference.
- [ ] Selecting an existing image.
- [ ] Uploading and selecting a replacement.
- [ ] Cancelling selection without changing the field.
- [ ] Clearing a reference without deleting the media file.
- [ ] Reusing media across multiple sections.
- [ ] Saving image drafts without changing published content.
- [ ] Publishing image changes.
- [ ] Persistence after reload.
- [ ] Rejection of invalid uploads.
- [ ] Rejection of missing or invalid CSRF tokens.
- [ ] Unauthorized access to protected media being denied.

Run available checks:

- [ ] Backend tests.
- [ ] Mako template compilation.
- [ ] Python compilation/checks.
- [ ] Frontend lint.
- [ ] Frontend production build.
- [ ] Browser checks of editor/picker interactions at desktop and
      mobile widths, if browser tooling is available.

Clearly distinguish database-independent tests, SQLite tests,
mocked Redis checks, live PostgreSQL/Redis tests, and actual browser
verification.

Do not claim template-rendering tests prove interactive UI behavior.
Document unavailable infrastructure and unperformed checks.

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


## Phase 5 — Pure White Minimal Redesign

Status: Not started

### Objective

Redesign the public website and admin panel with pure white backgrounds
and a highly minimal visual style, without decorative graphics.

Implement the changes, not just an audit or design proposal.

### Design requirements

- Use #FFFFFF for page backgrounds and content surfaces.
- Do not substitute off-white, cream, light gray, or tinted white.
- Keep Roboto and the existing Tailwind CSS v4 setup.
- Use whitespace, typography, alignment, and subtle borders for structure.
- Remove decorative graphics, patterns, gradients, and ornamental effects.
- Preserve actual content images and functional interface elements.
- Keep brand colors only as restrained functional accents.
- Do not introduce a new UI framework.

### 1. Inspect existing layouts and styles

- [ ] Inspect shared public and admin layouts, templates, and styles.
- [ ] Identify background colors, gradients, textures, and patterns.
- [ ] Identify decorative graphics and pseudo-elements.
- [ ] Identify dark-mode rules that could override white backgrounds.
- [ ] Distinguish decorative assets from meaningful content images.
- [ ] Apply changes across all existing routes, not just the homepage.

### 2. Make the public website pure white

- [ ] Set body and main layout backgrounds to #FFFFFF.
- [ ] Make header, navigation, sections, and footer backgrounds white.
- [ ] Make cards, menus, dialogs, and content surfaces white.
- [ ] Remove colored section background bands.
- [ ] Remove background gradients, textures, and patterns.
- [ ] Remove decorative background images and overlays.
- [ ] Remove ornamental shapes, lines, and pseudo-elements.
- [ ] Remove unnecessary shadows and decorative visual effects.
- [ ] Do not replace removed graphics with new decorative artwork.
- [ ] Use whitespace and restrained neutral borders for separation.

### 3. Remove the Home hero's abstract composition

The current hero contains a CSS-generated decorative composition,
including classes such as:

- `hero-composition`
- `composition-frame`
- `composition-disc`
- `composition-arch`
- `composition-block`
- `composition-line`
- `composition-side-note`

Requirements:

- [ ] Remove this composition from the public layout.
- [ ] Remove its ornamental labels, numbering, and captions.
- [ ] Preserve the actual hero headline, description, and CTA actions.
- [ ] Rebalance the hero into a clean text-focused layout.
- [ ] Remove the unused visual column and any empty placeholder.
- [ ] Use appropriate text width and responsive spacing.
- [ ] Delete obsolete CSS or assets only if unused elsewhere.

Scope clarification:

The earlier request to add a replacement hero image field is deferred.
Do not implement a new hero-image field in this phase.
Do not delete any existing CMS fields, references, or media files.

### 4. Make the admin panel pure white

Use #FFFFFF backgrounds for:

- [ ] Admin login page.
- [ ] Admin body and main shell.
- [ ] Sidebar and top navigation.
- [ ] Main content area.
- [ ] Cards, field groups, and panels.
- [ ] Inputs, textareas, and selects.
- [ ] Tables and Media Library containers.
- [ ] Picker dialogs, menus, and modal content.

Maintain clear structure:

- [ ] Distinguish page titles, section headings, labels, and helper text.
- [ ] Use consistent spacing and alignment.
- [ ] Use subtle neutral borders where necessary.
- [ ] Keep active navigation clearly identifiable.
- [ ] Preserve visible focus states.
- [ ] Remove large shadows and decorative graphics.
- [ ] Remove unnecessary tinted panels and background blocks.

A restrained translucent backdrop is allowed behind a modal when
needed to distinguish it from the page. The dialog itself must be white.

### 5. Preserve content and functional visual elements

“No decorative graphics” does not mean removing useful content.

- [ ] Preserve the brand logo.
- [ ] Preserve actual portfolio and resource images.
- [ ] Preserve CMS-managed content images.
- [ ] Preserve Media Library thumbnails and image previews.
- [ ] Preserve functional search, close, upload, and navigation icons.
- [ ] Preserve loading indicators.
- [ ] Preserve validation messages and status information.
- [ ] Do not delete media files or database content.
- [ ] Do not remove existing image fields or references.
- [ ] If a background image carries meaningful content, preserve it
      through an appropriate inline presentation.
- [ ] Do not introduce illustrations or placeholder artwork.

### 6. Refine typography, buttons, and states

- [ ] Keep Roboto.
- [ ] Use dark, readable text on white.
- [ ] Use accessible secondary-text colors.
- [ ] Keep brand colors limited to functional accents.
- [ ] Avoid large brand-colored surfaces.
- [ ] Primary buttons may retain a solid brand color.
- [ ] Use white surfaces and subtle borders for secondary buttons.
- [ ] Preserve hover, focus, active, and disabled states.
- [ ] Keep success and error messages clear without large tinted panels.
- [ ] Do not communicate status using color alone.

The result must look intentionally designed, not unstyled or stripped
of necessary interface boundaries.

### 7. Responsive behavior and accessibility

- [ ] Verify desktop and mobile layouts.
- [ ] Avoid horizontal overflow.
- [ ] Preserve semantic headings and accessible labels.
- [ ] Maintain readable contrast.
- [ ] Preserve visible keyboard focus.
- [ ] Keep mobile navigation usable.
- [ ] Keep media pickers and other dialogs usable.
- [ ] Ensure system dark mode does not override the white design.
- [ ] Do not disable accessibility features such as forced colors.

### 8. Preserve functionality and data

This is a presentation-focused phase.

- [ ] Preserve public routes and application behavior.
- [ ] Preserve authentication, authorization, and session handling.
- [ ] Preserve CSRF protection.
- [ ] Preserve existing Mako include argument fixes.
- [ ] Preserve media uploads, references, and access controls.
- [ ] Preserve Save Draft and Publish behavior.
- [ ] Avoid schema changes unless strictly necessary and explained.
- [ ] Do not reset the database or overwrite content.
- [ ] Do not rotate credentials or signing secrets.
- [ ] Preserve unrelated working-tree changes.
- [ ] Do not commit or push.

The previously reported missing image controls remain a separate issue.
Do not mark them fixed based on this visual redesign.

### 9. Implementation quality

- [ ] Prefer coherent updates to shared templates and styles.
- [ ] Do not rely on blanket `!important` overrides.
- [ ] Avoid global selectors that erase functional states or previews.
- [ ] Remove unused decorative styles where safe.
- [ ] Keep changes scoped to the white minimal redesign.
- [ ] Update this checklist according to actual progress.

### 10. Tests and visual verification

Run available checks:

- [ ] Backend regression tests.
- [ ] Mako template checks.
- [ ] Frontend production build.
- [ ] Lint and formatting checks for changed files.
- [ ] `git diff --check`.

If browser tooling is available, inspect:

- [ ] Home.
- [ ] Free Tools.
- [ ] Services & Work.
- [ ] Contact.
- [ ] Admin login.
- [ ] Admin dashboard.
- [ ] Content editors.
- [ ] Media Library and picker dialogs.
- [ ] Representative desktop and mobile widths.

Confirm visually:

- [ ] Page and section backgrounds are #FFFFFF.
- [ ] Decorative compositions and backgrounds are gone.
- [ ] The hero has no empty visual column.
- [ ] Meaningful content images remain.
- [ ] Text, controls, borders, and focus states remain readable.
- [ ] Navigation, forms, and dialogs remain usable.

If browser verification is unavailable, leave those checks unchecked
and explicitly report the limitation. Template tests do not prove
visual correctness.

### Acceptance criteria

- Public pages and admin screens use pure white backgrounds.
- No decorative compositions, patterns, or gradients remain.
- Home uses a balanced, text-focused hero without an empty image column.
- Meaningful images and functional icons remain intact.
- Admin hierarchy remains clear through typography, spacing, and borders.
- Desktop and mobile layouts remain usable.
- Authentication, CSRF, media handling, and draft/publish remain intact.
- No content or media files are deleted.

### Completion report

When finished, report:

1. Public website changes.
2. Admin panel changes.
3. Decorative elements removed.
4. Functional images and icons preserved.
5. Changed files.
6. Test and build results.
7. Unverified items and remaining limitations.
8. Required restart or asset-build commands.

Leave incomplete or blocked checklist items unchecked.
Do not commit or push.



## Phase 6 — Creative Homepage Hero

Status: Implemented; browser visual verification remains unverified

### Objective

Improve the visual impact of the homepage hero while preserving its
existing copy and pure white background.

Create a refined, creative-agency hero through expressive typography
and a conceptual visual beside the text.

This phase supersedes the text-only hero direction from Phase 5.
Other Phase 5 requirements remain unchanged.

Implement the changes, not just a proposal.

### 1. Inspect and preserve existing content

- [x] Inspect the Home template, hero styles, content schema, and editor.
- [x] Preserve all existing hero copy, capitalization, and punctuation.
- [x] Preserve CTA labels, destinations, and behavior.
- [x] Preserve CMS editing for existing text fields.
- [x] Do not overwrite saved content with hardcoded defaults.

The current headline is:

“Clear strategy.”
“Distinctive content.”

The current supporting copy is:

“We help businesses in Oman turn ideas into thoughtful marketing,
compelling content, and distinctive visual experiences.”

Preserve the existing eyebrow, both CTAs, and the closing line as well.
Use the actual stored content as the source of truth.

### 2. Create expressive, readable typography

- [x] Keep Roboto and Tailwind CSS v4.
- [x] Give “Clear strategy.” a precise, composed, medium-weight treatment.
- [x] Give “Distinctive content.” a stronger visual weight.
- [x] Emphasize “Distinctive” with the brand teal, #1E6F79.
- [x] Use carefully tuned line height, letter spacing, and responsive sizing.
- [x] Maintain one semantic H1, with spans for visual treatment if needed.
- [x] Preserve natural, accessible reading order.
- [x] Keep supporting text clearly subordinate but comfortably readable.
- [x] Ensure headings do not collide with the visual or overflow.

Avoid:
- Outlined or hollow headline text.
- Distorted, wavy, or rotating letters.
- Animated typing.
- Excessive gradients or text shadows.
- Converting the headline into an image.

Do not make typography depend on fragile exact-string replacement.
Use the existing structured fields where possible. If the content model
needs a minimal extension for emphasis, preserve existing data and
provide a safe rendering fallback for edited headlines.

### 3. Rebuild the hero composition

Desktop:

- [x] Use a balanced two-column composition.
- [x] Keep headline, supporting text, and CTAs on the left.
- [x] Place the conceptual visual on the right.
- [x] Adjust column proportions based on actual headline fit.
- [x] Keep the background pure #FFFFFF.
- [x] Preserve generous but purposeful whitespace.
- [x] Avoid excessive empty space or an oversized fixed-height hero.
- [x] Do not put artwork behind supporting text or buttons.

Mobile:

- [x] Keep the copy and CTAs first.
- [x] Place the visual below them.
- [x] Scale and position the artwork without horizontal overflow.
- [x] Avoid excessive vertical whitespace.
- [x] Preserve comfortable CTA touch targets.

Do not redesign the navigation or unrelated homepage sections.

### 4. Add the conceptual visual

Concept: “From clarity to distinction.”

Visual direction:

A sculptural arrangement of thin, orderly layers that gradually open
into a distinctive expressive form.

The ordered layers represent clear strategy.
The expressive result represents distinctive content.

Art direction:

- Matte material, resembling thick paper or a refined physical sculpture.
- Soft studio lighting and restrained natural shadows.
- A white or transparent background that blends into the white page.
- Navy and teal as primary colors.
- A small amount of warm yellow as an accent.

Brand palette:
- #384661
- #8491AF
- #1E6F79
- #F5DEA2
- #153A42

Requirements:

- [x] Create or source a suitable visual through tools actually available.
- [x] Prefer a high-quality static asset before adding animation.
- [x] Use a local, optimized asset rather than an externally hotlinked image.
- [x] Avoid a visible rectangular background or decorative card frame.
- [x] Keep text and slogans out of the artwork.
- [x] Do not use generic office/team stock photography.
- [x] Do not use fake dashboards, invented metrics, or client logos.
- [x] Do not restore the old circle/arch/block CSS composition.
- [x] Do not add a heavy 3D runtime merely to display a static visual.
- [x] Confirm usage rights for any externally sourced asset.

If suitable image-generation or licensed asset tools are unavailable:
- Do not substitute an unrelated stock image or crude placeholder.
- Implement the layout and configurable media slot.
- Report the artwork as blocked and provide a precise asset brief.
- Do not mark the visual or overall phase complete.
- Keep a graceful text-only fallback without an empty image column.

### 5. Make the hero visual editable

The previous missing-image-controls issue must not be repeated.

- [x] Reuse the existing Media Library and reusable image-field control.
- [x] Add a visible “Hero visual” section to the actual Home editor.
- [x] Show a current-image preview or a clear empty state.
- [x] Provide “Choose from Media Library”.
- [x] Provide “Upload new image”.
- [x] Provide “Remove image”.
- [x] Support appropriate alternative text and a decorative-image option.
- [x] Do not require manually entered URLs, paths, IDs, or HTML.
- [x] Ensure the control is actually rendered in the active editor route.
- [x] Preserve other unsaved form values during picker interactions.

Content behavior:

- [x] Selecting or uploading an image does not publish it.
- [x] Save Draft persists the selection without changing public Home.
- [x] Publish updates the public hero visual.
- [x] Removing a reference does not delete the library file.
- [x] Publishing an empty selection renders a balanced text-only hero.
- [x] Do not silently restore artwork after an intentional removal.
- [x] Preserve private-media and published-media access rules.
- [x] Do not overwrite any existing hero image selection.
- [x] If schema changes are necessary, use a backward-compatible migration.

Do not automatically publish new artwork into existing content.
Document how to select and publish the supplied asset.

### 6. Use restrained motion

- [x] A short, subtle entrance transition is acceptable.
- [x] Keep content visible if JavaScript fails or is disabled.
- [x] Respect prefers-reduced-motion.
- [x] Avoid continuous spinning, aggressive parallax, and cursor tracking.
- [x] Do not animate each letter independently.
- [x] Do not add animation dependencies without a clear necessity.

A strong static composition is sufficient.
Do not simulate moving layers by awkwardly deforming a flat image.

### 7. Performance and accessibility

- [x] Keep the headline as selectable HTML text.
- [x] Preserve accessible contrast and keyboard focus.
- [x] Use empty alt text for a purely decorative visual.
- [x] Use meaningful alt text if the selected visual conveys content.
- [x] Do not wrap the new image in the old composition's role="img"
      and unrelated aria-label.
- [x] Supply image dimensions or an aspect ratio to avoid layout shifts.
- [ ] Optimize asset size and responsive image delivery where supported.
- [x] Do not lazy-load the above-the-fold hero image.
- [x] Avoid unnecessary JavaScript and large rendering libraries.

### 8. Scope and safety

- [x] Limit public design changes to the Home hero.
- [x] Keep the public background pure white.
- [x] Keep the admin's white minimal design.
- [x] Do not redesign Direction, Creation, Presence, or Growth yet.
- [x] Do not change other sections or public copy.
- [x] Preserve authentication, authorization, sessions, and CSRF.
- [x] Preserve existing Mako include argument fixes.
- [x] Preserve draft/publish behavior.
- [x] Do not reset the database, delete media, or overwrite content.
- [x] Preserve unrelated working-tree changes.
- [x] Do not rotate credentials.
- [x] Do not commit or push.

### 9. Tests and verification

Run available checks:

- [x] Backend regression tests.
- [x] Mako template checks.
- [x] Frontend production build.
- [ ] Lint and formatting checks for changed files.
- [x] git diff --check.

Add appropriate coverage for:

- [x] Hero copy and CTA destinations remaining unchanged.
- [x] Home editor rendering the hero media control.
- [x] Saving a draft image without changing published Home.
- [x] Publishing and rendering the selected image.
- [x] Removing/publishing without deleting the media file.
- [x] Rendering a balanced fallback when no image is selected.
- [x] Appropriate alternative-text behavior.
- [x] Existing authentication and CSRF protections.

If browser tooling is available:

- [ ] Inspect desktop, tablet, and mobile layouts.
- [ ] Confirm headline wrapping and spacing.
- [ ] Confirm image controls are visible in the Home editor.
- [ ] Choose an image through the picker.
- [ ] Save Draft and reload the editor.
- [ ] Publish and verify public Home.
- [ ] Check reduced-motion behavior.
- [ ] Capture representative screenshots for review.

If browser tooling or artwork creation is unavailable, report that
explicitly and leave the corresponding checks incomplete.

Do not claim template tests prove visual quality or interactive behavior.

### Acceptance criteria

- Existing hero copy and CTA behavior are preserved.
- Typography has clear, intentional contrast and hierarchy.
- The background remains pure white.
- The conceptual visual complements rather than obscures the message.
- The old abstract CSS composition is not restored.
- Desktop and mobile layouts are balanced.
- The hero image can be managed through the actual Home editor.
- Draft and published image states remain separate.
- No unrelated sections, content, or security behavior are changed.

### Completion report

Report:

1. Hero layout and typography changes.
2. Artwork source, implementation, and any usage requirements.
3. Exact navigation to the Home hero media control.
4. How to select, save, publish, and remove the visual.
5. Changed files.
6. Tests and build results.
7. Browser checks and screenshots, if available.
8. Blocked or unverified items.
9. Any required migration, asset-build, or restart commands.

Update this checklist honestly.
Do not commit or push.
