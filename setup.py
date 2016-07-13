from setuptools import setup, find_packages

__version__ = "0.7"


install_requires = [
    'pykwalify',
    'PyYAML',
    'future',
    'docopt',
    'docker-py',
]

extras_require = {
    'django': ['django', 'django-form-utils'],
}

scripts = [
    'bin/kliko-validate',
    'bin/kliko-run',
]

setup(
    name="kliko",
    version=__version__,
    packages=find_packages(),
    scripts=scripts,
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
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Emulators",
        "Topic :: System :: Operating System Kernels :: Linux",
        ]
)
