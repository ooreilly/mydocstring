from mydocstring import extract
import pytest

example = 'fixtures/example.py'
example_pybind = 'fixtures/example_pybind.py'

def test_get_names():
    extract.get_names('test') == ('', 'test', 'function')
    extract.get_names('Test') == ('Test', '', 'class')
    extract.get_names('Test.test') == ('Test', 'test', 'method')
    extract.get_names('') == ('', '', 'module')

def test_function():
    match = extract.extract(example, 'function_with_docstring')
    args = match['parsed_signature']['args']
    assert match['function'] == 'function_with_docstring'
    assert match['signature'] == '(arg1, arg2=True)'
    assert match['type'] == 'function'
    assert match['source'] == \
            'def function_with_docstring(arg1, arg2=True):\n    pass\n\n'
    assert match['docstring']
    assert args['arg1'] == ''
    assert args['arg2'] == '=True'
    assert 'Some more' in match['docstring']

def test_old_class():
    match = extract.extract(example, 'ExampleOldClass')
    assert match['class'] == 'ExampleOldClass'
    assert match['type'] == 'class'
    assert match['docstring']
    assert 'Some more' in match['docstring']

def test_new_class():
    match = extract.extract(example, 'ExampleNewClass')
    assert match['class'] == 'ExampleNewClass'
    assert match['signature'] == '(object)'
    assert match['type'] == 'class'
    assert match['docstring']
    assert 'Some more' in match['docstring']

def test_init():
    match = extract.extract(example, 'ExampleOldClass.__init__')
    assert match['class'] == 'ExampleOldClass'
    assert match['signature'] == '(self, arg1, arg2)'
    assert match['docstring']
    assert 'Some more' in match['docstring']

def test_method():
    match = extract.extract(example, 'ExampleOldClass.method_with_docstring')
    assert match['function'] == 'method_with_docstring'
    assert match['signature'] == '(self, arg1, arg2)'
    assert match['type'] == 'method'
    print(match)
    print(match['docstring'])
    assert 'Some more' in match['docstring']

def test_function_not_found():
    with pytest.raises(NameError):
        extract.extract(example, 'something')
    with pytest.raises(ValueError):
        extract.extract(example, 'something.a.a')

def test_overloaded_function():
    match = extract.extract(example, 'overloaded_add')
    assert isinstance(match, list)
    assert len(match) == 2
    assert match[0]['docstring']
    assert 'Some more' in match[0]['docstring']
    assert not 'arg3' in match[0]['docstring']
    assert match[1]['docstring']
    assert 'Some more' in match[1]['docstring']
    assert 'arg3' in match[1]['docstring']

def test_multiline_signature():
    example = 'fixtures/example.py'
    match = extract.extract(example, 'multiline')
    assert match['function'] == 'multiline'

def test_extract_pep484():
    match = extract.extract(example, 'function_with_docstring_pep484')
    assert match['function'] == 'function_with_docstring_pep484'
    assert match['signature'] == '(arg0: int, arg1: bool = True) -> bool'
    args = match['parsed_signature']['args']
    return_annotation = match['parsed_signature']['return_annotation']
    assert args['arg0'] == 'int'
    assert args['arg1'] == 'bool = True'
    assert return_annotation == 'bool'
    assert 'Example of a function with a doc string.' in match['docstring']
    assert 'Some more' in match['docstring']

    # Allow for nested.types in return type annotation
    match = extract.extract(example, 'function_with_docstring_objects_pep484')
    assert match['signature'] == '(arg0: int, arg1: bool = True) -> obj.bool'


def test_pybind_function():
    pybind = extract.PyBindExtract(open(example_pybind).read())
    match = pybind.extract('subtract')
    assert match['function'] == 'subtract'
    assert match['return_annotation'] == 'int'
    assert match['signature'] == '(arg0: int, arg1: int) -> int'
    assert 'Subtract two numbers' in match['docstring']
    assert 'Some other' in match['docstring']
    match = pybind.extract('add_multiline')
    assert match['function'] == 'add_multiline'
    assert match['return_annotation'] == 'int'
    assert match['signature'] == '(arg0: int, arg1: int) -> int'
    assert 'Add two numbers' in match['docstring']

    match = pybind.extract('subtract_expressive')
    assert match['signature'] == '('\
            'arg0: operator.Operator, '\
            'arg1: numpy.ndarray[float64[m, 1]]) -> List[List[int]]'
    assert match['return_annotation'] == 'List[List[int]]'
    assert 'Example of expressive' in match['docstring']

def test_pybind_function_cleaned():
    import inspect  

    docs = \
        """
        __init__(self, arg0: int, arg1: int) -> int
             Initialize.

             Args:
                 arg0: input argument 1.
                 arg1: this description should also get captured.
        """
    docs = inspect.cleandoc(docs)
    pybind = extract.PyBindExtract(docs)
    match = pybind.extract('__init__')
    assert 'captured' in match['docstring'] 

def test_pybind_parse_overloaded():
    pybind = extract.PyBindExtract(open(example_pybind).read())
    match = pybind.extract('add')
    assert isinstance(match, list)
    assert match[0]['function'] == 'add'
    assert match[0]['return_annotation'] == 'int'
    assert match[0]['signature'] == '(arg0: int, arg1: int) -> int'
    assert 'Adds two numbers' in match[0]['docstring']
    assert 'by a colon.' in match[0]['docstring']
    assert match[1]['function'] == 'add'
    assert match[1]['return_annotation'] == 'int'
    assert match[1]['signature'] == '(arg0: int, arg1: int, arg2: int) -> int'
    assert 'Adds three numbers' in match[1]['docstring']
    assert 'by a colon.' in match[1]['docstring']

def test_pybind_class():
    docstring =\
        """
    class  Operations

    The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).
    """
    pybind = extract.PyBindExtract(open(example_pybind).read())
    match = pybind.extract('Operations')
    assert match['class'] == 'Operations'
    assert 'The summary line' in match['docstring'] 
    assert 'If the class' in match['docstring'] 
    assert 'below).' in match['docstring']

def test_pybind_method():
    docstring = \
    """
    operation(self: python_example.Operations, i: int, j: int, op_name: str)
    -> int


      Performs one of the allowed operations.

      Args:
          i (int): The first parameter.
          j (int): The second parameter.
          op_name (str='add'): The type of operation.

      Returns:
          int: If op_name=='add' it perform the sum param1+param2, otherwise 0.

    """
    pybind = extract.PyBindExtract(open(example_pybind).read())
    match = pybind.extract('Operations.operation')
    assert match['class'] == 'Operations'
    assert match['signature'] == '(self: python_example.Operations, ' \
                                 + 'i: int, j: int, op_name: str) -> int'
    assert match['return_annotation'] == 'int'
    assert match['type'] == 'method'
    
    with pytest.raises(NameError): pybind.extract('WrongClassName.operation')

    # Class name can be omitted, but then type is 'function' instead of 'method'
    match = pybind.extract('operation')
    assert match['type'] == 'function'
