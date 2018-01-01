# gdocstr
Parser for google-style docstrings

# Ideas


## Hmm, maybe not make is so complicated
First step is to parse the source code and fetch all docstrings
out = getdocstr('file.c')
returns out['module', 'classes', 'functions']

out['module'] = 'docstr'
out['classes'] = [class1, class2]
class1 = {'name' : , 'docstr', functions}

out['functions'] = [function1, function2]

## 

Fetch the module docstring
>>> minidocs find file.py

Fetch the class docstring from the class `Example`
>>> minidocs find file.py Example

Fetch a function called `function`
>>> minidocs find file.py function

Fetch a method called `method`
>>> minidocs find file.py method

>>> minidocs render file.py method > file.method


## Anchors

"""
Example of a private function with a doc string.
This docstring will be ignore by default.

Args:
    arg1(type) : description for arg1.
    arg2 : description for arg2.

See also:
    `very interesting module` : some note about this
    [Block](block) : some note about this

"""
