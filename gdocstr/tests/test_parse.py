import pytest
from ..extract import extract
from .. import parse

def setup_google(filename='fixtures/example.py', function='function_with_docstring'):
    match = extract(filename, function)
    google = parse.GoogleDocString(match['docstring'])
    return google

def get_docstring1():
    docstring = []
    docstring.append("""Short description.
    Example of a function with a doc string.
    """
    )
    docstring.append(
    """Args:
        arg1 (`int`): This description for this argument fits on one line.
        arg2 (`int`, optional): This description is too long to fit on a 
            single line. Note that it is continued by being indented.
    """
    )
    docstring.append(
    """Returns:
        bool: `True` or `False`. Defaults to `True`.
                                                    
        The return section can also have a detailed description that spans
        multiple lines. It is important that this description is indented.
    """)
    docstring.append(
    """This text is no longer indented and therefore not part of the `Returns`
    section.
    """)

    return docstring

def test_arguments():
    google = setup_google()
    docstr = google.parse()

    args = docstr[1]
    assert args['args'][0]['field'] == 'arg1'
    assert args['args'][0]['signature'] == '(type)'
    assert args['args'][0]['description'] == 'description for arg1.'
    assert args['args'][1]['field'] == 'arg2'
    assert args['args'][1]['signature'] == ''
    assert args['args'][1]['description'] == """description for arg2
    that spans multiple lines."""

def test_extract_sections():
    import re
    google = setup_google()

    
    len(google._parsing['sections']) == 4
    txt = get_docstring1()
    google = parse.GoogleDocString('\n'.join(txt))
    google.parse()

    expr = ['Short description','Example of a function with a doc string.']

    for ex in expr:
        assert re.compile(ex, re.M).findall(google._parsing['sections'][0])

    # Too difficult to get exact match, so result to approximate match by
    # checking for key features such as text for more than a single line.
    expr = ['arg1', '(`int`)', 
            'This description for this argument fits on one line.']
    for ex in expr:
        assert re.compile(ex, re.M).findall(google._parsing['sections'][1])

    expr = ['arg2', '(`int`, optional)', 'continued by being indented.']
    for ex in expr:
        assert re.compile(ex, re.M).findall(google._parsing['sections'][1])

    expr = ['bool', 'Defaults to', 
            'It is important that this description is indented.']
    for ex in expr:
        assert re.compile(ex, re.M).findall(google._parsing['sections'][2])

    expr = ['This text is no longer indented and therefore']
    for ex in expr:
        assert re.compile(ex, re.M).findall(google._parsing['sections'][3])

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

