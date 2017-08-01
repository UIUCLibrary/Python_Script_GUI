from setuptools import setup
import script_gui
import os


def get_metadata():
    metadata = {}
    metadata_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'script_gui', '__version__.py')
    with open(metadata_file, 'r', encoding='utf-8') as f:
        exec(f.read(), metadata)
    return metadata


def get_readme():
    with open('README.md', 'r', encoding='utf-8') as readme_file:
        return readme_file.read()


metadata = get_metadata()
readme = get_readme()

setup(
    name=metadata["__title__"],
    version=metadata["__version__"],
    url=metadata["__url__"],
    license=metadata["license_"],
    author=metadata["__author__"],
    author_email=metadata["__author_email__"],
    maintainer=metadata["maintainer"],
    maintainer_email=metadata["maintainer_email"],
    description=metadata["__description__"],
    download_url=metadata["download_url"],
    packages=["script_gui"],
    install_requires=["PyQt5"],
    long_description=readme

)
