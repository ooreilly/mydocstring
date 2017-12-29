import re

class DocString(object):

    def __init__(self, docstring):
        self.docstring = docstring

    def args(self):
        pass

    def find(self, pattern):
        """
        Performs a search for a docstring that matches a specific pattern.

        Returns:
            dict: The return type is a dictionary with the following keys:
                `name` : The name of the function/method.
                `signature` : the signature of the function/method.
                `dtype` : What type of construct the docstring is attached to
                `'module'`, `'class'`, `'method'`, or `'function'`.
        """
        import warnings
        matches = re.compile(pattern, re.M).findall(self.txt)
        if not matches:
            warnings.warn(r'Unable to extract docstring for `%s`' % self.query)
            return None
        else:
            return {'name': matches[0][0],
                    'signature': matches[0][1],
                    'docstring': matches[0][2],
                    'dtype': self.dtype}

class GoogleDocString(DocString):

    def args(self, keywords='Args|Arguments'):
        import warnings
        import textwrap
        docstring = textwrap.dedent(self.docstring).strip()
        # Get the argument block
        # The argument block ends after a new line, or 
        # is the last part of the docstring.
        pattern = '(?:%s):\n([\w\W]*)(?:\n[^.])?'%keywords
        matches = re.compile(pattern, re.M).findall(docstring)

        if not matches:
            warnings.warn(r'Unable to find argument list for `%s`' %
                    self.docstring['query'])
            return None
        argblock = textwrap.dedent(matches[0])

        # Parse arguments
        # The format is `variable (optional signature): description`.
        # The variable and signature is separated from the description using 
        # `: ` (including space). Space in the separator is needed to 
        # to ensure there is no clash with restructured text syntax 
        # (e.g., :any:).
        # Multiline line descriptions must be indented using at least two
        # spaces.
        pattern = '(\w*)\s*(?:\((.*)\))*\s*:\s(.*\n(?:\s{2,}.*)*)'
        matches = re.compile(pattern, re.M).findall(argblock)

        if not matches:
            raise ValueError('Failed to parse argument block:\n `%s` ' 
                  % (argblock))

        argsout = []
        for m in matches:
            argsout.append({'name' : m[0], 'signature' : m[1], 'description' :
                    m[2].strip()})
        return argsout


def parse(obj, parser=GoogleDocString):
    docstr = {}
    parser = parser(obj['docstring'])
    docstr['args'] = parser.args()
    return docstr

