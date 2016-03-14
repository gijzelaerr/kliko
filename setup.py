from setuptools import setup, find_packages

from kliko.version import __version__

install_requires = [
    'pykwalify',
    'PyYAML',
    'future',
    'docopt'
]

extras_require = {
    'django': ['django', 'django-form-utils'],
    'docker': ['docker-py'],
}


setup(
    name="kliko",
    version=__version__,
    packages=find_packages(),
    scripts=['bin/kliko-validate.py'],
    install_requires=install_requires,
    extras_require=extras_require,
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
