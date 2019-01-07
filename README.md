# MyDocstring
[MyDocstring](README.md) is a small Python package that allows you to extract and parse docstrings. It suited for building your own documentation system. Docstrings can be displayed as either plain-text, [Markdown](http://commonmark.org/), or [JSON](https://www.json.org/) data.

* Supports [Python PEP484 type hints](https://www.python.org/dev/peps/pep-0484/).
* Supports [pybind11](https://github.com/pybind/pybind11) docstrings.
* Supports [Google-style docstrings](http://google.github.io/styleguide/pyguide.html).
* Produces [JSON](https://www.json.org/), plain-text, and [Markdown](http://commonmark.org/) output for modules, classes, functions, and
  methods.

## Getting Started
If you are interested in building a documentation solution for your own
project, a good place to
start is this [tutorial](tutorials/begin.ipynb). This tutorial will teach you
how to extract and parse docstrings. 

If you are after a complete documentation solution, then see the
[showcase](#showcase) section that features solutions built on *MyDocstring*.

The project also comes with a command line tool that serves as an example of
what you can build with the package. See [here](examples/README.md) for learning
how to use the command line tool and to see some example output.

## Installation
The package is available on the Python packaging index [PyPi](https://pypi.python.org/pypi) and can be installed via pip as follows.
```bash
$ pip install mydocstring
```

## Dependencies
This project uses:
* [docopt](http://docopt.org/) for the command line interface application. 
* [mako](http://www.makotemplates.org/) for producing markdown templates.
* [pytest](https://docs.pytest.org/en/latest/) for testing.

## Issues
If you are having problems extracting your docstrings, or parts of their content
end up missing, then please make sure that your are only using spaces (no tabs).
Four spaces should be used for each level of indentation.
Also, make sure that you conform to the [Google style
guide](http://google.github.io/styleguide/pyguide.html) when writing your
docstrings. 

Otherwise, please submit a new issue using the [issue tracker](https://github.com/ooreilly/mydocstring/issues) and explain the problem. 

## Contributing
Contributions are more than welcome. Please reach out via the issue tracker to
discuss and also see [here](CONTRIBUTING.md) for
some guidelines.

##  Showcase 
If you end up using this tool in your project in one way or another. I would
love to hear about it and showcase it here. Please go ahead and make a pull
request. 

* [NetKet](https://www.netket.org) is an open-source project for machine learning and
  many-body quantum systems. It uses *mydocstring* for generating reference
  documentation from [pybind11](https://github.com/pybind/pybind11) docstrings.
  See
  [here](https://github.com/netket/netket/tree/v2.0/Docs) for the source. 

## License

This project is licensed under the MIT License - see the
[LICENSE.md](LICENSE.md) file for details.
