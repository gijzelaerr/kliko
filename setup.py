from setuptools import setup, find_packages

from kliko.version import __version__

setup(
    name="kliko",
    version=__version__,
    packages=find_packages(),
    scripts=[],
    install_requires=['pykwalify', 'PyYAML', 'docker-py', 'future'],

    package_data={
        '': ['*.txt', '*.rst'],
        'kliko': ['schemas/*.yml'],
    },

    author="Gijs Molenaar",
    author_email="gijs@pythonic.nl",
    description="Scientific Compute Container Spec Parser",
    license="GPL2",
    keywords="science docker yaml json",
    url="https://github.com/gijzelaerr/kliko",
)
