<%inherit file="master.mako" />

<%def name="icon(name, class_name)">
  <svg class="${class_name}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><use href="#icon-${name}"></use></svg>
</%def>

<%def name="decoration_layer(section)">
  <div class="decorative-layer" aria-hidden="true">
    % for name, position in decorations[section]:
      ${self.icon(name, 'background-icon ' + position)}
    % endfor
  </div>
</%def>

<%block name="head">
  <meta property="og:title" content="${agency['name']} — Creative Marketing Agency · Oman">
  <meta property="og:description" content="${agency['positioning']} Based in Oman.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="${settings.publicurl.rstrip('/')}/">
</%block>

<svg class="icon-sprite" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg">
  <symbol id="icon-compass" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="m16.2 7.8-2.1 6.3-6.3 2.1 2.1-6.3z"/></symbol>
  <symbol id="icon-clapperboard" viewBox="0 0 24 24"><path d="M4 8h16v12H4zM4 8l1-4h16l-1 4M8 4l4 4m2-4 4 4"/></symbol>
  <symbol id="icon-message-circle" viewBox="0 0 24 24"><path d="M21 11.5a8.5 8.5 0 0 1-12.3 7.6L3 21l1.9-5.4A8.5 8.5 0 1 1 21 11.5Z"/><path d="M8 12h.01M12 12h.01M16 12h.01"/></symbol>
  <symbol id="icon-trending-up" viewBox="0 0 24 24"><path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/></symbol>
  <symbol id="icon-camera" viewBox="0 0 24 24"><path d="M14 4h-4L8 7H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3z"/><circle cx="12" cy="13" r="3"/></symbol>
  <symbol id="icon-video" viewBox="0 0 24 24"><path d="M15 10 20 7v10l-5-3M4 6h11v12H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2Z"/></symbol>
  <symbol id="icon-megaphone" viewBox="0 0 24 24"><path d="m3 11 18-5v12l-18-5zM11.6 16.8 13 22M3 11v2M21 10v4"/></symbol>
  <symbol id="icon-pen-tool" viewBox="0 0 24 24"><path d="m12 19 7-7 3 3-7 7zM18 13l-7-7 3-3 7 7zM11 6 5 8l-2 6 6 2 2-6zM3 14l-1 8 8-6"/></symbol>
  <symbol id="icon-aperture" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="m14.3 6.2 3.4 5.8M9.7 6.2h6.8M5.7 9.1l3.4-5.8M4 15l3.4-5.9m-1.1 8.7h6.8m-4.5-5.6-3.4 5.9m8.5-.3-3.4-5.9m7.4 2.9-3.4 5.8M20 9l-3.4 5.9"/></symbol>
  <symbol id="icon-sparkles" viewBox="0 0 24 24"><path d="m12 3 1.9 5.8L20 11l-6.1 2.2L12 19l-1.9-5.8L4 11l6.1-2.2zM19 14l1.1 2.9L23 18l-2.9 1.1L19 22l-1.1-2.9L15 18l2.9-1.1zM5 2l.8 2.2L8 5l-2.2.8L5 8l-.8-2.2L2 5l2.2-.8z"/></symbol>
  <symbol id="icon-bar-chart" viewBox="0 0 24 24"><path d="M3 3v18h18M18 17V9M13 17V5M8 17v-3"/></symbol>
</svg>

<section class="hero decorated-section" aria-labelledby="home-title">
  ${self.decoration_layer('hero')}
  <div class="hero-copy">
    <p class="eyebrow"><span class="eyebrow-rule"></span> Creative Marketing Agency <span class="eyebrow-dot">·</span> Oman</p>
    <h1 id="home-title">Clear strategy.<br><span>Distinctive content.</span></h1>
    <p class="hero-description">We help businesses in Oman turn ideas into thoughtful marketing, compelling content, and distinctive visual experiences.</p>
    <div class="hero-actions">
      <a class="button button-primary" href="#services-work">Explore Our Services <span aria-hidden="true">↘</span></a>
      <a class="button button-text" href="#free-tools">Explore Free Tools <span aria-hidden="true">↗</span></a>
    </div>
    <p class="hero-location"><span aria-hidden="true">✳</span> Independent thinking, rooted in Oman.</p>
  </div>
  <div class="hero-composition" role="img" aria-label="An abstract composition of shapes in the agency's colors">
    <div class="composition-frame"><span class="frame-label">IDEAS INTO IMPACT</span><span class="frame-index">01 / 03</span>
      <div class="composition-disc"></div><div class="composition-arch"></div><div class="composition-block"></div><div class="composition-line"></div>
      <span class="composition-caption">STRATEGY<br>× CREATIVE</span>
    </div>
    <span class="composition-side-note">MUSCAT · OMAN</span>
  </div>
