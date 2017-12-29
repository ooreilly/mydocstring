"""
This module is used to fetch a docstring from source.
"""
import re

class Fetch(object):
    """
    Base class for fetching docstrings.

    """

    def __init__(self, txt, query):
        """
        Initializer for Fetch.

        Arguments:
            txt: A string that holds the text to fetch docstrings from.
            query: A string that specifies what type of docstring to fetch.

        """
        self.txt = txt
        self.query = query
        self.classname, self.funcname, self.dtype = get_names(query)

    def fetch(self):
        """
        Fetches the docstring.

        """

        types = {'class' : self.fetch_class,
                 'method' : self.fetch_method,
                 'function' : self.fetch_function,
                 'module' : self.fetch_module}

        return types[self.dtype]()

    def fetch_function(self):
        """
        Override this method to fetch function docstrings for the specific
        language. The functions fetched are module functions. Lamba functions
        are not fetched.

        Returns:
            A dictionary that matches the description given by `Fetch.find`.
        """
        pass
    def fetch_class(self):
        """
        Override this method to fetch class docstrings for the specific
        language.

        Returns:
            A dictionary that matches the description given by `Fetch.find`.
        """
        pass

    def fetch_method(self):
        """
        Override this method to fetch method docstrings for the specific
        language.

        Returns:
            A dictionary that matches the description given by `Fetch.find`.
        """
        pass

    def fetch_module(self):
        """
        Override this method to fetch module docstrings for the specific
        language. Module docstrings are defined at the start of a file and are
        not attached to any block of code.

        Returns:
            A dictionary that matches the description given by `Fetch.find`.
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
            warnings.warn(r'Unable to fetch docstring for `%s`' % self.query)
            return None
        else:
            return {'name': matches[0][0],
                    'signature': matches[0][1],
                    'docstring': matches[0][2],
                    'dtype': self.dtype}

class PyFetch(Fetch):
    """
    Base class for fetching docstrings from python source code.
    """

    def fetch_function(self):
        pattern = (r'def\s(%s)(\((?!self)[:=,\s\w]*\)):\n*\s+"""([\w\W]*?)"""' %
                   self.funcname)
        return self.find(pattern)

    def fetch_class(self):
        pattern = (r'class\s*(%s)(\(?\w*\)?):\n*\s+"""([\w\W]*?)"""' %
                   self.classname)
        return self.find(pattern)

    def fetch_method(self):
        # First check that the class name matches.
        # Then check that method signature matches.
        # Finally get the docstring.
        pattern = (r'class\s+%s\(?\w*\)?:[\n\s]+[\w\W]*?' % self.classname +
                   r'[\n\s]+def\s+(%s)(\(self[:=\w,\s]*\)):' % self.funcname +
                   r'[\n\s]+"""([\w\W]*?)"""')
        return self.find(pattern)

    def fetch_module(self):
        # The module docstring does not have any name and signature,
        # so skip these.
        pattern = r'()()^"""([\w\W]*?)"""'
        return self.find(pattern)


def fetch(filestr, query):
    """
    Fetches a docstring from source.

    Arguments:
        filestr: A string that specifies filename of the source code to fetch
            from.
        query: A string that specifies what type of docstring to fetch.

    """
    import os

    filename = os.path.splitext(filestr)
    ext = filename[1]
    txt = open(filestr).read()

    if ext in ['.py']:
        fetcher = PyFetch(txt, query)

    return fetcher.fetch()


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
