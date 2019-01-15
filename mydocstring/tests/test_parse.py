import pytest
from mydocstring.extract import extract
from mydocstring import parse

def setup_google(filename='fixtures/example.py', 
                 function='function_with_docstring', 
                 signature=None, 
                 config=None
                 ):
    match = extract(filename, function)
    google = parse.GoogleDocString(match['docstring'], signature=signature,
                config=config)
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

def test_check_arguments():
    # Missing documentation
    signature = '(arg1: int, arg2:int = True, arg3: int = True)'
    in_args = parse.parse_signature(signature)
    google = setup_google(signature=in_args)
    with pytest.warns(UserWarning) : google.parse()
    
    # Annotation mismatch
    signature = '(arg1: int, arg2:int = True)'
    in_args = parse.parse_signature(signature)
    google = setup_google(signature=in_args)
    with pytest.warns(UserWarning) : google.parse()

    # Unknown argument
    signature = '(arg1: (type))'
    in_args = parse.parse_signature(signature)
    google = setup_google(signature=in_args)
    with pytest.warns(UserWarning) : google.parse()
    

    # Do not check annotations if signature does not contain any
    signature = '(arg1, arg2)'
    in_args = parse.parse_signature(signature)
    google = setup_google(signature=in_args)
    google.parse()

    # Ok
    signature = '(arg1: type, arg2:int = True)'
    in_args = parse.parse_signature(signature)
    google = setup_google(signature=in_args)
    google.parse()

    # Disable checks
    signature = '(arg1: int, arg2:int = True, arg3: int = True)'
    in_args = parse.parse_signature(signature)
    google = setup_google(signature=in_args, config = {'check_args' : 0})
    google.parse()

    # Do not warn when self is not documented
    signature = '(self: int, arg1: int, arg2:int = True)'
    in_args = parse.parse_signature(signature)
    google = setup_google(signature=in_args,function='ExampleOldClass.__init__',
                          config={'exclude_warn_if_no_arg_doc' : ['self',
                              'arg1']})
    google.parse()

def test_override_annotations():
    signature = '(arg1: type, arg2:int = True)'
    in_args = parse.parse_signature(signature)

    google = setup_google(signature=in_args)
    docstr = google.parse()
    args = docstr[1]
    assert args['args'][0]['field'] == 'arg1'
    assert args['args'][0]['signature'] == in_args['args']['arg1']
    assert args['args'][1]['field'] == 'arg2'
    assert args['args'][1]['signature'] == in_args['args']['arg2']

    # Do not override if signature does not have any annotations
    signature = '(arg1, arg2)'
    in_args = parse.parse_signature(signature)
    google = setup_google(signature=in_args)
    docstr = google.parse()
    args = docstr[1]
    assert args['args'][0]['field'] == 'arg1'
    assert args['args'][0]['signature'] == '(type)'

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
    google.extract_sections()

def test_summary():
    test_str = 'This is a test.\n This line is not part of the summary'
    assert parse.summary(test_str) == 'This is a test.'

def test_json():
    from json import loads
    google = setup_google()
    google.parse()
    d = loads(google.__json__())
    assert d == google.data

def test_parse_args():
    signature = '(arg0, arg1)'
    args = parse.parse_signature(signature)
    assert 'arg0' in args['args'] and args['args']['arg0'] == ''
    assert 'arg1' in args['args'] and args['args']['arg1'] == ''

def test_parse_args_pep484():
    signature = '(arg0: int, arg1: int)'
    args = parse.parse_signature(signature)
    assert 'arg0' in args['args'] and args['args']['arg0'] == 'int'
    assert 'arg1' in args['args'] and args['args']['arg1'] == 'int'

def test_parse_optional_args_pep484():
    signature = "(self: python_example.Operations," \
                + "i: int, j: int, op_name: str='add')"
    args = parse.parse_signature(signature)
    assert 'self' in args['args'] and \
            args['args']['self'] == 'python_example.Operations'
    assert 'i' in args['args'] and args['args']['i'] == 'int'
    assert 'j' in args['args'] and args['args']['j'] == 'int'
    assert 'op_name' in args['args'] and args['args']['op_name'] == "str='add'"

def test_parse_cpp_pep484():
    signature = "(example: Example::ExampleOperator," \
                + "i: int, j: int, op_name: str='add')"
    args = parse.parse_signature(signature)
    assert 'example' in args['args']

    signature = "(example: Example::ExampleOperator<int, int>," \
                + "i: int, j: int, op_name: str='add')"
    args = parse.parse_signature(signature)
    assert 'example' in args['args']

def test_parse_code():
    code = """
           Code block 1.
           >>> a = 1
           >>> a
           1

           Code block 2.
           >>> b = 1
           >>> b
           1

           Each block must end with an empty line. This text is not part of the
           code block.
           """
    formatted_code = parse.mark_code_blocks(code)
    assert 'Code block 1.\n' in formatted_code
    assert '```python\n\n           >>> a\n' in formatted_code
    assert '```python\n\n           >>> b\n' in formatted_code

def test_undefined_headers():
    example = 'fixtures/example.py'
    match = extract(example, 'function_with_undefined_header')
    with pytest.warns(UserWarning) : \
            docstring = parse.GoogleDocString(match['docstring']).parse()
    assert docstring[0]['args'] == []

    config = {'ignore_args_for_undefined_headers': False}
    with pytest.warns(UserWarning) : \
            docstring = parse.GoogleDocString(match['docstring'],
                                              config=config).parse()
    assert not docstring[0]['args'] == []

def test_get_config():
    default = {'arg1': 'test', 'arg2' : 'test'}
    config = {'arg1' : 'new'}
    config = parse.get_config(default, config)
    assert 'arg2' in config
    assert config['arg1'] == 'new'

    with pytest.warns(UserWarning) : parse.get_config(default, {'unknown' : 0})


