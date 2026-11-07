<%inherit file="admin_master.mako" />
<%block name="title">Media library — Admin</%block>

<header class="mb-8 border-b border-color-4/20 pb-7">
  <p class="mb-3 text-xs font-medium uppercase tracking-[0.18em] text-color-2">Private uploads</p>
  <h1 class="text-4xl font-semibold tracking-tight sm:text-5xl">Media library</h1>
  <p class="mt-3 max-w-2xl text-base leading-7 text-color-2">Upload once, then reuse images across homepage sections. Unpublished files stay private.</p>
</header>

% if error:
  <p class="mb-6 border border-color-4/40 bg-color-1 px-4 py-3 text-sm" role="alert">${error | h}</p>
% endif
% if notice:
  <p class="mb-6 border border-color-3/60 bg-color-1 px-4 py-3 text-sm" role="status">${notice | h}</p>
% endif

<section class="mb-10 border border-color-4/20 bg-color-1/45 p-5 sm:p-7" aria-labelledby="upload-heading">
  <h2 id="upload-heading" class="text-2xl font-semibold">Upload image or resource</h2>
  <p class="mt-2 text-sm leading-6 text-color-2">Supported: JPG/JPEG, PNG, WEBP, PDF, DOCX, XLSX, and CSV. Maximum ${max_upload_mb} MB per file; images may be up to 30 megapixels.</p>
  <form action="/admin/media" method="post" enctype="multipart/form-data" class="mt-6 grid gap-5 md:grid-cols-2">
    <input type="hidden" name="csrf" value="${csrf | h}">
    <input type="hidden" name="action" value="upload">
    <div>
      <label class="mb-2 block text-sm font-medium" for="upload">File</label>
      <input class="min-h-12 w-full border border-color-2/45 bg-color-5 px-3 py-2 text-sm text-color-4 file:mr-4 file:border-0 file:bg-color-4 file:px-3 file:py-2 file:font-medium file:text-color-5" id="upload" name="upload" type="file" accept=".jpg,.jpeg,.png,.webp,.pdf,.docx,.xlsx,.csv" required>
    </div>
    <div>
      <label class="mb-2 block text-sm font-medium" for="default-alt">Default alt text</label>
      <input class="min-h-12 w-full border border-color-2/45 bg-color-5 px-4 py-3 text-sm text-color-4 outline-none focus:border-color-4" id="default-alt" name="default_alt" maxlength="300" placeholder="Describe the image, or leave blank if decorative">
      <label class="mt-3 flex min-h-10 items-center gap-3 text-sm">
        <input class="size-4 accent-color-4" type="checkbox" name="decorative" value="yes">
        Image is decorative by default
      </label>
    </div>
    <button class="min-h-11 w-fit bg-color-4 px-5 py-2.5 text-sm font-medium text-color-5 hover:bg-color-4/90 md:col-span-2" type="submit">Upload image or file</button>
  </form>
</section>

<section class="mb-6 flex flex-col gap-4 border-b border-color-4/15 pb-5 sm:flex-row sm:items-end sm:justify-between" aria-labelledby="library-heading">
  <div><h2 id="library-heading" class="text-2xl font-semibold">Your library</h2><p class="mt-1 text-sm text-color-2">${result_count} result${'' if result_count == 1 else 's'} · 24 items per page</p></div>
  <form action="/admin/media" method="get" class="flex w-full gap-2 sm:max-w-md">
    <label class="sr-only" for="media-search">Search filenames</label>
    <input class="min-h-11 min-w-0 flex-1 border border-color-2/45 bg-white px-3 text-sm outline-none focus:border-color-4" id="media-search" name="search" type="search" value="${search | h}" placeholder="Search filenames">
    <button class="min-h-11 bg-color-4 px-4 text-sm font-medium text-color-5" type="submit">Search</button>
  </form>
</section>

