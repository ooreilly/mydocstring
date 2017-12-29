from .. import docstring 
import pytest

def test_get_names():
    docstring.get_names('test') == ('', 'test', 'function')
    docstring.get_names('Test') == ('Test', '', 'class')
    docstring.get_names('Test.test') == ('Test', 'test', 'method')
    docstring.get_names('') == ('', '', 'module')

def test_fetch():
    example = 'fixtures/example.py'
    match = docstring.fetch(example, 'function_with_docstring')
    assert match['name'] == 'function_with_docstring'
    assert match['signature'] == '(arg1, arg2)'
    assert match['dtype'] == 'function'
    
    match = docstring.fetch(example, 'ExampleOldClass')
    assert match['name'] == 'ExampleOldClass'
    assert match['signature'] == ''
    assert match['dtype'] == 'class'
    
    match = docstring.fetch(example, 'ExampleNewClass')
    assert match['name'] == 'ExampleNewClass'
    assert match['signature'] == '(object)'
    assert match['dtype'] == 'class'

    match = docstring.fetch(example, 'ExampleOldClass.__init__')


    with pytest.warns(UserWarning) : docstring.fetch(example, 'something')
    with pytest.raises(ValueError) : docstring.fetch(example, 'something.a.a')
