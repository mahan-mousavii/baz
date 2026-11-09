<%inherit file="master.mako" />

<%block name="head">
  <meta property="og:title" content="${agency['name'] | h} — Creative Marketing Agency · Oman">
  <meta property="og:description" content="${agency['positioning'] | h} Based in Oman.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="${settings.publicurl.rstrip('/')}/">
</%block>

<section class="hero${' hero-with-visual' if home.get('hero_visual_asset_id') else ''}" aria-labelledby="home-title">
  <div class="hero-copy">
    <p class="eyebrow">${home['eyebrow'] | h}</p>
    <h1 id="home-title"><span class="hero-title-line hero-title-line-first">${headline_lines[0] | h}</span> <span class="hero-title-line hero-title-line-second"><span class="hero-title-accent">${headline_emphasis | h}</span>${headline_remainder | h}</span></h1>
    <p class="hero-description">${home['hero_description'] | h}</p>
    <div class="hero-actions">
      <a class="button button-primary" href="${home['primary_cta_href'] | h}">${home['primary_cta_label'] | h} <span aria-hidden="true">↘</span></a>
      <a class="button button-text" href="${home['secondary_cta_href'] | h}">${home['secondary_cta_label'] | h} <span aria-hidden="true">↗</span></a>
    </div>
    <p class="hero-location">Independent thinking, rooted in Oman.</p>
  </div>
  % if home.get('hero_visual_asset_id'):
    <img class="hero-visual" src="/media/${home['hero_visual_asset_id'] | h}" alt="${home.get('hero_visual_alt', '') | h}" width="${home.get('hero_visual_width') or 1200}" height="${home.get('hero_visual_height') or 800}" loading="eager" fetchpriority="high" decoding="async">
  % endif
</section>

<section class="services-section section-shell" id="services-work" aria-labelledby="services-title">
  <div class="section-intro">
    <p class="eyebrow">THINKING, THEN MAKING</p>
    <h2 id="services-title">${home['services_heading'] | h}</h2>
    <p class="section-summary">${home['services_intro'] | h}</p>
  </div>
  <div class="service-list">
    % for service in services:
      <article class="service-row">
        <div class="service-heading">
          <div class="service-title-group">
            <h3>${service['title'] | h}</h3>
            <p class="service-subtitle">${service['subtitle'] | h}</p>
          </div>
        </div>
        <p class="service-description">${service['description'] | h}</p>
      </article>
    % endfor
  </div>
  <div class="work-intro"><p class="eyebrow">A FEEL FOR THE POSSIBLE</p><p>${home['portfolio_heading'] | h}</p><p class="section-summary">${home['portfolio_intro'] | h}</p></div>
  <div class="project-grid">
    % for project in projects[:2]:
      <article class="project-preview">
        % if project.get('cover_asset_id'):
          <div class="project-art project-photo">
            <img src="/media/${project['cover_asset_id'] | h}" alt="${project.get('cover_alt', '') | h}">
          </div>
        % endif
        <div class="project-caption"><div><span class="project-type">${project['category'] | h}</span><h3>${project['title'] | h}</h3></div>
          % if project.get('project_type') == 'concept':
            <span class="concept-tag">Concept Preview</span>
          % else:
            <span class="project-type">CLIENT WORK</span>
          % endif
        </div>
      </article>
    % endfor
  </div>
</section>

<section class="tools-section" id="free-tools" aria-labelledby="tools-title">
  <div class="tools-shell">
    <div class="tools-heading"><p class="eyebrow">GOOD THINKING, SHARED</p><h2 id="tools-title">${resources_heading_lines[0] | h}<br><span>${resources_heading_lines[1] | h}</span></h2><p>${home['resources_intro'] | h}</p></div>
    <div class="tool-list">
      % for tool in tools[:3]:
        <article class="tool-row">
          % if tool.get('cover_asset_id'):
            <img class="tool-cover" src="/media/${tool['cover_asset_id'] | h}" alt="${tool.get('cover_alt', '') | h}">
          % else:
            <span class="tool-label" aria-hidden="true">Resource</span>
          % endif
          <div class="tool-copy"><h3>${tool['title'] | h}</h3><p>${tool['description'] | h}</p></div>
          % if tool.get('download_href'):
            <a class="coming-soon resource-link" href="${tool['download_href'] | h}">Open resource <span aria-hidden="true">↗</span></a>
          % else:
            <span class="coming-soon">Coming soon</span>
          % endif
        </article>
      % endfor
    </div>
  </div>
</section>

<section class="about-section section-shell" aria-labelledby="about-title">
  <p class="eyebrow">A LITTLE ABOUT HOW WE THINK</p>
  <div class="about-content"><h2 id="about-title">${about_heading_lines[0] | h}<br><span>${about_heading_lines[1] | h}</span></h2><p>${home['about_description'] | h}</p></div>
</section>

<section class="contact-section" id="contact" aria-labelledby="contact-title">
  <div class="contact-shell"><div class="contact-copy"><p class="eyebrow">START A CONVERSATION</p><h2 id="contact-title">${contact_heading_lines[0] | h}<br><span>${contact_heading_lines[1] | h}</span></h2><p>${home['contact_description'] | h}</p></div>
    <div class="contact-details">
      <div class="contact-detail"><span>BUSINESS EMAIL</span>
        % if agency['email']:
          <a href="mailto:${agency['email'] | h}">${agency['email'] | h}</a>
        % else:
          <p class="contact-placeholder">[Business email placeholder]</p>
        % endif
      </div>
      <div class="contact-detail"><span>WHATSAPP</span>
        % if agency['whatsapp_url']:
          <a href="${agency['whatsapp_url'] | h}" target="_blank" rel="noopener noreferrer">Message us <span aria-hidden="true">↗</span></a>
        % else:
          <p class="contact-placeholder">[WhatsApp URL placeholder]</p>
        % endif
      </div>
    </div>
  </div>
</section>

<footer class="site-footer">
  <div class="footer-main"><div><a class="wordmark footer-wordmark" href="#top">${agency['name'] | h}</a><p>${(agency['footer_text'] or agency['positioning']) | h}</p>
    <div class="footer-socials">
      % if agency.get('instagram_url'):
        <a href="${agency['instagram_url'] | h}" target="_blank" rel="noopener noreferrer">Instagram ↗</a>
      % endif
      % if agency.get('linkedin_url'):
        <a href="${agency['linkedin_url'] | h}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a>
      % endif
    </div>
  </div>
    <nav class="footer-navigation" aria-label="Footer navigation">
      % for item in navigation:
        <a href="${item['href'] | h}">${item['label'] | h}</a>
      % endfor
    </nav>
  </div>
  <div class="footer-bottom"><span>© ${year} ${agency['name'] | h}. All rights reserved.</span><span>Based in Oman</span></div>
</footer>
