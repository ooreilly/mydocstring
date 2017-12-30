import pytest
from ..extract import extract
from .. import parse

def test_extract_section():
    example = 'fixtures/example.py'
    match = extract(example, 'function_with_docstring')
    google = parse.GoogleDocString(match['docstring'])
    google.extract_section('Args')
    google.extract_section('Returns')
    with pytest.warns(UserWarning) : google.extract_section('Not found', require=True)

def test_arguments():
    example = 'fixtures/example.py'
    match = extract(example, 'function_with_docstring')
    docstr = parse.parse(match)

    args = docstr[1]
    args['args'][0]['specifier'] == 'arg1'
    args['args'][0]['signature'] == ['type']
    args['args'][0]['description'] == 'description for arg1'
    args['args'][1]['specifier'] == 'arg2'
    args['args'][1]['signature'] == ['']
    args['args'][1]['description'] == 'description for arg2'

    match = extract(example, 'function_with_invalid_argblock')
    with pytest.raises(ValueError) : parse.parse(match)

def test_parse_section():
    example = 'fixtures/example.py'
    match = extract(example, 'function_with_docstring')
    google = parse.GoogleDocString(match['docstring'])
    section = google.extract_section('Args')
    output = google.parse_section(section)

def test_parse_sections():
    example = 'fixtures/example.py'
    match = extract(example, 'function_with_docstring')
    google = parse.GoogleDocString(match['docstring'])
    sections = google.extract_sections()

def test_summary():
    test_str = 'This is a test.\n This line is not part of the summary'
    assert parse.summary(test_str) == 'This is a test.'
