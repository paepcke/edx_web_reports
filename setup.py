import multiprocessing
from setuptools import setup, find_packages
setup(
    name = "edx_web_reports",
    version = "0.1",
    packages = find_packages(),

    setup_requires   = [],
    install_requires = [#'pymysql_utils>=0.33',
			#'configparser>=0.7.0',
			'django-htmlmin>=0.3',
			'html5lib>=0.999',
			'beautifulsoup4>=4.3.2',
			],
    tests_require    = ['sentinels>=0.0.6', 'nose>=1.0'],

    # Unit tests; they are initiated via 'python setup.py test'
    test_suite       = 'nose.collector', 

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
     #   '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
     #   'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Andreas Paepcke",
    author_email = "paepcke@cs.stanford.edu",
    description = "Wrapper for Highcharts JavaScript/D3 charting lib.",
    license = "BSD",
    keywords = "Highcharts, Visualization",
    url = "git@github.com:paepcke/edx_web_reports.git",   # project home page, if any
)