</section>

<section class="services-section section-shell decorated-section" id="services-work" aria-labelledby="services-title">
  ${self.decoration_layer('services')}
  <div class="section-intro">
    <p class="eyebrow">THINKING, THEN MAKING</p>
    <h2 id="services-title">From clear direction to creative execution.</h2>
    <p class="section-summary">Strategy, content, social media, and campaigns — working together for your brand.</p>
  </div>
  <div class="service-list">
    % for service in services:
      <article class="service-row">
        <div class="service-heading">
          ${self.icon(service['icon'], 'service-icon')}
          <div class="service-title-group">
            <h3>${service['title']}</h3>
            <p class="service-subtitle">${service['subtitle']}</p>
          </div>
        </div>
        <p class="service-description">${service['description']}</p>
      </article>
    % endfor
  </div>
  <div class="work-intro"><p class="eyebrow">A FEEL FOR THE POSSIBLE</p><p>Selected explorations</p></div>
  <div class="project-grid">
    % for project in projects:
      <article class="project-preview">
        <div class="project-art project-${project['style']}" aria-hidden="true">
          % if project['style'] == 'ritual':
            <div class="ritual-disc"></div><div class="ritual-vessel"></div><span class="project-art-note">MORNING<br>RITUALS</span>
          % else:
            <div class="road-sun"></div><div class="road-shape road-shape-back"></div><div class="road-shape road-shape-front"></div><span class="road-type">GO<br>FURTHER</span>
          % endif
          <span class="project-number">${project['number']}</span>
        </div>
        <div class="project-caption"><div><span class="project-type">${project['type']}</span><h3>${project['title']}</h3></div><span class="concept-tag">CONCEPT</span></div>
      </article>
    % endfor
  </div>
</section>

<section class="tools-section decorated-section" id="free-tools" aria-labelledby="tools-title">
  ${self.decoration_layer('tools')}
  <div class="tools-shell">
    <div class="tools-heading"><p class="eyebrow">GOOD THINKING, SHARED</p><h2 id="tools-title">Practical tools.<br><span>A clearer next step.</span></h2><p>Simple resources to help you plan your marketing, organize your content, and move forward independently.</p></div>
    <div class="tool-list">
      % for tool in tools:
        <article class="tool-row"><span class="tool-icon" aria-hidden="true">✳</span><div class="tool-copy"><h3>${tool['title']}</h3><p>${tool['description']}</p></div><span class="coming-soon">Coming soon</span></article>
      % endfor
    </div>
  </div>
</section>

<section class="about-section section-shell decorated-section" aria-labelledby="about-title">
  ${self.decoration_layer('about')}
  <p class="eyebrow">A LITTLE ABOUT HOW WE THINK</p>
  <div class="about-content"><h2 id="about-title">A thoughtful approach<br>to <span>brand growth.</span></h2><p>Based in Oman, we bring marketing thinking and creative production together to help businesses communicate clearly and show up with purpose.</p></div>
</section>

<section class="contact-section decorated-section" id="contact" aria-labelledby="contact-title">
  ${self.decoration_layer('contact')}
  <div class="contact-shell"><div class="contact-copy"><p class="eyebrow">START A CONVERSATION</p><h2 id="contact-title">Let’s create<br>your next move.</h2><p>Tell us what you’re building and where you need support.</p></div>
    <div class="contact-details">
      <div class="contact-detail"><span>BUSINESS EMAIL</span>
        % if agency['email']:
          <a href="mailto:${agency['email']}">${agency['email']}</a>
        % else:
          <p class="contact-placeholder">[Business email placeholder]</p>
        % endif
      </div>
      <div class="contact-detail"><span>WHATSAPP</span>
        % if agency['whatsapp_url']:
          <a href="${agency['whatsapp_url']}" target="_blank" rel="noopener noreferrer">Message us <span aria-hidden="true">↗</span></a>
        % else:
          <p class="contact-placeholder">[WhatsApp URL placeholder]</p>
        % endif
      </div>
    </div>
  </div>
</section>

<footer class="site-footer">
  <div class="footer-main"><div><a class="wordmark footer-wordmark" href="#top">${agency['name']}</a><p>${agency['positioning']}</p></div>
    <nav class="footer-navigation" aria-label="Footer navigation">
      % for item in navigation:
        <a href="${item['href']}">${item['label']}</a>
      % endfor
    </nav>
  </div>
  <div class="footer-bottom"><span>© ${year} ${agency['name']}. All rights reserved.</span><span>Based in Oman <span aria-hidden="true">✳</span></span></div>
</footer>
