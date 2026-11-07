from bddrest import response, status


def test_home_page(httpreq):
    with httpreq('/'):
        assert status == 200
        assert '<html lang="en">' in response.text
        assert (
            '<title>[Agency Name] — Creative Marketing Agency · Oman</title>'
            in response.text
        )
        assert (
            '<h1 id="home-title">Clear strategy.<br>'
            '<span>Distinctive content.</span></h1>'
            in response.text
        )
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
        assert response.text.count('class="decorative-layer"') == 5
        for icon in (
            'decor-camera', 'decor-sparkles', 'decor-clapperboard',
            'decor-pen-tool', 'decor-megaphone', 'decor-message-circle',
            'decor-aperture', 'decor-bar-chart', 'decor-video',
        ):
            assert icon in response.text
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
