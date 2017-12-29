import pytest
from ..extract import extract
from .. import parse

def test_section():
    example = 'fixtures/example.py'
    match = extract(example, 'function_with_docstring')
    google = parse.GoogleDocString(match['docstring'])
    google.section('Args')
    google.section('Returns')
    with pytest.warns(UserWarning) : google.section('Not found', require=True)

def test_arguments():
    example = 'fixtures/example.py'
    match = extract(example, 'function_with_docstring')
    docstr = parse.parse(match)

    args = docstr['args']
    args[0]['name'] == 'arg1'
    args[0]['signature'] == ['type']
    args[0]['description'] == 'description for arg1'
    args[1]['name'] == 'arg2'
    args[1]['signature'] == ['']
    args[1]['description'] == 'description for arg2'

    match = extract(example, 'function_with_invalid_argblock')
    with pytest.raises(ValueError) : parse.parse(match)

def test_return():
    pass
