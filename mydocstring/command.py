"""
MIT License

Copyright (c) 2018 Ossian O'Reilly

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
"""
The command module handles the execution of the user-supplied commands via the
command-line interface (main application). In particular, this module takes the
parsed docstrings and outputs them to plain-text, markdown, or json.
"""
class Command(object):
    """
    Executes the commands provided on the command line.

    """

    def __init__(self, options):
        import os
        from . import extract
        from . import parse
        self.filename = options['<file>']
        self.options = {}

        if options['--version']:
            self.version()
            return

        if options['<name>'] == '.':
            self.name = ''
        else:
            self.name = options['<name>']
        self.docstring = extract.extract(self.filename, self.name)

        self.parser = parse.GoogleDocString(self.docstring['docstring']) 

        self.options = {'--text' : self.text,
                        '--markdown' : self.markdown,
                        '--json' : self.json
                        }

        if options['--template']:
            self.template = options['--template'][1:]
        else:
            self.template = ''

        if not self.template:
            self.template = os.path.join(os.path.dirname(__file__),
                                         'templates/google_docstring.md')

    def __call__(self, cmd):
        """
        Executes a command if it is found.

        Args:
            cmd : A string that specifies the command to execute.

        """
        if cmd in self.options:
            self.options[cmd]()

    def text(self):
        """
        Output docstring as plain-text.
        """
        txt = ''

        self.parser.parse()
        if self.docstring['class']:
            txt += self.docstring['class']
            if self.docstring['function']:
                txt += '.'
        for prop in ['function', 'signature']:
            if prop in self.docstring:
                txt += self.docstring[prop]
        txt += self.docstring['docstring']
        print(txt)

    def markdown(self):
        """
        Output docstring as markdown using a template.
        """
        from mako.template import Template
        template = Template(filename=self.template)
        hd1 = '#'
        hd2 = '##'
        hd3 = '###'
        self.parser.parse(mark_code_blocks=True)
        headers, data = self.parser.markdown()
        print(template.render(header=self.docstring, sections=data,
                              headers=headers, h1=hd1, h2=hd2, h3=hd3))

    def json(self):
        """
        Output docstring as JSON data.
        """
        self.parser.parse()
        print(self.parser.__json__())

    def version(self):
        """
        Output current version number.
        """
        from . import version
        print(version.__VERSION__)
