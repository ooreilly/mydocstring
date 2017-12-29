from .. import fetch 
import pytest

def test_get_names():
    fetch.get_names('test') == ('', 'test', 'function')
    fetch.get_names('Test') == ('Test', '', 'class')
    fetch.get_names('Test.test') == ('Test', 'test', 'method')
    fetch.get_names('') == ('', '', 'module')

def test_fetch():
    example = 'fixtures/example.py'
    match = fetch.fetch(example, 'function_with_docstring')
    assert match['name'] == 'function_with_docstring'
    assert match['signature'] == '(arg1, arg2=True)'
    assert match['dtype'] == 'function'
    
    match = fetch.fetch(example, 'ExampleOldClass')
    assert match['name'] == 'ExampleOldClass'
    assert match['signature'] == ''
    assert match['dtype'] == 'class'
    
    match = fetch.fetch(example, 'ExampleNewClass')
    assert match['name'] == 'ExampleNewClass'
    assert match['signature'] == '(object)'
    assert match['dtype'] == 'class'

    match = fetch.fetch(example, 'ExampleOldClass.__init__')


    with pytest.warns(UserWarning) : fetch.fetch(example, 'something')
    with pytest.raises(ValueError) : fetch.fetch(example, 'something.a.a')
