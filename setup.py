from distutils.core import setup
from setuptools import setup, find_packages

long_desc = '''
This package enable embedding yuml diagrams on your Sphinx documentation.

Example::

    .. yuml:: 
       :alt: [Customer]->[Billing Address]
       :type: class, activity or usecase
       :scale: positive integer value
       :direction: LR, TD or RL
       :style: boring, plain, scruffy

       [Customer]->[Billing Address]

'''

setup(
    name='sphinxcontrib-yuml',
    version='0.1',
    url='https://github.com/njouanin/sphinxcontrib-yuml',
    packages=find_packages(),
    license='GPLv3',
	description='Sphinx extension yuml',
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