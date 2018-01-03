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

    def __init__(self, docstring, config=None):
        self.header = {}
        self.docstring = docstring
        self.data = []
        self._config = config

        # Internals for parsing
        # _section : This variable will hold the contents of each unparsed section
        # _sections : A list that will hold all unparsed sections.
        # _linenum : line number relative to the current section being
        # parsed.
        # _re .. : Regex functions.
        # _indent : This variable will hold the current indentation (number of spaces).

        self._parsing = {'indent' : 0, 'linenum' : 0, 'sections' : [],
                         'section' : []}
        self._re = {}

    def parse(self):
        """
        This method should be overloaded and perform the parsing of all
        sections.
        """
        self.data = []
        self.extract_sections()
        for section in self._parsing['sections']:
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
        return self.docstring

    def markdown(self):
        """
        Output data relevant data needed for markdown rendering.

        Args:
            filename (str, optional) : select template to use for markdown
                rendering.
        """
        data = self.data
        headers = self._config['headers'].split('|')
        return headers, data


class GoogleDocString(DocString):
    """
    This is the base class for parsing docstrings that are formatted according
    to the Google style guide: .
    """

    def __init__(self, docstring, config=None):
        import os

        if not config:
            config = {}
            config['headers'] = ('Args|Arguments|Returns|Yields|Raises|Note|' +
                                 'Notes|Example|Examples|Attributes|Todo')
            config['indent'] = 4
            config['delimiter'] = ':'
            config['arg_delimiter'] = ': '

        super(GoogleDocString, self).__init__(docstring, config)

        self._re = {'header' : self._compile_header(),
                    'indent' : self._compile_indent(),
                    'arg' : self._compile_arg()}


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

        # Get header
        lines = section.split('\n')
        header = self._compile_header().findall(lines[0])


        # Skip the first line if it is a header
        header = self._get_header(lines[0])
        self._parsing['linenum'] = int(bool(header))
        text = []

        args = []
        while self._parsing['linenum'] < len(lines):

            arg_data = self._parse_arglist(lines)
            if arg_data:
                args.append(arg_data)
            else:
                text.append(lines[self._parsing['linenum']])
            self._parsing['linenum'] += 1

        out = {}
        out['header'] = header
        out['text'] = '\n'.join(text)
        out['args'] = args
        return out

    def extract_sections(self):
        """
        Extracts sections from the docstring. Sections are identified by an
        additional header which is a recognized Keyword such as `Args` or
        `Returns`. All text within  a section is indented and the section ends
        after the indention.
        """

        lines = self.docstring.split('\n')
        new_section = True

        for linenumber, line in enumerate(lines):
            # Compute amount of indentation
            current_indent = self._get_indent(line)

            # Capture indent to be able to remove it from the text and also
            # to determine when a section ends.
            # The indent is reset when a new section begins.
            if new_section and self._is_indent(line):
                self._parsing['indent'] = current_indent
                new_section = False

            if self._is_header(line):
                self._err_if_missing_indent(lines, linenumber)
                self._end_section()
                self._begin_section()
                new_section = True
            # Section ends because of a change in indent that is not caused
            # by a line break
            elif line  and current_indent < self._parsing['indent']:
                self._end_section()
                self._begin_section()

            self._parsing['section'].append(line[self._parsing['indent']:])

        self._end_section()
        self._begin_section()

    def _parse_arglist(self, lines, require=False):
        arg_data = self._get_arg(lines[self._parsing['linenum']])

        if not arg_data:
            if require:
                raise ValueError('Failed to parse argument list:\n `%s` ' %
                                 (self._parsing['section']))
            return None

        # Take into account that the description can be multi-line
        # the next line has to be indented
        description = [arg_data[0][2]]
        next_line = _get_next_line(lines, self._parsing['linenum'])
        while self._is_indent(next_line):
            self._parsing['linenum'] += 1
            description.append(lines[self._parsing['linenum']])
            next_line = _get_next_line(lines, self._parsing['linenum'])

        return {'field' : arg_data[0][0],
                'signature' : arg_data[0][1],
                'description' : '\n'.join(description)}

    def _compile_header(self):
        return re.compile(r'^\s*(%s)%s\s*'%(self._config['headers'],
                                            self._config['delimiter']))

    def _compile_indent(self):
        return re.compile(r'(^\s{%s,})'%self._config['indent'])

    def _compile_arg(self):
        return re.compile(r'(\w*)\s*(\(.*\))?\s*%s(.*)' %
                          self._config['arg_delimiter'])


    def _err_if_missing_indent(self, lines, linenumber):
        next_line = _get_next_line(lines, linenumber)
        is_next_indent = self._is_indent(next_line)
        if not is_next_indent:
            raise SyntaxError("Missing indent after `%s`" %
                              next_line)

    def _begin_section(self):
        self._parsing['section'] = []
        self._parsing['indent'] = 0

    def _end_section(self):
        section_text = '\n'.join(self._parsing['section'])
        if section_text.strip():
            self._parsing['sections'].append(section_text)

    def _get_indent(self, line):
        """
        Returns the indentation size.
        """
        indent_size = self._re['indent'].findall(line)
        if indent_size:
            return len(indent_size[0])
        else:
            return 0

    def _is_indent(self, line):
        """
        Returns if the line is indented or not.
        """
        indent = self._get_indent(line)
        return bool(indent > 0)

    def _is_header(self, line):
        return bool(self._re['header'].findall(line))

    def _get_header(self, line):
        header = self._re['header'].findall(line)
        if header:
            return header[0]
        else:
            return ''
    def _get_arg(self, line):
        return self._re['arg'].findall(line)

    def _is_arg(self, line):
        return bool(self._re['arg'].findall(line))

def _get_next_line(lines, linenumber):
    """
    Returns the next line but skips over any empty lines.
    An empty line is returned if read past the last line.
    """
    inc = linenumber + 1
    num_lines = len(lines)
    while True:
        if inc == num_lines:
            return ''
        if lines[inc]:
            return lines[inc]
        inc += 1

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
