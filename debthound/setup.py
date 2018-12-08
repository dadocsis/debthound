from setuptools import setup, find_packages

__version__ = '0.1'


setup(
    name='debthound',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-restful',
        'flask-migrate',
        'flask-jwt-extended',
        'flask-marshmallow',
        'marshmallow-sqlalchemy',
        'python-dotenv',
        'passlib',
        'alembic',
        'sqlalchemy',
        'pymysql',
        'scrapy',
        'scrapyd',
        'schedule'
    ],
    entry_points={
        'console_scripts': [
            'web_api = web_api.manage:cli'
        ],
        'scrapy': ['settings = scrapers.settings']
    }
)
