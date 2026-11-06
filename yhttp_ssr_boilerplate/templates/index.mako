<%inherit file="master.mako" />

<%block name="head">
  <meta property="og:title" content="${agency['name']} — Creative Marketing Agency · Oman">
  <meta property="og:description" content="${agency['positioning']} Based in Oman.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="${settings.publicurl.rstrip('/')}/">
</%block>

<section class="hero" aria-labelledby="home-title">
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

<section class="services-section section-shell" id="services-work" aria-labelledby="services-title">
  <div class="section-intro">
    <p class="eyebrow">THINKING, THEN MAKING</p>
    <h2 id="services-title">Strategy meets<br><span>creative execution.</span></h2>
    <p class="section-summary">One clear point of view, carried through every part of how your business shows up.</p>
  </div>
  <div class="service-list">
    % for service in services:
      <article class="service-row">
        <span class="service-number">${service['number']}</span>
        <h3>${service['title']}</h3>
        <p>${service['description']}</p>
        <span class="service-mark" aria-hidden="true">↗</span>
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

<section class="tools-section" id="free-tools" aria-labelledby="tools-title">
  <div class="tools-shell">
    <div class="tools-heading"><p class="eyebrow">GOOD THINKING, SHARED</p><h2 id="tools-title">Practical tools.<br><span>A clearer next step.</span></h2><p>Simple resources to help you plan your marketing, organize your content, and move forward independently.</p></div>
    <div class="tool-list">
      % for tool in tools:
        <article class="tool-row"><span class="tool-icon" aria-hidden="true">✳</span><div class="tool-copy"><h3>${tool['title']}</h3><p>${tool['description']}</p></div><span class="coming-soon">Coming soon</span></article>
      % endfor
    </div>
  </div>
</section>

<section class="about-section section-shell" aria-labelledby="about-title">
  <p class="eyebrow">A LITTLE ABOUT HOW WE THINK</p>
  <div class="about-content"><h2 id="about-title">A thoughtful approach<br>to <span>brand growth.</span></h2><p>Based in Oman, we bring marketing thinking and creative production together to help businesses communicate clearly and show up with purpose.</p></div>
</section>

<section class="contact-section" id="contact" aria-labelledby="contact-title">
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
