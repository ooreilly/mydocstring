"""
mydocstring

Usage:
  mydocstring <file> <name> [-tmj] [-T=<tpl>]
  mydocstring -h | --help
  mydocstring --version

Options:
  -h --help                         Show help (this screen).
  --version                         Show version.
  -m --markdown                     Output extracted docstring as Markdown.
  -t --text                         Output extracted docstring as plain-text.
  -j --json                         Output extracted docstring as JSON.
  -T=<tpl> --template=<tpl>         Set template for Markdown output.

Examples:
  Extract the module docstring
    mydocstring module.py . --markdown
  Extract a module function docstring
    mydocstring module.py function --markdown
  Extract a class docstring
    mydocstring module.py Class --markdown
  Extract a method docstring
    mydocstring module.py Class.method --markdown

Help:
  Please see the issue tracker for the Github repository:
  https://github.com/ooreilly/docstringout
"""
from docopt import docopt
from . import command

def main():
    """
    Program main
    """
    options = docopt(__doc__)
    cmd = command.Command(options)

    for opt in options:
        if options[opt]:
            cmd(opt)

