import os
import glob
import codecs
import pathlib
from setuptools import setup, find_packages


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


def get_css():
    return glob.glob("asched/static/css/*.css")


def get_js():
    return glob.glob("asched/static/js/*.js")


def get_html():
    return glob.glob("asched/templates/*.html")


def get_sqlite():
    return glob.glob("asched/static/tables/*.sqlite")


setup(
    name="asched",
    version=get_version("asched/__init__.py"),
    description=("Simple assignment scheduler."),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/frankhart2018/assignment-scheduler",
    author="Siddhartha Dhar Choudhury",
    author_email="sdharchou@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
    ],
    packages=[package for package in find_packages()],
    package_data={"asched": get_css() + get_js() + get_html() + get_sqlite(),},
    entry_points={"console_scripts": ["asched = asched.run_app:run_app",]},
    install_requires=["flask"],
)
