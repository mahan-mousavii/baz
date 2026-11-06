"""Homepage copy and replaceable agency configuration."""

AGENCY = {
    'name': '[Agency Name]',
    'positioning': 'Thoughtful marketing. Distinctive creative.',
    'email': None,
    'whatsapp_url': None,
}

NAVIGATION = (
    {'label': 'Home', 'href': '#top'},
    {'label': 'Free Tools', 'href': '#free-tools'},
    {'label': 'Services & Work', 'href': '#services-work'},
    {'label': 'Contact', 'href': '#contact', 'cta': True},
)

SERVICES = (
    {
        'number': '01',
        'title': 'Marketing Strategy',
        'description': (
            'Clear direction for your brand, content, and campaigns.'
        ),
    },
    {
        'number': '02',
        'title': 'Content & Production',
        'description': (
            'Photography, video, and digital content crafted around your '
            'business.'
        ),
    },
    {
        'number': '03',
        'title': 'AI Creative Production',
        'description': (
            'Concept-led visuals and videos using AI as a creative tool.'
        ),
    },
)

PROJECTS = (
    {
        'number': '01',
        'title': 'A study in everyday ritual',
        'type': 'Visual identity · Concept Preview',
        'style': 'ritual',
    },
    {
        'number': '02',
        'title': 'Made for the open road',
        'type': 'Campaign direction · Concept Preview',
        'style': 'road',
    },
)

TOOLS = (
    {
        'title': 'One-Page Marketing Plan',
        'description': (
            'Bring your audience, message, and next steps into focus.'
        ),
    },
    {
        'title': '30-Day Content Calendar',
        'description': 'Turn a month of ideas into a simple, steady rhythm.',
    },
    {
        'title': 'Mobile Video Checklist',
        'description': (
            'A practical guide to planning your next phone-shot video.'
        ),
    },
)
