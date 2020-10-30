import os.path
import re
from setuptools import setup

(__version__, ) = re.findall("__version__.*\s*=\s*[']([^']+)[']",
                             open('python_tuples_to_sql/__init__.py').read())

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name="python_tuples_to_sql",
    version=__version__,
    description="Generate sql from python tuples",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["python_tuples_to_sql"],
    install_requires=[],
)
