<%inherit file="admin_master.mako" />
<%block name="title">${page_title | h} — Admin</%block>

<header class="mb-8 border-b border-slate-200 pb-7">
  <p class="mb-3 text-xs font-medium uppercase tracking-[0.18em] text-slate-600">Homepage content</p>
  <h1 class="text-4xl font-light tracking-tight sm:text-5xl">${page_title | h}</h1>
  <p class="mt-3 max-w-2xl text-base leading-7 text-slate-600">${description | h}</p>
</header>

% if error:
  <p class="mb-6 border border-slate-200 bg-white px-4 py-3 text-sm" role="alert">${error | h}</p>
% endif
% if notice:
  <p class="mb-6 border border-teal-700 bg-white px-4 py-3 text-sm" role="status">${notice | h}</p>
% endif

% if is_collection:
  <section class="mb-10 border border-slate-200 bg-white p-5 sm:p-7" aria-labelledby="new-item-title">
    <h2 id="new-item-title" class="text-2xl font-light">Add ${page_title.lower() | h}</h2>
    <p class="mt-2 text-sm leading-6 text-slate-600">New items stay in draft until published.</p>
    <form action="/admin/${section}" method="post" class="mt-6 space-y-5">
      <input type="hidden" name="csrf" value="${csrf | h}">
      % for group in create_field_groups:
        <fieldset class="border border-slate-200 bg-white/50 p-4 sm:p-6">
          <legend class="px-2 text-lg font-semibold">${group['title'] | h}</legend>
          <p class="mb-4 text-sm leading-6 text-slate-600">${group['description'] | h}</p>
          <div class="grid gap-5 md:grid-cols-2">
            % for field in group['fields']:
              <%include file="admin_field.mako" args="field=field, form_id='create-' + field['name'], csrf=csrf" />
            % endfor
          </div>
        </fieldset>
      % endfor
      <div class="border-t border-slate-200 pt-4">
        <p class="mb-3 text-sm text-slate-600">Save draft keeps this item off the live homepage. Publish makes the submitted changes public.</p>
        <div class="flex flex-wrap items-center gap-3">
          <button class="min-h-11 border border-slate-200 px-5 py-2.5 text-sm font-medium hover:border-slate-400" type="submit" name="action" value="save_draft">Save draft</button>
          <button class="min-h-11 bg-color-3 px-5 py-2.5 text-sm font-semibold text-white hover:bg-teal-800" type="submit" name="action" value="publish">Publish</button>
        </div>
      </div>
    </form>
  </section>
% endif

% if not entries and not is_collection:
  <p class="border border-slate-200 bg-white px-5 py-6 text-sm leading-6 text-slate-600">No CMS content is available yet. Run the database migration and initial content seed described in the setup guide.</p>
% elif not entries:
  <p class="border border-slate-200 bg-white px-5 py-6 text-sm leading-6 text-slate-600">No items yet. Add the first item above.</p>
% endif

<section class="space-y-6" aria-label="${page_title | h} entries">
  % for entry in entries:
    <article class="border border-slate-200 bg-white p-5 sm:p-7 ${'opacity-70' if entry['archived'] else ''}">
      <div class="mb-5 flex flex-wrap items-start justify-between gap-3 border-b border-slate-200 pb-4">
        <div>
          <p class="text-xs uppercase tracking-[0.15em] text-slate-600">${entry['status'] | h}${' · archived' if entry['archived'] else ''}</p>
          <h2 class="mt-2 text-xl font-medium">${entry['title'] | h}</h2>
          <p class="mt-1 text-xs text-slate-600">Updated ${entry['updated_at']}</p>
        </div>
        % if entry['published_at']:
          <p class="text-xs text-slate-600">Last published ${entry['published_at']}</p>
        % endif
      </div>

      <form action="/admin/${section}" method="post" class="space-y-5" data-track-changes>
        <input type="hidden" name="csrf" value="${csrf | h}">
        <input type="hidden" name="record_id" value="${entry['id'] | h}">
        % for group in entry['field_groups']:
          <fieldset class="border border-slate-200 bg-white/45 p-4 sm:p-6">
            <legend class="px-2 text-lg font-semibold">${group['title'] | h}</legend>
            <p class="mb-4 text-sm leading-6 text-slate-600">${group['description'] | h}</p>
            <div class="grid gap-5 md:grid-cols-2">
              % for field in group['fields']:
                <%include file="admin_field.mako" args="field=field, form_id=entry['id'] + '-' + field['name'], csrf=csrf" />
              % endfor
            </div>
          </fieldset>
        % endfor
        <div class="flex flex-wrap items-end gap-x-8 gap-y-4 md:col-span-2">
          <label class="flex min-h-11 items-center gap-3 text-sm">
            <input class="size-5 accent-color-3" type="checkbox" name="visible" value="yes" ${'checked' if entry['draft_visible'] else ''}>
            Visible when published
          </label>
          <label class="flex min-h-11 items-center gap-3 text-sm">
            <span>Display order</span>
            <input class="min-h-10 w-24 border border-slate-200 bg-white px-3 text-slate-900" type="number" name="display_order" value="${entry['display_order']}" min="-100000" max="100000">
          </label>
        </div>
        <div class="border-t border-slate-200 pt-4">
          <p class="mb-3 text-sm text-slate-600">Save draft keeps this content off the live homepage. Publish makes these changes public.</p>
          <div class="flex flex-wrap gap-3">
          <button class="min-h-11 border border-slate-200 px-5 py-2.5 text-sm font-medium hover:border-slate-400" type="submit" name="action" value="save_draft">Save draft</button>
          <button class="min-h-11 bg-color-3 px-5 py-2.5 text-sm font-semibold text-white hover:bg-teal-800" type="submit" name="action" value="publish">Publish</button>
          % if entry['published_at']:
            <button class="min-h-11 border border-slate-200 px-5 py-2.5 text-sm text-slate-600 hover:border-slate-200 hover:text-slate-900" type="submit" name="action" value="unpublish" onclick="return confirm('Remove this item from the public homepage?')">Unpublish</button>
          % endif
          </div>
        </div>
      </form>

      % if is_collection:
        <div class="mt-5 flex flex-wrap gap-2 border-t border-slate-200 pt-4">
          <form action="/admin/${section}" method="post">
            <input type="hidden" name="csrf" value="${csrf | h}">
            <input type="hidden" name="record_id" value="${entry['id'] | h}">
            <button class="min-h-10 border border-slate-200 px-3 py-2 text-xs hover:border-slate-200" name="action" value="move_up" type="submit" aria-label="Move ${entry['title'] | h} up">Move up ↑</button>
            <button class="min-h-10 border border-slate-200 px-3 py-2 text-xs hover:border-slate-200" name="action" value="move_down" type="submit" aria-label="Move ${entry['title'] | h} down">Move down ↓</button>
          </form>
          <form action="/admin/${section}" method="post" onsubmit="return confirm('${'Restore' if entry['archived'] else 'Archive'} this item?')">
            <input type="hidden" name="csrf" value="${csrf | h}">
            <input type="hidden" name="record_id" value="${entry['id'] | h}">
            % if entry['archived']:
              <button class="min-h-10 border border-slate-200 px-3 py-2 text-xs hover:border-slate-200" name="action" value="restore" type="submit">Restore</button>
            % else:
              <button class="min-h-10 border border-slate-200 px-3 py-2 text-xs text-slate-600 hover:border-slate-200 hover:text-slate-900" name="action" value="archive" type="submit">Archive</button>
            % endif
          </form>
        </div>
      % endif
    </article>
  % endfor
</section>
