<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="${agency['positioning'] | h} Based in Oman.">
    <meta name="theme-color" content="#FFFFFF">
    <title>${agency['name'] | h} — Creative Marketing Agency · Oman</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    % if settings.env == 'development':
      <script type="module" src="${asseturl('@vite/client')}"></script>
    % endif
    <link rel="stylesheet" href="${asseturl('www/master.css')}">
    % if hasattr(next, 'head'):
      ${next.head()}
    % endif
  </head>
  <body id="top" x-data="{ menuOpen: false }" @keydown.escape.window="menuOpen = false">
    <header class="site-header">
      % if agency.get('logo_asset_id'):
        <a class="wordmark wordmark-image" href="#top" aria-label="${agency['name'] | h} home"><img src="/media/${agency['logo_asset_id'] | h}" alt="${agency['name'] | h}"></a>
      % else:
        <a class="wordmark" href="#top" aria-label="${agency['name'] | h} home">${agency['name'] | h}</a>
      % endif
      <button class="menu-toggle" type="button" @click="menuOpen = !menuOpen" :aria-expanded="menuOpen" aria-controls="primary-navigation" aria-label="Toggle navigation">
        <span></span><span></span>
      </button>
      <nav id="primary-navigation" class="primary-navigation" :class="{ 'is-open': menuOpen }" aria-label="Main navigation">
        % for item in navigation:
          <a class="nav-link ${'nav-contact' if item.get('cta') else ''}" href="${item['href']}" @click="menuOpen = false">${item['label']}</a>
        % endfor
      </nav>
    </header>
    <main>
      ${self.body()}
    </main>
    <script type="module" src="${asseturl('www/master.js')}"></script>
  </body>
</html>
