"""
Module docstring
"""

def function_with_docstring(arg1, arg2=True):
    """Short description.
    Example of a function with a doc string.

    Args:
        arg1(type): description for arg1.
        arg2 : description for arg2
            that spans multiple lines.

    Returns:
        bool: `True` or `False`. Defaults to `True`.

        The return section can also have a detailed description that spans
        multiple lines. It is important that this description is indented.

    """
    pass

class ExampleOldClass:
    """
    An example of a docstring for an old-style class.
    """

    def __init__(self):
        """
        Description of the __init__ function.

        """
        pass

    def class_function_with_docstring(self, arg1, arg2):
        """
        Description of a class function.
        
        Args:
            arg1(type) : description for arg1.
            arg2 : description for arg1.

        """
        pass
    
class ExampleNewClass(object):
    """
    An example of a docstring for a new-style class.
    """
    def __init__(self):
        """
        Example of a docstring for the init function.
        """
        pass

def __init__(arg1):
    """
    Example of docstring for a function with the same name as a method.
    """
    pass
