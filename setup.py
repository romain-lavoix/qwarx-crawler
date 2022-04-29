# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name='qwarx_spiders',
    version='1.0',
    packages=find_packages(),
    package_data={
        'qwarx_spiders': ['resources/*']
    },
    entry_points={'scrapy': ['settings = qwarx_spiders.settings']},
)
