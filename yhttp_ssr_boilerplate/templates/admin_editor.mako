<%inherit file="admin_master.mako" />
<%block name="title">${page_title | h} — Admin</%block>

<header class="mb-8 border-b border-color-4/20 pb-7">
  <p class="mb-3 text-xs font-medium uppercase tracking-[0.18em] text-color-2">Homepage content</p>
  <h1 class="text-4xl font-light tracking-tight sm:text-5xl">${page_title | h}</h1>
  <p class="mt-3 max-w-2xl text-base leading-7 text-color-2">${description | h}</p>
</header>

% if error:
  <p class="mb-6 border border-color-4/40 bg-color-1 px-4 py-3 text-sm" role="alert">${error | h}</p>
% endif
% if notice:
  <p class="mb-6 border border-color-3/60 bg-color-1 px-4 py-3 text-sm" role="status">${notice | h}</p>
% endif

% if is_collection:
  <section class="mb-10 border border-color-4/20 bg-color-1/45 p-5 sm:p-7" aria-labelledby="new-item-title">
    <h2 id="new-item-title" class="text-2xl font-light">Add ${page_title.lower() | h}</h2>
    <p class="mt-2 text-sm leading-6 text-color-2">New items stay in draft until published.</p>
    <form action="/admin/${section}" method="post" class="mt-6 grid gap-5 md:grid-cols-2">
      <input type="hidden" name="csrf" value="${csrf | h}">
      % for field in create_fields:
        <%include file="admin_field.mako" args="field=field, form_id='create-' + field['name']" />
      % endfor
      <div class="flex flex-wrap items-center gap-3 md:col-span-2">
        <button class="min-h-11 bg-color-4 px-5 py-2.5 text-sm font-medium text-color-5 hover:bg-color-4/90" type="submit" name="action" value="save_draft">Save as draft</button>
        <button class="min-h-11 border border-color-4/40 px-5 py-2.5 text-sm hover:bg-color-4/10" type="submit" name="action" value="publish">Publish</button>
      </div>
    </form>
  </section>
% endif

% if not entries and not is_collection:
  <p class="border border-color-4/20 bg-color-1/45 px-5 py-6 text-sm leading-6 text-color-2">No CMS content is available yet. Run the database migration and initial content seed described in the setup guide.</p>
% elif not entries:
  <p class="border border-color-4/20 bg-color-1/45 px-5 py-6 text-sm leading-6 text-color-2">No items yet. Add the first item above.</p>
% endif

<section class="space-y-6" aria-label="${page_title | h} entries">
  % for entry in entries:
    <article class="border border-color-4/20 bg-color-1/40 p-5 sm:p-7 ${'opacity-70' if entry['archived'] else ''}">
      <div class="mb-5 flex flex-wrap items-start justify-between gap-3 border-b border-color-4/15 pb-4">
        <div>
          <p class="text-xs uppercase tracking-[0.15em] text-color-2">${entry['status'] | h}${' · archived' if entry['archived'] else ''}</p>
          <h2 class="mt-2 text-xl font-medium">${entry['title'] | h}</h2>
          <p class="mt-1 text-xs text-color-2">Updated ${entry['updated_at']}</p>
        </div>
        % if entry['published_at']:
          <p class="text-xs text-color-2">Last published ${entry['published_at']}</p>
        % endif
      </div>

      <form action="/admin/${section}" method="post" class="grid gap-5 md:grid-cols-2" data-track-changes>
        <input type="hidden" name="csrf" value="${csrf | h}">
        <input type="hidden" name="record_id" value="${entry['id'] | h}">
        % for field in entry['fields']:
          <%include file="admin_field.mako" args="field=field, form_id=entry['id'] + '-' + field['name']" />
        % endfor
        <div class="flex flex-wrap items-end gap-x-8 gap-y-4 md:col-span-2">
          <label class="flex min-h-11 items-center gap-3 text-sm">
            <input class="size-5 accent-color-4" type="checkbox" name="visible" value="yes" ${'checked' if entry['draft_visible'] else ''}>
            Visible when published
          </label>
          <label class="flex min-h-11 items-center gap-3 text-sm">
            <span>Display order</span>
            <input class="min-h-10 w-24 border border-color-2/45 bg-color-5 px-3 text-color-4" type="number" name="display_order" value="${entry['display_order']}" min="-100000" max="100000">
          </label>
        </div>
        <div class="flex flex-wrap gap-3 md:col-span-2">
          <button class="min-h-11 bg-color-4 px-5 py-2.5 text-sm font-medium text-color-5 hover:bg-color-4/90" type="submit" name="action" value="save_draft">Save draft</button>
          <button class="min-h-11 border border-color-4/40 px-5 py-2.5 text-sm hover:bg-color-4/10" type="submit" name="action" value="publish">Publish</button>
          % if entry['published_at']:
            <button class="min-h-11 border border-color-4/25 px-5 py-2.5 text-sm text-color-2 hover:border-color-4/50 hover:text-color-4" type="submit" name="action" value="unpublish" onclick="return confirm('Remove this item from the public homepage?')">Unpublish</button>
          % endif
        </div>
      </form>

      % if is_collection:
        <div class="mt-5 flex flex-wrap gap-2 border-t border-color-4/15 pt-4">
          <form action="/admin/${section}" method="post">
            <input type="hidden" name="csrf" value="${csrf | h}">
            <input type="hidden" name="record_id" value="${entry['id'] | h}">
            <button class="min-h-10 border border-color-4/20 px-3 py-2 text-xs hover:border-color-4/45" name="action" value="move_up" type="submit" aria-label="Move ${entry['title'] | h} up">Move up ↑</button>
            <button class="min-h-10 border border-color-4/20 px-3 py-2 text-xs hover:border-color-4/45" name="action" value="move_down" type="submit" aria-label="Move ${entry['title'] | h} down">Move down ↓</button>
          </form>
          <form action="/admin/${section}" method="post" onsubmit="return confirm('${'Restore' if entry['archived'] else 'Archive'} this item?')">
            <input type="hidden" name="csrf" value="${csrf | h}">
            <input type="hidden" name="record_id" value="${entry['id'] | h}">
            % if entry['archived']:
              <button class="min-h-10 border border-color-4/20 px-3 py-2 text-xs hover:border-color-4/45" name="action" value="restore" type="submit">Restore</button>
            % else:
              <button class="min-h-10 border border-color-4/20 px-3 py-2 text-xs text-color-2 hover:border-color-4/45 hover:text-color-4" name="action" value="archive" type="submit">Archive</button>
            % endif
          </form>
        </div>
      % endif
    </article>
  % endfor
</section>
