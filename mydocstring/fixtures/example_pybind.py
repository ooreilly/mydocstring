"""

subtract(arg0: int, arg1: int) -> int

       Subtract two numbers

       Some other explanation about the subtract function.

subtract_expressive(arg0: operator.Operator, arg1: numpy.ndarray[float64[m, 1]]) -> List[List[int]]

        Example of expressive type annontation.


add_multiline(arg0: int,
              arg1: int) -> int

        Add two numbers

Overloaded function.

    1. add(arg0: int, arg1: int) -> int


        Adds two numbers

        Args:
            arg0 (int): The first parameter.
                Second line of description should be indented.
            arg1 (int): The second parameter.

        Returns:
            int: The sum arg0+arg1

            The return type is optional and may be specified at the beginning of
            the ``Returns`` section followed by a colon.


      2. add(arg0: int, arg1: int, arg2: int) -> int


          Adds three numbers

          Args:
              arg0 (int): The first parameter.
                  Second line of description should be indented.
              arg1 (int): The second parameter.
              arg2 (int): The third parameter.

          Returns:
              int: The sum arg0+arg1+arg2.

              The return type is optional and may be specified at the beginning of
              the ``Returns`` section followed by a colon.

class  Operations

    The summary line for a class docstring should fit on one line.
    
    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

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
