from setuptools import setup

with open('README.md') as fhandle:
    long_description = fhandle.read()


setup(
    name='rexutil',
    version='1.0.4',
    description='A python module for regular expression manipulations.',
    long_description=long_description,
    url="https://github.com/bdastur/rex",
    author="Behzad Dastur",
    author_email="bdastur@gmail.com",
    license='Apache Software License',
    classifier=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],

    keywords='re regular expression utility matching development',
    py_modules=['rex']
)

