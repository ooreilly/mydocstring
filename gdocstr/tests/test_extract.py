from .. import extract 
import pytest

def test_get_names():
    extract.get_names('test') == ('', 'test', 'function')
    extract.get_names('Test') == ('Test', '', 'class')
    extract.get_names('Test.test') == ('Test', 'test', 'method')
    extract.get_names('') == ('', '', 'module')

def test_extract():
    example = 'fixtures/example.py'
    match = extract.extract(example, 'function_with_docstring')
    assert match['name'] == 'function_with_docstring'
    assert match['signature'] == '(arg1, arg2=True)'
    assert match['dtype'] == 'function'
    
    match = extract.extract(example, 'ExampleOldClass')
    assert match['name'] == 'ExampleOldClass'
    assert match['signature'] == ''
    assert match['dtype'] == 'class'
    
    match = extract.extract(example, 'ExampleNewClass')
    assert match['name'] == 'ExampleNewClass'
    assert match['signature'] == '(object)'
    assert match['dtype'] == 'class'

    match = extract.extract(example, 'ExampleOldClass.__init__')


    with pytest.warns(UserWarning) : extract.extract(example, 'something')
    with pytest.raises(ValueError) : extract.extract(example, 'something.a.a')
