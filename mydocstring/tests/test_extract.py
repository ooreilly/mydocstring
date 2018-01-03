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
    assert match['function'] == 'function_with_docstring'
    assert match['signature'] == '(arg1, arg2=True)'
    assert match['type'] == 'function'
    assert match['source'] == 'def function_with_docstring(arg1, arg2=True):\n    pass\n\n'
    assert match['docstring']
    
    match = extract.extract(example, 'ExampleOldClass')
    assert match['class'] == 'ExampleOldClass'
    assert match['type'] == 'class'
    
    match = extract.extract(example, 'ExampleNewClass')
    assert match['class'] == 'ExampleNewClass'
    assert match['signature'] == '(object)'
    assert match['type'] == 'class'

    match = extract.extract(example, 'ExampleOldClass.__init__')

    with pytest.raises(NameError) : extract.extract(example, 'something')
    with pytest.raises(ValueError) : extract.extract(example, 'something.a.a')
