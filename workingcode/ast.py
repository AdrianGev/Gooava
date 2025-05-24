# Abstract Syntax Tree (AST) Node Definitions

class ASTNode:
    """Base class for all AST nodes."""
    pass

class Function(ASTNode):
    """Represents a named function."""
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"Function(name={self.name}, parameters={self.parameters}, body={self.body})"

class AnonymousFunction(ASTNode):
    """Represents an anonymous function assigned to a variable."""
    def __init__(self, parameters, body, variable_name):
        self.parameters = parameters
        self.body = body
        self.variable_name = variable_name

    def __repr__(self):
        return f"AnonymousFunction(parameters={self.parameters}, body={self.body}, variable_name={self.variable_name})"

class HigherOrderFunction(ASTNode):
    """Represents a function that takes another function as a parameter."""
    def __init__(self, name, func_param, value_param, body):
        self.name = name
        self.func_param = func_param
        self.value_param = value_param
        self.body = body

    def __repr__(self):
        return (f"HigherOrderFunction(name={self.name}, func_param={self.func_param}, "
                f"value_param={self.value_param}, body={self.body})")

class Call(ASTNode):
    """Represents a function call."""
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"Call(name={self.name}, arguments={self.arguments})"

class Return(ASTNode):
    """Represents a return statement."""
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return(value={self.value})"

class Parameter(ASTNode):
    """Represents a parameter in a function definition."""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Parameter(name={self.name}, value={self.value})"

class NestedFunction(ASTNode):
    """Represents a nested function within another function."""
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return f"NestedFunction(name={self.name}, parameters={self.parameters}, body={self.body})"

class Print(ASTNode):
    """Represents a print statement."""
    def __init__(self, value, is_variable=False, expression=None):
        self.value = value
        self.is_variable = is_variable
        self.expression = expression  # For arithmetic expressions like <1+2>

    def __repr__(self):
        if self.expression is not None:
            return f"Print(expression={self.expression})"
        if self.is_variable:
            return f"Print(variable={self.value})"
        return f"Print(value={self.value})"

class VariableDeclaration(ASTNode):
    """Represents a variable declaration."""
    def __init__(self, var_type, name, value):
        self.var_type = var_type  # integerNamed, textValueNamed, etc.
        self.name = name
        self.value = value

    def __repr__(self):
        return f"VariableDeclaration(type={self.var_type}, name={self.name}, value={self.value})"

class IfCondition(ASTNode):
    """Represents an if condition with optional else block."""
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"IfCondition(condition={self.condition}, body={self.body}, else_body={self.else_body})"
