# Docstring
[Docstring](README.md) is a small Python package that allows you to extract docstrings from
source code and display them as plain-text, markdown, or JSON data. It is meant
to serve as a basic building-block for building customized documentation
systems. Simply put, [Docstring](README.md) extracts and parses docstrings and
gives you access to their data so you can decide what you want to do with it.

* Support for `Python` code  (support `C` is planned).
* Support for [Google-style docstrings](http://google.github.io/styleguide/pyguide.html)
* Produces [JSON](https://www.json.org/), plain-text, and [markdown](http://commonmark.org/) output for modules, classes, functions, and
  methods.

## Contents
  * [Getting Started](#getting-started)
    * [Usage](#usage)
    * [Python Examples](#python-examples)
    * [Installing](#installing)
    * [Dependencies](#dependencies)
    * [Troubleshooting](#troubleshooting)
  * [Contributing](#contributing)
    * [Showcase](#showcase)
    * [Pull requests](#pull-requests)
    * [Running tests](#running-tests)
  * [License](#license)

## Getting Started
Once [installed](#installing), you can begin extracting and converting docstrings using the
command-line interface application `docstring`. 

### Usage

```
$ docstring --help
docstring

Usage:
  docstring <file> <name> [-tmj] [-T=<tpl>]
  docstring -h | --help
  docstring --version

Options:
  -h --help                         Show help (this screen).
  --version                         Show version.
  -m --markdown                     Output extracted docstring as Markdown.
  -t --text                         Output extracted docstring as plain-text.
  -j --json                         Output extracted docstring as JSON.
  -T=<tpl> --template=<tpl>         Set template for Markdown output.

Examples:
  Extract the module docstring
    docstring module.py . --markdown
  Extract a module function docstring
    docstring module.py function --markdown
  Extract a class docstring
    docstring module.py Class --markdown
  Extract a method docstring
    docstring module.py Class.method --markdown

Help:
  Please see the issue tracker for the Github repository:
  https://github.com/ooreilly/docstring
```

```python
def example_function(arg1, arg2=1):
    """
    This is an example of a docstring that conforms to the Google style guide. 
    The indentation uses four spaces (no tabs). Note that each section starts
    with a header such as `Arguments` or `Returns` and its contents is indented.

    Arguments:

        arg1 (`int`): This description for this argument fits on one line.
        arg2 (`int`, optional): This description is too long to fit on a
            single line. Note that it is continued by being indented. 

    Returns:

        `bool` :  Stating the return type here is optional.

        We can continue putting explanations in this section as long as the text
        is indented.

    This text is no longer indented and therefore not part of the `Returns`
    section.

    Raises:

        ValueError: This is exception is raised when arg1 and arg2 are equal.

    """
    if arg1 == arg2:
        raise ValueError("`arg1` and `arg2` cannot be equal.")
    if arg1 > arg2:
        return True
    else: 
        return False
```

#### Plain-text

Next, we extract the docstring for the function above and output it as
plain-text by calling
```
$ docstring examples/example.py example_function --text  > examples/example_py.txt

```
Go to [examples/example.txt](examples/example_py.txt) to view the output.

#### Markdown
To output markdown, we simply call

```
$ docstring examples/example.py --markdown > examples/example_py.md

```
Go to [examples/example_py.md](examples/example_py.md) to
view the output. 

#### Customization

If you are not satisfied with the resulting markdown, you can provide your own
[mako](http://makotemplates.org) template
```
$ docstring examples/example.py example_function --markdown --template customization.md

```
Go to [docstring/templates/](docstring/templates/) to see how to make your own
template. 

#### JSON

Another possibility is to output JSON data (then its up to you how you to
format the data)

```
$ docstring examples/example.py --json > examples/example_py.md

```
Go to [examples/example_py.json](examples/example_py.json) to
view the output for this example.

### Installing
Use setup tools or pip to install this package.

```bash
$ pip install docstring
```
*or*
```bash
$ sudo python setup.py install 
```

### Dependencies
This project uses:
* [docopt](http://docopt.org/) for the command-line interface application. 
* [mako](http://www.makotemplates.org/) for producing markdown templates.
* [pytest](https://docs.pytest.org/en/latest/) for testing.

### Troubleshooting
If you are having problems extracting your docstrings, or parts of their content
end up missing. Please make sure that your are only using spaces (no tabs).
Four spaces should be used for each level of indentation as stated in PEP .
Also, make sure that you conform to the [Google style
guide](http://google.github.io/styleguide/pyguide.html) when writing your
docstrings. It's easy to forget indentation or mess something else up! 

That said, this tool likely breaks for some edge-cases and it is completely
possible that you have discovered a bug. Please see the issue tracker to see if
this problem is known. If not, please submit a new issue with a minimum example
that introduces the problem and also what the excepted output is supposed to be.


## Contributing
###  Showcase 
If you end up using this tool in your project in one way or another. I would
love to hear about it and showcase it here. Please go ahead and make a pull
request. 

## Pull requests
You are more than welcome to contribute to this project. In fact, getting some help
developing and maintaining this package would be fantastic! Please use the issue
tracker to look for any issues you think you can resolve, or feel free to post a
new issue if you want to suggest a new feature. Ideally, post a feature
request to discuss it before you implement it and make a pull request. 

If you are contributing new code, then 
1. First, fork the repository and create your own branch. Commit your changes to
   this branch. 
2. In your commit, please include a test case that demonstrates that your
   contribution works as expected using `pytest`.
   Having a test case will make it easier to review your code and therefore lead
   to your pull request being approved faster.  Please also use `pylint` to check
   for issues. During development it is usually simplest to disable
   reports via `pylint my_feature.py --reports=n` and then enable again once all
   issues have been corrected. Make sure that you test all parts of your code
   using a coverage tool such as `py-cov`.
3. Update [ACKNOWLEDGMENTS](ACKNOWLEDGMENTS.md) to make sure you get credit for
   your contribution. 
4. Update [README](README.md) to explain how to use your feature.
5. Make all your commits to your feature branch and check that all tests pass.
   Then go ahead and submit a pull request! 

## Running tests
[Pytest](https://docs.pytest.org/en/latest/) is used for testing. Currently, the
tests are quite limited in scope. More tests should definitely be developed to identify
edge cases and facilitate future code refactoring. 

To run the tests, go to the `docstring` directory and type

```bash
$ pytest
```
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
