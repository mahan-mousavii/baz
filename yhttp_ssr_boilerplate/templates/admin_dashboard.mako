<%inherit file="admin_master.mako" />
<%block name="title">Dashboard — ${agency_name | h}</%block>
<header class="mb-8 border-b border-color-4/20 pb-7">
  <p class="mb-3 text-xs font-medium uppercase tracking-[0.18em] text-color-2">Content overview</p>
  <h1 class="text-4xl font-light tracking-tight sm:text-5xl">Dashboard</h1>
  <p class="mt-3 max-w-2xl text-base leading-7 text-color-2">Manage the content that appears on the existing homepage.</p>
</header>

<section class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3" aria-label="Content sections">
  % for section in sections:
    <a class="group min-h-48 border border-color-4/20 bg-color-1/55 p-5 transition-colors hover:border-color-4/45 hover:bg-color-1" href="/admin/${section['section']}">
      <h2 class="text-xl font-medium">${section['title'] | h}</h2>
      <p class="mt-4 text-sm text-color-2">${section['count']} item${'' if section['count'] == 1 else 's'} · ${section['published']} published · ${section['drafts']} draft${'' if section['drafts'] == 1 else 's'}</p>
      <span class="mt-8 inline-block text-sm text-color-4">Open section ↗</span>
    </a>
  % endfor
</section>
