# Sailboat Playground

Language: [EN](#) (incomplete) / [PT-BR](README_br.md) (completo)

A very simple framework for developing autonomous sailing algorithms and testing them with 2D simulations/visualizations.

## Getting started

There are two ways to install this on your machine:

### Option #1 - From GitHub repository (recommended)

Using this method, you'll be able to execute the examples as they are, with no further changes required.

- Clone this repository

```
https://github.com/gabriel-milan/sailboat-playground
```

- `cd` into the cloned repository and install it

```
python3 -m pip install .
```

- And it's done! If you want to run the `upwind` example, do

```
python3 examples/upwind/sailing_upwind.py
```

### Option #2 - From PyPI

This package is also available on PyPI, but you'll need to create your own environment and boat configuration files before you use it.

- Install from PyPI:

```
python3 -m pip install sailboat_playground
```

## Basic usage

This framework is split in two main modules: `engine` and `visualization`.

The `engine` module handles the simulation and generates files with simulation data for later debugging and visualization. The main class of the engine is the `Manager` class. There, you need to provide both boat and environment configuration files

Work in progress... (will write this one in PT-BR first)