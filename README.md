# MyDocstring
[MyDocstring](README.md) is a small Python package that allows you to extract docstrings display them as either plain-text, [markdown](http://commonmark.org/), or [JSON](https://www.json.org/) data.

* Support for Python-code  (support for C-code is planned).
* Support for [Google-style docstrings](http://google.github.io/styleguide/pyguide.html)
* Produces [JSON](https://www.json.org/), plain-text, and [markdown](http://commonmark.org/) output for modules, classes, functions, and
  methods.

## Getting Started
You can begin extracting and converting docstrings using the command line tool
`mydocstring` that comes with package. Simply type `mydocstring --help` to see how to use it. 

Let's extract the docstring from the following example code and convert it to
markdown:
```python
def example_function(arg1, arg2=1):
    """
    This is an example of a Google-style docstring.

    Arguments:

        arg1 (`int`): This description for this argument fits on one line.
        arg2 (`int`, optional): This description is too long to fit on a
            single line. Note that it is continued by being indented. 
    """
    pass
```
A more detailed example code is found in [examples/example.py](examples/example.py).

```
$ docstring examples/example.py example_function --markdown > examples/example_py.md
```
Go to [examples/example_py.md](examples/example_py.md) to
view the output. If you are not satisfied with the resulting markdown, you can provide your own
[mako](http://makotemplates.org) template

```
$ docstring examples/example.py example_function --markdown --template customization.md
```
Go to [mydocstring/templates/](mydocstring/templates/) to see how to make your own
template. 

It is also possible to output plain-text, or JSON-data using the flags args
`--text` and `--json`. Example output can be found [here](examples/).


## Installation
The package is available on the Python packaging index [PyPi](https://pypi.python.org/pypi) and can be installed via pip as follows.
```bash
$ pip install mydocstring
```

## Dependencies
This project uses:
* [docopt](http://docopt.org/) for the command-line interface application. 
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
discuss and also see [here](contributing.md) for
some guidelines.

##  Showcase 
If you end up using this tool in your project in one way or another. I would
love to hear about it and showcase it here. Please go ahead and make a pull
request. 

## Acknowledgments
These are some projects that inspired me to develop this tool. 
* [pdoc](https://github.com/BurntSushi/pdoc/) A tool for auto-generating API
  documentation for Python libraries.
* [mkdocs](http://www.mkdocs.org/) Static site generator for building
  documentation using markdown. 
* [moxygen](https://github.com/sourcey/moxygen) Doxygen XML to Markdown
  converter.
* [napoleon](https://pypi.python.org/pypi/sphinxcontrib-napoleon) Sphinx
  extension that can parse numpy and Google-style docstrings.
* [pypydoxify](https://pypi.python.org/pypi/doxypypy/0.8.8.6) Converts Python
  comments into Doxygen's syntax.
* [docsify](https://github.com/QingWei-Li/docsify/) Markdown-based documentation
  site generator.

## License

This project is licensed under the MIT License - see the
[LICENSE.md](LICENSE.md) file for details.
