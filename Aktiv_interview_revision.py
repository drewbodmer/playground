class Expression:
    """
    Represents an algebraic expression: add, subtract, multiply, or divide.
    """

    def __init__(self):
        pass

    def __str__(self):
        return str(self.val)


class Operation(Expression):
    """
    Contains a list of Expressions
    """

    def __init__(self, val: list[Expression]):
        self.val = val
        super().__init__()

    def __str__(self):
        return str("(" + " ".join([str(v) for v in self.val]) + ")")

    def swap(self, i1: int, i2: int):  # swap two expressions given their indexes
        expr_len = len(self.val)
        if i1 >= expr_len or i2 >= expr_len or i1 < 0 or i2 < 0:
            raise ValueError("Cannot swap, index out of range")
        intermediate = self.val[i1]
        self.val[i1] = self.val[i2]
        self.val[i2] = intermediate

    def move(self, i1: int, i2: int):  # move the expression at index 1 to index 2
        expr_len = len(self.val)
        if i1 >= expr_len or i2 >= expr_len or i1 < 0 or i2 < 0:
            raise ValueError("Cannot move, index out of range")
        intermediate = self.val[i1]
        self.val = self.val[:i1] + self.val[i1+1:]
        self.val.insert(i2, intermediate)


class Value:
    def __init__(self, val: str or int):
        self.val = val


class Char(Value):
    def __init__(self, val: str):
        super().__init__(val)


class Int(Value):
    def __init__(self, val: int):
        super().__init__(val)


class Add(Expression):
    def __init__(self, val: Operation or Value):
        self.val = val
        super().__init__()

    def __str__(self):
        return '+ ' + str(self.val)


class Sub(Expression):
    def __init__(self, val: Operation or Value):
        self.val = val
        super().__init__()

    def __str__(self):
        return '- ' + str(self.val)


class Mul(Expression):
    def __init__(self, val: Operation or Value):
        self.val = val
        super().__init__()

    def __str__(self):
        return '* ' + str(self.val)


class Div(Expression):
    def __init__(self, val: Operation or Value):
        self.val = val
        super().__init__()

    def __str__(self):
        return '/ ' + str(self.val)


# Operation(Add(1), Mul(2), Sub(1))
print('prelim tests ======================')
expr = Operation([Int(3), Sub('a'), Add(4)])  # 3 - a + 4
print(expr)
expr.swap(0, 1)
print(expr)
expr.swap(1, 2)
print(expr)

print('real tests ========================')
# 2(x + 1) + 5y + z
term1 = Operation([Int(2), Mul(Operation([Char('x'), Add(1)]))])
term2 = Operation([Int(5), Mul('y')])
term3 = Operation('z')

expr = Operation([Add(term1), Add(term2), Add(term3)])
print(expr)
expr.swap(2, 0)
expr.swap(2, 1)
# z + 2(x + 1) + 5y
print(expr)
expr.move(0, 2)
# 2(x + 1) + 5y + z
print(expr)
expr.swap(2, 1)
# 2(x + 1) + z + 5y
print(expr)

print('edge cases ========================')
# Testing edge cases don't crash anything
expr = Operation([])
print(expr)
expr = Operation([Char('x'), Int(1)])
try:
    expr.swap(200, 0)
except ValueError as e:
    print(e)

expr.swap(0, 0)
print(expr)

try:
    expr.move(0, -10)
except ValueError as e:
    print(e)

"""
Considerations:

I decided the simplest way to do this was to have an Expression object that represents any expression possible (in this case numbers, symbols, and operations).
Then for each type of expression, I added a subclass with the name of the expression, e.g. Int (unsigned integer), Char (symbol), etc.

For an internal representation, this could have been simplified to use just a single Expression object that contains a list of Expressions, however I felt that
implementation would be impractical for implementing evaluation. I also wanted a simple way to print the constructed expression to check my code.

Parentheses in this implementation are fairly simple, as an evaluator would have to evaluate nested Expressions first.

To rearrange the Expressions, I implemented a swap function and a move function. The swap function takes two numbers that each represent the index of an expression.
The function swaps those two expressions with each other.

Move takes two indexes, the index of the expression to move and the destination index. It moves the expression from the first index to the second.

REVISION ===========================================================================================:

To accomodate expressions with mixed interleaved operators, I added an Operation class. Expressions can now be one of Add, Sub, Mul, Div, or Operation.
I added a second superclass called Value, which represents a Char or an Int. The non-Operation expressions can take either an
Operation or a Value. To construct an interleaved operation, create an Operation and pass it a list of expressions:

Operation([Int(3), Sub('a'), Div(4)]) for 3 - a / 4

This allows for interleaved mixed operators. 


AST:
define MATH:
  [Int Integer]
  [Char Symbol]
  [Add List[MATH]]
  [Sub List[MATH]]
  [Mul List[MATH]]
  [Div List[MATH]]
"""
