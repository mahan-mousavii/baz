"""Homepage copy and replaceable agency configuration."""

AGENCY = {
    'name': 'Mahnil Digital',
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
        'title': 'Direction',
        'subtitle': 'Marketing & Brand Strategy',
        'description': (
            'We define your audience, sharpen your message, and build '
            'practical marketing plans that give your brand a clear '
            'direction — from positioning to campaign planning.'
        ),
        'icon': 'compass',
    },
    {
        'title': 'Creation',
        'subtitle': 'Content & Visual Production',
        'description': (
            'We turn ideas into photography, video, social content, and '
            'AI-powered visuals — bringing your brand’s personality and '
            'message to life through thoughtful creative production.'
        ),
        'icon': 'clapperboard',
    },
    {
        'title': 'Presence',
        'subtitle': 'Social Media Management',
        'description': (
            'We plan, create, and publish consistent social content, '
            'keeping your brand’s voice cohesive and using performance '
            'insights to refine its presence over time.'
        ),
        'icon': 'message-circle',
    },
    {
        'title': 'Growth',
        'subtitle': 'Digital Marketing & Campaigns',
        'description': (
            'We plan and manage digital campaigns that connect your brand '
            'with relevant audiences, then measure and refine performance '
            'to encourage meaningful enquiries and action.'
        ),
        'icon': 'trending-up',
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
