from bddrest import response, status


def test_home_page(httpreq):
    with httpreq('/'):
        assert status == 200
        assert '<html lang="en">' in response.text
        assert (
            '<title>Mahnil Digital — Creative Marketing Agency · Oman</title>'
            in response.text
        )
        assert (
            '<h1 id="home-title"><span class="hero-title-line '
            'hero-title-line-first">Clear strategy.</span> '
            '<span class="hero-title-line hero-title-line-second">'
            '<span class="hero-title-accent">Distinctive</span> '
            'content.</span></h1>'
            in response.text
        )
        assert (
            'We help businesses in Oman turn ideas into thoughtful '
            'marketing, compelling content, and distinctive visual '
            'experiences.' in response.text
        )
        assert 'Independent thinking, rooted in Oman.' in response.text
        assert 'href="#services-work">Explore Our Services' in response.text
        assert 'href="#free-tools">Explore Free Tools' in response.text
        assert 'src="/media/' not in response.text
        assert (
            '<h2 id="services-title">From clear direction to creative '
            'execution.</h2>'
            in response.text
        )
        assert (
            'Strategy, content, social media, and campaigns — working '
            'together for your brand.'
            in response.text
        )
        assert 'href="#free-tools"' in response.text
        assert 'href="#services-work"' in response.text
        assert 'href="#contact"' in response.text
        for service in (
            'Direction', 'Marketing &amp; Brand Strategy',
            'Creation', 'Content &amp; Visual Production',
            'Presence', 'Social Media Management',
            'Growth', 'Digital Marketing &amp; Campaigns',
        ):
            assert service in response.text
        assert response.text.count('class="service-row"') == 4
        assert 'class="decorative-layer"' not in response.text
        assert 'hero-composition' not in response.text
        assert 'composition-disc' not in response.text
        assert 'road-sun' not in response.text
        assert 'ritual-vessel' not in response.text
        assert 'One-Page Marketing Plan' in response.text
        assert '30-Day Content Calendar' in response.text
        assert 'Mobile Video Checklist' in response.text
        assert '[Business email placeholder]' in response.text
        assert '[WhatsApp URL placeholder]' in response.text
        assert 'Concept Preview' in response.text
        assert 'Coming soon' in response.text


def test_home_page_rejects_unexpected_input(httpreq):
    with httpreq('/', query={'unexpected': 'value'}):
        assert status == 400
