"""
This module is used to extract a docstring from source.
"""
import re

class Extract(object):
    """
    Base class for extracting docstrings.

    Attributes:
        filename: A string that that specifies the file to extract docstrings
            from.
        txt : A string that contains the source code that has been read from
            `source`.
        query : The docstring to search for. The search is specified in the form
            of `Class.method`, or `function`, or `.` to search for the module
            docstring.
        classname : Holds the class name of the query.
        funcname : Holds the function or method name of the query.
        dtype : Holds the type of the query `module`, `class`, `method`, or
            `function`.

    """

    def __init__(self, filename):
        """
        Initializer for Extract.

        Arguments:
            filename: A string that that specifies the file to extract
                docstrings from.

        """
        self.txt = open(filename).read()
        self.filename = filename
        self.query = ''
        self.classname = ''
        self.funcname = ''
        self.dtype = ''


    def extract(self, query):
        """
        Extracts the docstring.

        Arguments:
            query : The docstring to search for. The search is specified in the form
                of `Class.method`, or `function`, or `.` to search for the module
                docstring.

        Returns:
            A dictionary that matches the description given by `Extract.find`.

        """

        self.query = query
        self.classname, self.funcname, self.dtype = get_names(query)
        types = {'class' : self.extract_class,
                 'method' : self.extract_method,
                 'function' : self.extract_function,
                 'module' : self.extract_module}

        return types[self.dtype]()

    def extract_function(self):
        """
        Override this method to extract function docstrings for the specific
        language. The functions extracted are module functions. Lamba functions
        are not extracted.

        Returns:
            A dictionary that matches the description given by `Extract.find`.
        """
        pass
    def extract_class(self):
        """
        Override this method to extract class docstrings for the specific
        language.

        Returns:
            A dictionary that matches the description given by `Extract.find`.
        """
        pass

    def extract_method(self):
        """
        Override this method to extract method docstrings for the specific
        language.

        Returns:
            A dictionary that matches the description given by `Extract.find`.
        """
        pass

    def extract_module(self):
        """
        Override this method to extract module docstrings for the specific
        language. Module docstrings are defined at the start of a file and are
        not attached to any block of code.

        Returns:
            A dictionary that matches the description given by `Extract.find`.
        """
        pass

    def find(self, pattern):
        """
        Performs a search for a docstring that matches a specific pattern.

        Returns:
            dict: The return type is a dictionary with the following keys:
                 * `class` :  The name of the class.
                 * `function` : The name of the function/method.
                 * `signature` : The signature of the function/method.
                 * `docstring` : The docstring itself.
                 * `type` : What type of construct the docstring is attached to.
                      This can be either `'module'`, `'class'`, `'method'`, or
                      `'function'`.
                 * `label` : The search query string.
                 * `filename` : The filename of source to extract docstrings from.
                 * `source` : The source code if the query is a function/method.

        Raises:
            NameError: This is exception is raised if the docstring cannot be
                extracted.
        """
        import textwrap
        matches = re.compile(pattern, re.M).findall(self.txt)
        if not matches:
            raise NameError(r'Unable to extract docstring for `%s`' % self.query)
        else:

            cls = matches[0][0]
            function = matches[0][1]
            signature = matches[0][2]
            indent = len(matches[0][3])
            docstring = remove_indent(matches[0][4], indent)
            if self.dtype == 'function' or self.dtype == 'method': 
                source = textwrap.dedent('def ' + function + signature + ':\n' +
                                         matches[0][5]) 
            else: 
                source = ''

            out = {}
            out['class'] = cls
            out['function'] = function
            out['signature'] = signature
            out['docstring'] = docstring
            out['source'] = source
            out['type'] = self.dtype
            out['label'] = self.query
            out['filename'] = self.filename

            return out

class PyExtract(Extract):
    """
    Base class for extracting docstrings from python source code.
    """

    def extract_function(self):
        pattern = (r'^\s*()def\s(%s)(\((?!self).*\)):.*' % self.funcname
                   + r'\n*(\s+)"""([\w\W]*?)"""\n((\4.*\n+)+)?')
        return self.find(pattern)

    def extract_class(self):
        pattern = (r'^\s*class\s+(%s)()(\(\w*\))?:\n(\s+)"""([\w\W]*?)"""()' %
                   self.classname)
        return self.find(pattern)

    def extract_method(self):
        pattern = (r'class\s+(%s)\(?\w*\)?:[\n\s]+[\w\W]*?' % self.classname +
                   r'[\n\s]+def\s+(%s)(\(self.*\)):.*\n' % self.funcname +
                   r'(\s+)"""([\w\W]*?)"""\n((?:\4.*\n+)+)?')
        return self.find(pattern)

    def extract_module(self):
        pattern = r'()()()()^"""([\w\W]*?)"""'
        return self.find(pattern)


def extract(filestr, query):
    """
    Extracts a docstring from source.

    Arguments:
        filestr: A string that specifies filename of the source code to extract
            from.
        query: A string that specifies what type of docstring to extract.

    """
    import os

    filename = os.path.splitext(filestr)
    ext = filename[1]

    options = {'.py' : PyExtract}

    if ext in options:
        extractor = options[ext](filestr)

    return extractor.extract(query)


def get_names(query):
    """
    Extracts the function and class name from a query string.
    The query string is in the format `Class.function`.
    Functions starts with a lower case letter and classes starts
    with an upper case letter.

    Arguments:
        query: The string to process.

    Returns:
        tuple: A tuple containing the class name, function name,
               and type. The class name or function name can be empty.

    """
    funcname = ''
    classname = ''
    dtype = ''

    members = query.split('.')
    if len(members) == 1:
        # If no class, or function is specified, then it is a module docstring
        if members[0] == '':
            dtype = 'module'
        # Identify class by checking if first letter is upper case
        elif members[0][0].isupper():
            classname = query
            dtype = 'class'
        else:
            funcname = query
            dtype = 'function'
    elif len(members) == 2:
        # Parse method
        classname = members[0]
        funcname = members[1]
        dtype = 'method'
    else:
        raise ValueError('Unable to parse: `%s`' % query)

    return (classname, funcname, dtype)

def remove_indent(txt, indent):
    """
    Dedents a string by a certain amount.
    """
    lines = txt.split('\n')
    if lines[0] != '\n':
        header = '\n' + lines[0]
    else:
        header = ''
    return '\n'.join([header] + [line[indent:] for line in lines[1:]])

