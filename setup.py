"""
flask-validation-extended
-------------
Get and validate all Flask input parameters with easily!
"""

from setuptools import setup
from flask_validation_extended import __VERSION__

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flask-validation-extended',
    version=__VERSION__,
    description='Get and validate all Flask input parameters with easily!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/iml1111/flask-validation-extended',
    author='IML',
    author_email='shin10256@gmail.com',
    license='MIT',
    keywords='flask validation extended',
    packages=['flask_validation_extended'],
    install_requires=['flask'],
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)