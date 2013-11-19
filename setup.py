from distutils.core import setup
from setuptools import setup, find_packages

long_desc = '''
This package enable embedding yuml diagrams on your Sphinx documentation.

Example::

    .. yuml:: 
       :alt: [Customer]->[Billing Address]
       :type: class

       [Customer]->[Billing Address]

'''

setup(
    name='sphinxcontrib-yuml',
    version='0.3',
    url='https://github.com/njouanin/sphinxcontrib-yuml',
    packages=find_packages(),
    license='GPLv3',
	description='Sphinx extension for embedding yuml diagram in documentations',
    long_description=long_desc,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
)
