<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="robots" content="noindex, nofollow, noarchive">
    <meta name="theme-color" content="#FFFFFF">
    <title><%block name="title">Admin — ${agency_name | h}</%block></title>
    % if settings.env == 'development':
      <script type="module" src="${asseturl('@vite/client')}"></script>
    % endif
    <link rel="stylesheet" href="${asseturl('www/master.css')}">
  </head>
  <body class="min-h-screen bg-white text-slate-900 antialiased">
    % if show_navigation:
      <% admin_navigation = (
        ('/admin', 'Dashboard'),
        ('/admin/home', 'Homepage'),
        ('/admin/services', 'Services'),
        ('/admin/portfolio', 'Portfolio'),
        ('/admin/resources', 'Free resources'),
        ('/admin/media', 'Media library'),
        ('/admin/settings', 'Settings'),
      ) %>
      <div class="min-h-screen lg:grid lg:grid-cols-[250px_minmax(0,1fr)]">
        <aside class="border-b border-slate-200 p-5 lg:min-h-screen lg:border-b-0 lg:border-r lg:px-6 lg:py-8">
          <a href="/" class="text-lg font-medium tracking-tight text-slate-900">${agency_name | h}</a>
          <p class="mt-1 text-xs uppercase tracking-[0.18em] text-slate-600">Admin workspace</p>
          <nav class="mt-6 flex gap-2 overflow-x-auto pb-2 lg:mt-10 lg:flex-col lg:overflow-visible" aria-label="Admin navigation">
            % for href, label in admin_navigation:
              <a class="min-h-11 shrink-0 rounded-sm px-3 py-3 text-sm ${'bg-color-3 text-white' if context.get('active_href') == href else 'text-slate-700 hover:text-teal-800'} focus-visible:outline-2 focus-visible:outline-teal-700" href="${href}" ${'aria-current="page"' if context.get('active_href') == href else ''}>${label}</a>
            % endfor
          </nav>
          <div class="mt-3 flex gap-4 border-t border-slate-200 pt-5 text-sm lg:flex-col">
            <a class="min-h-11 py-3 text-slate-600 hover:text-slate-900" href="/">View public website ↗</a>
            <form action="/admin/logout" method="post">
              <input type="hidden" name="csrf" value="${csrf | h}">
              <button class="min-h-11 py-3 text-slate-600 hover:text-slate-900" type="submit">Log out</button>
            </form>
          </div>
        </aside>
        <main class="min-w-0 px-5 py-8 sm:px-8 lg:px-12 lg:py-10">
          ${self.body()}
        </main>
      </div>
    % else:
      ${self.body()}
    % endif
    <script type="module" src="${asseturl('www/master.js')}"></script>
    % if show_navigation:
      <script>
        document.querySelectorAll('[data-track-changes]').forEach((form) => {
          let changed = false;
          form.addEventListener('input', () => { changed = true; });
          form.addEventListener('change', () => { changed = true; });
          form.addEventListener('submit', () => { changed = false; });
          window.addEventListener('beforeunload', (event) => {
            if (changed) {
              event.preventDefault();
              event.returnValue = '';
            }
          });
        });
      </script>
    % endif
  </body>
</html>
