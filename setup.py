try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import rex

rex_classifiers = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Intended Audience :: Developers",
    "License :: Apache License",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

with open("DESCRIPTION.rst", "r") as fp:
    rex_long_description = fp.read()

setup(name="rex",
      version=rex.__version__,
      author="Behzad Dastur",
      url="http://pypi.python.org/pypi/rex/",
      py_modules=["rex"],
      description="Python 2,3 string & regular expression matching utility",
      long_description=rex_long_description,
      license="Apache",
      classifiers=rex_classifiers
      )

    keywords='re regularexpressions utility matching development',

