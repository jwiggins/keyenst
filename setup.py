from distutils.util import convert_path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="Enstaller",
    version="1.0.0",
    author="Enthought, Inc.",
    author_email="info@enthought.com",
    url = "https://github.com/enthought/enstaller",
    license="BSD",
    description = "Install and managing tool for egg-based packages",
    py_modules = [
        'patcher.py'
    ],
    packages = [
        'egginst',
    ],
    entry_points = {
        "console_scripts": [
             "egginst = egginst.main:main",
        ],
    },
    classifiers = [
        "License :: OSI Approved :: BSD License",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
    ],
)
