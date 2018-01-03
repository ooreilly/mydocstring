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
        if options['<name>'] == '.':
            self.name = ''
        else:
            self.name = options['<name>']
        self.docstring = extract.extract(self.filename, self.name)
        self.parser = parse.parser(self.docstring['docstring'], 'Google')
        self.parser.parse()
        self.options = {'--text' : self.text,
                        '--markdown' : self.markdown,
                        '--json' : self.json}

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
        headers, data = self.parser.markdown()
        print(template.render(header=self.docstring, sections=data,
                              headers=headers, h1=hd1, h2=hd2, h3=hd3))

    def json(self):
        """
        Output docstring as JSON data.
        """
        print(self.parser.__json__())
