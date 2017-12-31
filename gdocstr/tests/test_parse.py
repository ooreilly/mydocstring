import pytest
from ..extract import extract
from .. import parse

def setup_google(filename='fixtures/example.py'):
    match = extract(filename, 'function_with_docstring')
    google = parse.GoogleDocString(match)
    return google

def test_extract_section():
    google = setup_google()
    google.extract_section('Args')
    google.extract_section('Returns')
    with pytest.warns(UserWarning) : google.extract_section('Not found', require=True)

def test_arguments():
    google = setup_google()
    docstr = google.parse()

    print(docstr)
    args = docstr[1]
    args['args'][0]['field'] == 'arg1'
    args['args'][0]['signature'] == ['type']
    args['args'][0]['description'] == 'description for arg1'
    args['args'][1]['field'] == 'arg2'
    args['args'][1]['signature'] == ['']
    args['args'][1]['description'] == 'description for arg2'

def test_parse_section():
    google = setup_google()
    section = google.extract_section('Args')
    output = google.parse_section(section)

def test_parse_sections():
    google = setup_google()
    sections = google.extract_sections()

def test_summary():
    test_str = 'This is a test.\n This line is not part of the summary'
    assert parse.summary(test_str) == 'This is a test.'

def test_json():
    from json import loads
    google = setup_google()
    google.parse()
    d = loads(google.__json__())
    assert d == google.data

