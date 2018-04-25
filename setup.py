import re,ast
from distutils.core import setup
from setuptools import find_packages

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('lycan/__init__.py', 'rb') as f:
    VERSION = str(ast.literal_eval(_version_re.search(
                    f.read().decode('utf-8')).group(1)))
setup(
    name='lycan',
    version=VERSION,
    packages=find_packages(exclude=["tests"]),
    license='MIT',
    include_package_data=True,
    long_description=open('README.md').read(),
    install_requires=[
        'six',
    ],
)
