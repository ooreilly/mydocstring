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

    Attributes:
        argdelimiter : A string that specifies how to separate arguments in a
            argument list. Defaults to `':'`.
        secdelimiter : A string that is used to identify a section and is placed
            after the section name (e.g., `Arguments:`). Defaults to `': '`. 
        indent : An int that specifies the minimum number of spaces to use for
            indentation.


    """

    def __init__(self, docstring):
        self.docstring = docstring
        self.argdelimiter = ': '
        self.secdelimiter = ':' 
        self.indent = 2

    def parse(self):
        """
        This method should be overloaded and perform the parsing of all
        sections.
        """
        pass

    def args(self, keywords=''):
        """
        This method should be overloaded to specify how to parse the argument
        section.
        """
        pass

    def returns(self, keywords=''):
        """
        This method should be overloaded to specify how to parse the return
        section.
        """
        pass

    def section(self, keywords=''):
        """
        This method should be overloaded to specify how to extract a section.
        """
        pass

    def arglist(self, keywords=''):
        """
        This method should be overloaded to specify how to parse an argument
        list.
        """
        pass


class GoogleDocString(DocString):
    """
    This is the base class for parsing docstrings that are formatted according
    to the Google style guide: .

    """

    def parse(self):
        docstr = {}
        docstr['args'] = self.args('Args|Arguments')
        #docstr['returns'] = self.returns('Returns')
        return docstr

    def section(self, keywords=''):
        import warnings
        import textwrap
        docstring = textwrap.dedent(self.docstring).strip()

        # A section starts with `keyword` + delimiter and the contents of the
        # section are indented. The section ends after the indent.
        pattern = r'(?:%s)%s\n((?:^\s{%s,}.*\n)*)'%(keywords, self.secdelimiter,
                  self.indent)
        matches = re.compile(pattern, re.M).findall(docstring)

        if not matches:
            warnings.warn(r'Unable to find section `%s`' %
                          keywords)
            return None
        return textwrap.dedent(matches[0])

    def args(self, keywords='Args|Arguments'):
        """
        Parses the argument list of a section in the docstring.

        Args:
            keywords (str, optional): This string specifies all aliases for the
                block to parse. Each alias is separated by |. Defaults to
                `'Args|Arguments'`.

        Notes:
            This method can be used to parse any section that is formatted as:

            Keyword:
                arg1 (optional signature): This is a single line description.
                arg2 : This is an example of description that is too long to fit
                    on a single line. For multiline descriptions to work, each
                    new line must be indented by at least two spaces.

        """
        return self.arglist(self.section(keywords))

    def returns(self):
        pass

    def arglist(self, section):
        # Parse arguments
        # The format is `variable (optional signature): description`. The
        # variable and signature is separated from the description using `: `
        # (including space). Space in the separator is needed to to ensure there
        # is no clash with restructured text syntax (e.g., :any:). Multiline
        # line descriptions must be indented using at least two spaces.
        pattern = r'^(\w*)\s*(?:\((.*)\))*\s*:\s(.*\n(?:^\s{2,}.*)*)'
        matches = re.compile(pattern, re.M).findall(section)

        if not matches:
            raise ValueError('Failed to parse argument list:\n `%s` ' %
                             (section))

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
    parser = parser(obj['docstring'])
    docstr = parser.parse()
    return docstr

