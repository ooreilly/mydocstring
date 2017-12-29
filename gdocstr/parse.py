"""
This module provides parsers for parsing different docstring formats.  The
parsers work on docstring data objects that are constructed using the `extract`
module. After parsing, the data of docstring is stored in a dictionary. This
data can for instance be serialized using JSON, or rendered to markdown.
"""
import re

class DocString(object):
    """
    This is the base class for parsing docstrings.
    """

    def __init__(self, docstring):
        self.docstring = docstring

    def args(self, keywords=''):
        """
        This method should be overloaded to specify how to parse argument
        blocks.
        """
        pass

class GoogleDocString(DocString):
    """
    This is the base class for parsing docstrings that are formatted according
    to the Google style guide: .

    """

    def args(self, keywords='Args|Arguments'):
        """
        Parses an argument block in the docstring.

        This method can be used to parse any block that is formatted as:

        Keyword:
            arg1 (optional signature): This is a single line description.
            arg2 : This is an example of description that is too long to fit on
                a single line. For multiline descriptions to work, each new line
                must be indented by at least two spaces.

        Args:
            keywords (str, optional): This string specifies all aliases for the
                block to parse. Each alias is separated by |. Defaults to
                `'Args|Arguments'`.

        """
        import warnings
        import textwrap
        docstring = textwrap.dedent(self.docstring).strip()
        # Get the argument block The argument block ends after a new line, or is
        # the last part of the docstring.
        pattern = r'(?:%s):\n([\w\W]*)(?:\n[^.])?'%keywords
        matches = re.compile(pattern, re.M).findall(docstring)

        if not matches:
            warnings.warn(r'Unable to find argument list for `%s`' %
                          self.docstring['query'])
            return None
        argblock = textwrap.dedent(matches[0])

        # Parse arguments
        # The format is `variable (optional signature): description`. The
        # variable and signature is separated from the description using `: `
        # (including space). Space in the separator is needed to to ensure there
        # is no clash with restructured text syntax (e.g., :any:). Multiline
        # line descriptions must be indented using at least two spaces.
        pattern = r'(\w*)\s*(?:\((.*)\))*\s*:\s(.*\n(?:\s{2,}.*)*)'
        matches = re.compile(pattern, re.M).findall(argblock)

        if not matches:
            raise ValueError('Failed to parse argument block:\n `%s` ' %
                             (argblock))

        argsout = []
        for match in matches:
            argsout.append({'name' : match[0], 'signature' : match[1],
                            'description' : match[2].strip()})
        return argsout


def parse(obj, parser=GoogleDocString):
    """
    Parses a docstring using a parser that matches the formatting of the
    docstring.

    Args:
        obj : A dictionary that contains the docstring and other properties.
            This object is typically obtained by calling the `extract` function.

    """
    docstr = {}
    parser = parser(obj['docstring'])
    docstr['args'] = parser.args()
    return docstr