% if assets:
  <section class="grid gap-4 md:grid-cols-2 2xl:grid-cols-3" aria-label="Media assets">
    % for asset in assets:
      <article class="min-w-0 border border-color-4/20 bg-color-1/40 p-4 sm:p-5">
        % if asset['mime_type'].startswith('image/'):
          <a class="mb-4 block aspect-[16/10] overflow-hidden bg-color-5" href="/admin/media/${asset['id']}/preview" target="_blank" rel="noopener noreferrer" aria-label="Preview ${asset['filename'] | h}">
            <img class="h-full w-full object-cover" src="/admin/media/${asset['id']}/preview" alt="${asset['alt_text'] | h}">
          </a>
        % else:
          <div class="mb-4 flex aspect-[16/10] items-center justify-center bg-color-5 text-4xl text-color-2" aria-hidden="true">⇩</div>
        % endif
        <h3 class="break-all text-base font-semibold">${asset['filename'] | h}</h3>
        <p class="mt-2 text-xs leading-5 text-color-2">${asset['mime_type'] | h} · ${asset['size'] // 1024} KB
          % if asset['width'] and asset['height']:
            · ${asset['width']} × ${asset['height']} px
          % endif
        </p>
        <p class="mt-1 text-xs ${'text-color-4' if asset['used'] else 'text-color-2'}">${'Used in content' if asset['used'] else 'Unused'}</p>

        % if asset['mime_type'].startswith('image/'):
          <form class="mt-4 border-t border-color-4/15 pt-4" action="/admin/media/${asset['id']}" method="post">
            <input type="hidden" name="csrf" value="${csrf | h}">
            <label class="mb-2 block text-xs font-medium" for="alt-${asset['id']}">Default alt text</label>
            <div class="flex gap-2">
              <input class="min-h-10 min-w-0 flex-1 border border-color-2/45 bg-color-5 px-3 py-2 text-sm outline-none focus:border-color-4" id="alt-${asset['id']}" name="alt_text" value="${asset['alt_text'] | h}" maxlength="300">
              <button class="min-h-10 border border-color-4/35 px-3 py-2 text-xs hover:bg-color-4/10" type="submit">Save alt</button>
            </div>
            <label class="mt-2 flex min-h-9 items-center gap-3 text-xs text-color-2">
              <input class="size-4 accent-color-4" type="checkbox" name="decorative" value="yes" ${'checked' if asset['decorative'] else ''}>
              Decorative by default
            </label>
          </form>
        % else:
          <p class="mt-4 border-t border-color-4/15 pt-4 text-xs text-color-2">Private until a resource using this file is published as available.</p>
        % endif

        <form class="mt-3 flex flex-wrap items-center justify-between gap-3" action="/admin/media/${asset['id']}/delete" method="post" onsubmit="return confirm('Permanently delete this unused file?')">
          <input type="hidden" name="csrf" value="${csrf | h}">
          <label class="flex min-h-10 items-center gap-2 text-xs text-color-2">
            <input class="size-4 accent-color-4" type="checkbox" name="confirm_delete" value="yes" ${'disabled' if asset['used'] else ''} ${'required' if not asset['used'] else ''}>
            Confirm delete
          </label>
          <button class="min-h-10 border border-color-4/25 px-3 py-2 text-xs ${'cursor-not-allowed opacity-50' if asset['used'] else 'hover:border-color-4/50'}" type="submit" ${'disabled' if asset['used'] else ''}>Delete</button>
        </form>
      </article>
    % endfor
  </section>
% else:
  <p class="border border-color-4/20 bg-color-1/45 px-5 py-6 text-sm leading-6 text-color-2" role="status">${'No files match this filename search.' if search else 'No media has been uploaded yet. Use Upload image or resource above to add your first file.'}</p>
% endif

% if has_previous or has_next:
  <nav class="mt-6 flex items-center justify-between" aria-label="Media library pages">
    % if has_previous:
      <a class="min-h-11 border border-color-4/30 px-4 py-3 text-sm hover:bg-color-1" href="/admin/media?page=${page - 1}&amp;search=${search | u}">Previous</a>
    % else:
      <span></span>
    % endif
    <span class="text-sm text-color-2">Page ${page}</span>
    % if has_next:
      <a class="min-h-11 border border-color-4/30 px-4 py-3 text-sm hover:bg-color-1" href="/admin/media?page=${page + 1}&amp;search=${search | u}">Next</a>
    % else:
      <span></span>
    % endif
  </nav>
% endif
