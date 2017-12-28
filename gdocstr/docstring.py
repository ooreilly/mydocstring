"""
This module is used to fetch a docstring from source.
"""
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
        self.classname, self.funcname, self.dtype = get_names(query)

    def fetch(self):
        """
        Fetches the docstring.

        """
        if self.dtype == 'class':
            return self.fetch_class()
        elif self.dtype == 'method':
            return self.fetch_method()
        elif self.dtype == 'function':
            return self.fetch_function()
        elif self.dtype == 'module':
            return self.fetch_module()

    def fetch_function(self):
        """
        override to fetch function docstrings for the specific language.
        """
        pass
    def fetch_class(self):
        """
        override to fetch class docstrings for the specific language.
        """
        pass
    def fetch_method(self):
        """
        override to fetch method docstrings for the specific language.
        """
        pass
    def fetch_module(self):
        """
        override to fetch module docstrings for the specific language.
        """
        pass

class PyFetch(Fetch):
    """
    Base class for fetching docstrings from python source code.
    """

def fetch(filestr, query):
    """
    Fetches a docstring from a source code

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

