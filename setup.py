from setuptools import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pytfc',
    version='0.1.0',
    author='Alex Basista',
    author_email='alex.basista@gmail.com',
    description='Python HTTP client library for Terraform Cloud/Enterprise API.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/alexbasista/pytfc',
    py_modules=["pytfc"],
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        #"pyhcl>=0.4.4",
        "requests>=2.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "wheel>=0.37",
            "setuptools>=58.2",
            "twine>=3.4.2",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
    ],
)
