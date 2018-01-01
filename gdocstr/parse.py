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
        self.header = {}
        # Copy header data from docstring
        for doc in docstring:
            if doc != 'docstring':
                self.header[doc] = docstring[doc]
        self.docstring = docstring['docstring']
        self.headers = ''
        self.data = []
        self.mdtemplate = ''

    def parse(self):
        """
        This method should be overloaded and perform the parsing of all
        sections.
        """
        self.data = []
        sections = self.extract_sections()
        for section in sections:
            self.data.append(self.parse_section(section))
        return self.data

    def extract_sections(self):
        """
        This method should be overloaded to specify how to extract sections.
        """
        pass

    def parse_section(self, section):
        """
        This method should be overloaded to specify how to parse a section.
        """
        pass

    def __json__(self):
        """
        Output docstring as JSON data.
        """
        import json

        data = self.data
        data.append(self.header)
        return json.dumps(self.data, sort_keys=True,
                          indent=4, separators=(',', ': '))

    def __str__(self):
        """
        This method should be overloaded to specify how to output to plain-text.
        """
        txt = ''
        if 'class' in self.header:
            txt += self.header['class']
            if 'function' in self.header:
                txt += '.'
        for prop in ['function', 'signature']:
            if prop in self.header:
                txt += self.header[prop]
        txt += self.docstring
        return txt

    def __markdown__(self, filename=None):
        """
        Output docstring as markdown using a template.

        Args:
            filename (str, optional) : select template to use for markdown
                rendering.
        """
        from mako.template import Template
        if not filename:
            filename = self.mdtemplate
        template = Template(filename=filename)
        data = self.data
        headers = self.headers.split('|')
        hd1 = '#'
        hd2 = '##'
        hd3 = '###'
        return template.render(header=self.header, sections=data,
                               headers=headers, h1=hd1, h2=hd2, h3=hd3)


