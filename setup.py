from setuptools import setup
from setuptools import find_packages

VERSION = '0.0.13'

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pytfc',
    version=VERSION,
    author='Alex Basista',
    author_email='alex.basista@gmail.com',
    url='https://github.com/alexbasista/pytfc',
    description='Python HTTP client library for Terraform Cloud/Enterprise API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files=['LICENSE'],
    py_modules=['pytfc'],
    packages=find_packages(),
    install_requires=[
        'pyhcl>=0.4.4',
        'requests>=2.26.0',
    ],
    keywords=['tfe', 'terraform enterprise', 'tfc', 'terraform cloud', 'terraform'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
    ],
)
