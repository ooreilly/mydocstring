import pytest
from ..extract import extract
from ..parse import parse
def test_arguments():

    example = 'fixtures/example.py'
    match = extract(example, 'function_with_docstring')
    docstr = parse(match)

    args = docstr['args']
    args[0]['name'] == 'arg1'
    args[0]['signature'] == ['type']
    args[0]['description'] == 'description for arg1'
    args[1]['name'] == 'arg2'
    args[1]['signature'] == ['']
    args[1]['description'] == 'description for arg2'

    match = extract(example, 'function_with_invalid_argblock')
    with pytest.raises(ValueError) : parse(match)
