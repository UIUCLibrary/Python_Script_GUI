from setuptools import setup
import script_gui

setup(
    name=script_gui.__title__,
    version=script_gui.__version__,
    license='University of Illinois/NCSA Open Source License',
    url=script_gui.__url__,
    author=script_gui.__author__,
    author_email=script_gui.__author_email__,
    packages=["script_gui"],
    install_requires=["PyQt5"],
    description=script_gui.__description__


)