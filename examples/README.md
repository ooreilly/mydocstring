# Command line tool
To learn how to use the command line tool, simply type `mydocstring --help`.

Let's extract the docstring from the following example code and convert it to
Markdown:
```python
def example_function(arg1, arg2=1):
    """
    This is an example of a docstring that conforms to the Google style guide. 
    The indentation uses four spaces (no tabs). Note that each section starts
    with a header such as `Arguments` or `Returns` and its contents is indented.

    Arguments:

        arg1 (`int`): This description for this argument fits on one line.
        arg2 (`int`, optional): This description is too long to fit on a
            single line. Note that it is continued by being indented. 

    Returns:

        `bool` :  Stating the return type here is optional.

        We can continue putting explanations in this section as long as the text
        is indented.

    This text is no longer indented and therefore not part of the `Returns`
    section.

    Raises:

        ValueError: This is exception is raised when arg1 and arg2 are equal.

    """
    if arg1 == arg2:
        raise ValueError("`arg1` and `arg2` cannot be equal.")
    if arg1 > arg2:
        return True
    else: 
        return False
```
This example code can be found here: [example.py](example.py).

To convert to Markdown, we simply use
```
$ docstring examples/example.py example_function --markdown > examples/example_py.md
```
The following rendered Markdown is produced: 

---
# example_function
```python
def example_function(arg1, arg2=1):
```

---


This is an example of a docstring that conforms to the Google style guide. 
The indentation uses four spaces (no tabs). Note that each section starts
with a header such as `Arguments` or `Returns` and its contents is indented.

## Arguments
* **arg1** (`int`) : This description for this argument fits on one line.
* **arg2** (`int`, optional) : This description is too long to fit on a
    single line. Note that it is continued by being indented. 


## Returns
*  Stating the return type here is optional.


We can continue putting explanations in this section as long as the text
is indented.

---
This text is no longer indented and therefore not part of the `Returns`
section.

## Raises
* **ValueError**  : This is exception is raised when arg1 and arg2 are equal.




## Source
```python
def example_function(arg1, arg2=1):
    if arg1 == arg2:
        raise ValueError("`arg1` and `arg2` cannot be equal")
    if arg1 > arg2:
        return True
    else: 
        return False

```

---
The output above can also be found here: [example_py.md](example_py.md).

If you are not satisfied with the resulting Markdown, you can provide your own
[mako](http://makotemplates.org) template

```
$ docstring examples/example.py example_function --markdown --template customization.md
```
Go to [mydocstring/templates/](../mydocstring/templates/) to see how to make your own
template. 

It is also possible to output plain-text, or JSON-data using the flags args
`--text` and `--json`. 


