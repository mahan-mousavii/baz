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
        assert 'href="#free-tools"' in response.text
        assert 'href="#services-work"' in response.text
        assert 'href="#contact"' in response.text
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
