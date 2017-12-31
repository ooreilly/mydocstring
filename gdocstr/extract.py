"""
This module is used to extract a docstring from source.
"""
import re

class Extract(object):
    """
    Base class for extracting docstrings.

    """

    def __init__(self, txt, query):
        """
        Initializer for Extract.

        Arguments:
            txt: A string that holds the text to extract docstrings from.
            query: A string that specifies what type of docstring to extract.

        """
        self.txt = txt
        self.query = query
        self.classname, self.funcname, self.dtype = get_names(query)

    def extract(self):
        """
        Extracts the docstring.

        """

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
                `name` : The name of the function/method.
                `signature` : the signature of the function/method.
                `dtype` : What type of construct the docstring is attached to
                `'module'`, `'class'`, `'method'`, or `'function'`.
        """
        import warnings
        matches = re.compile(pattern, re.M).findall(self.txt)
        if not matches:
            raise NameError(r'Unable to extract docstring for `%s`' % self.query)
        else:
            out = {}

            cls = matches[0][0]
            function = matches[0][1]
            signature = matches[0][2]
            indent = len(matches[0][3])
            # Remove indentation from docstring
            lines = matches[0][4].split('\n')
            if lines[0] != '\n':
                header =  '\n' + lines[0]
            else:
                header = ''
            docstring = '\n'.join([header] + [line[indent:] for line in
                                  lines[1:]])

            out['class'] = cls
            out['function'] = function
            out['signature'] = signature
            out['docstring'] = docstring
            out['type'] = self.dtype

            return out

class PyExtract(Extract):
    """
    Base class for extracting docstrings from python source code.
    """

    def extract_function(self):
        pattern = (r'^\s*()def\s(%s)(\((?!self)[:=,\s\w]*\)):\n*(\s+)"""([\w\W]*?)"""' %
                   self.funcname)
        return self.find(pattern)

    def extract_class(self):
        pattern = (r'^\s*class\s+(%s)()(\(\w*\))?:\n(\s+)"""([\w\W]*?)"""' %
                   self.classname)
        return self.find(pattern)

    def extract_method(self):
        # First check that the class name matches.
        # Then check that method signature matches.
        # Finally get the docstring.
        pattern = (r'class\s+(%s)\(?\w*\)?:[\n\s]+[\w\W]*?' % self.classname +
                   r'[\n\s]+def\s+(%s)(\(self[:=\w,\s]*\)):\n' % self.funcname +
                   r'(\s+)"""([\w\W]*?)"""')
        return self.find(pattern)

    def extract_module(self):
        # The module docstring does not have any name and signature,
        # so skip these.
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
    txt = open(filestr).read()

    if ext in ['.py']:
        extractor = PyExtract(txt, query)

    return extractor.extract()


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
