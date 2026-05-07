#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='irctc-railway-booking-bot',
    version='1.0.0',
    author='blackcop1',
    author_email='tushar.24mei10102@vitbhopal.ac.in',
    description='High-speed railway booking automation bot with smart timing and captcha bypass',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blackcop1/irctc-railway-booking-bot',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.9',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'irctc-bot=src.main:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
