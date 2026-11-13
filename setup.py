import os
import re

from setuptools import find_packages, setup


root = os.path.dirname(__file__)
with open(os.path.join(root, 'mahnil', 'manifest.py')) as f:
    version = re.compile(r".*__version__ = '(.*?)'", re.S).match(
        f.read(),
    ).group(1)

setup(
    name='mahnil',
    version=version,
    description='Mahnil Digital creative agency website and CMS.',
    packages=find_packages(where='.', exclude=['tests']),
    package_data={
        'mahnil': [
            'templates/**/*.mako',
            'dbmigration/*.py',
        ],
    },
    install_requires=[
        'yhttp >= 9.4.2, < 10',
        'yhttp-mako >= 3.1, < 4',
        'yhttp-auth >= 11.1, < 12',
        'yhttp-dbmanager >= 9.1, < 10',
        'yhttp-media >= 4.1, < 5',
        'yhttp-sqlalchemy >= 6.1, < 7',
        'boto3 >= 1.34, < 2',
        'Pillow >= 10, < 13',
    ],
    entry_points={
        'console_scripts': [
            'mahnil = mahnil:app.climain',
        ],
    },
    python_requires='>=3.11',
)