class GoogleDocString(DocString):
    """
    This is the base class for parsing docstrings that are formatted according
    to the Google style guide: .
    """

    def __init__(self, docstring):
        self.template = 'templates/google_docstring.md'
        super(GoogleDocString, self).__init__(docstring)
        self.headers = ('Args|Arguments|Returns|Yields|Raises|Note|' +
                        'Notes|Example|Examples|Attributes|Todo')
        self.mdtemplate = 'templates/google_docstring.md'
        self.argdelimiter = ': '
        self.secdelimiter = ':'
        self.indent = 2

    def extract_section(self, keywords='Args|Arguments', require=False):
        """
        Extracts a section from the docstring.

        Args:
            keywords (str, optional): This string specifies all aliases for the
                the section. Each alias is separated by |. Defaults to
                `'Args|Arguments'`.
            require (bool, optional): Issue a warning if the section is not
            found and this section is required. Defaults to False.
        """
        import warnings
        import textwrap
        docstring = textwrap.dedent(self.docstring).strip()

        # A section starts with `keyword` + delimiter and the contents of the
        # section are indented. The section ends after the indent.
        header = re.compile(r'(?:%s)%s\s*'%(keywords, self.secdelimiter))
        indent = re.compile(r'(^\s{%s,})'%self.indent)

        issection = False
        txt = []
        for line in docstring.split('\n'):
            # Add section contents as long as it is indented
            # or if it is blank
            if issection:
                if indent.findall(line) or not line:
                    txt.append(line)
                else:
                    break

            if header.findall(line):
                issection = True

        if not issection and require:
            warnings.warn(r'Unable to find section `%s`' %
                          keywords)
            return None

        return textwrap.dedent('\n'.join(txt))

    def parse_section(self, section):
        """
        Parses blocks in a section by searching for an argument list, and
        regular notes. The argument list must be the first block in the section.
        A section is broken up into multiple blocks by having empty lines.

        Returns:
            A dictionary that contains the key `args` for holding the argument
            list (`None`) if not found and the key `text` for holding regular
            notes.

        Example:
            ```
            Section:
                This is block 1 and may or not contain an argument list (see
                `args` for details).

                This is block 2 and any should not contain any argument list.
            ```

        """
        import textwrap

        # Get header
        lines = section.split('\n')
        header = self._header().findall(lines[0])
        if header:
            header = header[0]
            # Remove the header from section
            lines = lines[1:]
            section = '\n'.join(lines)
        else:
            header = ''

        # Get argument list
        args = self.parse_arglist(section)
        if args:
            section = ''

        out = {}
        out['header'] = header
        out['text'] = section
        out['args'] = args
        return out

    def extract_sections(self):
        """
        Extracts sections from the docstring. Sections are identified by an
        additional header which is a recognized Keyword such as `Args` or
        `Returns`. All text within  a section is indented and the section ends
        after the indention.
        """
        import textwrap

        sections = []
        section = []
        header = self._header()
        regex_indent = self._indent()
        indent = 0
        current_indent = 0
        is_section = False
        new_section = False
        lines = self.docstring.split('\n')

        def inline_new_section(section, sections):
            """
            Inline function for creating new section.
            """
            # Close the previous section
            section_text = '\n'.join(section)
            if section_text:
                sections.append(section_text)
            # and start the next one
            section = []
            indent = 0
            return indent, section, sections

        for line in lines:
            # Compute amount of indentation
            current_indent = get_indent(regex_indent, line)

            if new_section and current_indent > 0:
                new_section = False
                indent = current_indent

            if header.findall(line):
                is_section = True
                indent, section, sections = inline_new_section(section, sections)
                new_section = True
            # Section ends because of a change in indent that is not caused
            # by a line break
            elif line and is_section and current_indent < indent:
                is_section = False
                indent, section, sections = inline_new_section(section, sections)

            section.append(line[indent:])

        indent, section, sections = inline_new_section(section, sections)
        return sections

    def parse_arglist(self, section, require=False):
        """
        Parses the argument list placed at the start of a section.

        The format is `variable (optional signature): description`. The variable
        and signature is separated from the description using `: ` (including
        space). Space in the separator is needed to to ensure there is no clash
        with restructured text syntax (e.g., :any:). Multiline line descriptions
        must be indented using at least `indent` number of spaces.

        Arguments:

            section : A string that contains the text of the section to parse.
            require (bool, optional) : If this optional argument is set to
                `True`, then an exception is raised if parsing fails. Defaults
                to `False`. Setting this argument to `True` may be useful for
                parsing sections like `Arguments` that should always contain an
                argument list.

        Returns:

            list : Each item in this list is a dictionary that contains the
                properties of an argument. These properties are the field,
                signature, and description. If the no list is parsed, then
                `None` is returned.
            what is this?

        Raises:

            ValueError : This error is raised if `require` is `True` and parsing
                fails.


        """
        import textwrap

        pattern = (r'^(\w*)\s*(?:(\(.*\)))*\s*%s' % self.argdelimiter +
                   r'(.*\n?(?:^\s{%s,}.*\n)*)' % self.indent)
        matches = re.compile(pattern, re.M).findall(textwrap.dedent(section))

        if not matches:
            if require:
                raise ValueError('Failed to parse argument list:\n `%s` ' %
                                 (section))
            return None

        argsout = []
        for match in matches:
            field = match[0]
            signature = match[1]
            description = match[2].rstrip()
            argsout.append({'field' : field, 'signature' : signature,
                            'description' : description})
        return argsout

    def _header(self):
        return re.compile(r'^\s*(%s)%s\s*'%(self.headers, self.secdelimiter))

    def _indent(self):
        return re.compile(r'(^\s{%s,})'%self.indent)

def parser(obj, choice='Google'):
    """
    Returns a new docstring parser based on selection. Currently, only the
    Google docstring syntax is supported.

    Args:
        obj : A dictionary that contains the docstring and other properties.
            This object is typically obtained by calling the `extract` function.
        choice: Keyword that determines the parser to use. Defaults to
            `'Google'`.

    Returns:
        A parser for the selected docstring syntax.

    Raises:
        NotImplementedError : This exception is raised when no parser is found.



    """
    parsers = {'Google' : GoogleDocString}

    if choice in parsers:
        return parsers[choice](obj)
    else:
        NotImplementedError('The docstring parser `%s` is not implemented' %
                            choice)

def summary(txt):
    """
    Returns the first line of a string.
    """
    lines = txt.split('\n')
    return lines[0]

def get_indent(regex, txt):
    """
    Returns the indentation size.
    """
    indent_size = regex.findall(txt)
    if indent_size:
        return len(indent_size[0])
    else:
        return 0
