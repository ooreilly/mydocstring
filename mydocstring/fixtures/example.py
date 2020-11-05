"""
Module docstring
"""

def function_with_docstring(arg1, arg2=True):
    """Short description.
    Example of a function with a doc string.

    Some more details.

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

def function_with_docstring_pep484(arg0: int, arg1: bool = True) -> bool:
    """Short description.
    Example of a function with a doc string.

    Some more details.

    Args:
        arg0: description for arg0.
        arg1: description for arg1
            that spans multiple lines.

    Returns:
        bool: `True` or `False`. Defaults to `True`.

        The return section can also have a detailed description that spans
        multiple lines. It is important that this description is indented.

    """

def function_with_docstring_objects_pep484(arg0: int, arg1: bool = True) -> obj.bool:
    """
    """

def function_with_undefined_header():
    """

    The following arg list is ignored (unless undefined headers are allowed):
            arg1: ...
            arg2: ...

    """

def overloaded_add(arg1, arg2):
    """
    Add two integers

    Some more details.

    Args:
        arg1(int) : Integer to add.
        arg2(int) : Integer to add.

    Returns:
        The sum of the two integers.

    """
    return arg1 + arg2

def overloaded_add(arg1, arg2, arg3):
    """
    An overloaded function

    Some more details.

    Args:
        arg1(int) : Integer to add.
        arg2(int) : Integer to add.
        arg3(int) : Integer to add.
    """
    return arg1 + arg2 + arg3

def multiline(arg1,
              arg2,
              arg3):
    """
    A function with a signature that spans multiple lines.

    Args:
        arg1(int) : Integer to add.
        arg2(int) : Integer to add.
        arg3(int) : Integer to add.
    """
    return arg1 + arg2 + arg3

def multiline_new_line_before_args(
              arg1,
              arg2,
              arg3):
    """
    A function with a signature that spans multiple lines, but with a line break before the first
    argument.

    Args:
        arg1(int) : Integer to add.
        arg2(int) : Integer to add.
        arg3(int) : Integer to add.
    """
    return arg1 + arg2 + arg3

class ExampleOldClass:
    """
    An example of a docstring for an old-style class.

    Some more details
    """

    def __init__(self,
                 arg1,
                 arg2):
        """
        Description of the __init__ function.

        Some more details. Documentation for `arg1` is missing on purpose. 

        Args:
            arg2 : description for arg2.

        """
        pass

    def method_with_docstring(self, arg1, arg2):
        """
        Description of a method.

        Some more details.
        
        Args:
            arg1(type) : description for arg1.
            arg2 : description for arg1.

        """
        pass
    
class ExampleNewClass(object):
    """
    An example of a docstring for a new-style class.

    Some more details.

    """
    def __init__(self):
        """
        Example of a docstring for the init function.

        Some more details.
        """
        pass
    
    def method_with_new_line_before_self(
            self):
        """
        Method with a new line before `self`.
        """
        pass

def __init__(arg1):
    """
    Example of docstring for a function with the same name as a method.

    Some more details.
    """
    pass
