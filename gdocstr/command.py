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
        from . import extract
        from . import parse
        self.filename = options['<file>']
        if options['<name>'] == '.':
            self.name = ''
        else:
            self.name = options['<name>']
        self.docstring = extract.extract(self.filename, self.name)
        self.parser = parse.parser(self.docstring, 'Google')
        self.parser.parse()
        self.options = {'--text' : self.text,
                        '--markdown' : self.markdown,
                        '--json' : self.json}

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
        Output docstring as plain-text."
        """
        print(self.parser)

    def markdown(self, template=None):
        print(self.parser.__markdown__(template))

    def json(self):
        """
        Output docstring as JSON data.
        """
        print(self.parser.__json__())
