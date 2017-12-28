from .. import docstring 
import pytest

def test_get_names():
    docstring.get_names('test') == ('', 'test', 'function')
    docstring.get_names('Test') == ('Test', '', 'class')
    docstring.get_names('Test.test') == ('Test', 'test', 'method')
    docstring.get_names('') == ('', '', 'module')

def test_fetch():
    pass
    match = docstring.fetch('fixtures/example.py', 'function_with_docstring')
    assert match['name'] == 'function_with_docstring'
    assert match['signature'] == '(arg1, arg2)'

    with pytest.raises(NameError) : docstring.fetch(sample, 'something')
    with pytest.raises(ValueError) : docstring.fetch(sample, 'a.b.c')
