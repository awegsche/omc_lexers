# omc_lexers

[Pygments](https://pygments.org/) lexers for various OMC related languages / file formats.

## Currently supported

- [MadX](http://madx.web.cern.ch/madx/) (**work in progress**)

## Prerequisites

Python3 and, obviously, Pygments.

## Installation

Checkout the repository via git:

```shell
git clone git@github.com:awegsche/omc_lexers.git
```

and install it via pip into the current python envirionment:

```shell
pip install omc_lexers
```

This automatically registers the lexers with `pygments`.

## Usage

For a detailled description, please consult the [Pygments homepage](https://pygments.org/) and its [FAQ](https://pygments.org/faq/).

Once installed, it's as simple as

```shell
python -m pygments file.madx
```

or (on systems where this works, I couldn't get it running on Win10):

```shell
pygmentize file.madx
```
