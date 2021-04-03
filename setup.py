from setuptools import setup, find_packages
from setuptools.extension import Extension
import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


try:
    from Cython.Build import cythonize
except:
    install("cython")
    from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

extensions = [
    Extension(
        "sailboat_playground.*",
        ["sailboat_playground/*.py"],
    ),
    Extension(
        "sailboat_playground.engine.*",
        ["sailboat_playground/engine/*.py"],
    ),
    Extension(
        "sailboat_playground.visualization.*",
        ["sailboat_playground/visualization/*.py"],
    ),
    Extension(
        "sailboat_playground.visualization.resources.*",
        ["sailboat_playground/visualization/resources/*.py"],
    ),
]

setup(
    name="sailboat_playground",
    version="0.1.0",
    license="GPL-3.0",
    description="A very simple framework for sailboat simulation and autonomous navigation algorithms development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    author="Gabriel Gazola Milan",
    author_email="gabriel.gazola@poli.ufrj.br",
    url="https://github.com/gabriel-milan/sailboat-playground",
    include_package_data=True,
    keywords=[
        "framework",
        "python",
        "sailboat",
        "simulation",
        "autonomous navigation",
    ],
    install_requires=[
        "cython",
        "numpy",
        "pyglet==1.5.15",
        "pandas",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    ext_modules=cythonize(extensions, compiler_directives={
                          "language_level": "3"}),
)
