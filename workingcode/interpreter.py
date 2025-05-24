import re
from ast import ASTNode, Function, Call, Return, Print, VariableDeclaration, IfCondition, AnonymousFunction, HigherOrderFunction

class Interpreter:
    def __init__(self):
        self.functions = {}
        self.variables = {}

    def visit(self, node):
        if isinstance(node, list):
            results = []
            for n in node:
                result = self.visit(n)
                if result is not None:
                    results.append(result)
            return results

        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Function(self, node):
        # Store the function definition in the interpreter's function table
        self.functions[node.name] = node
        return f"Function '{node.name}' defined."

    def visit_Call(self, node):
        # Find the function definition
        func = self.functions.get(node.name)
        if not func:
            raise Exception(f"Function '{node.name}' is not defined.")

        # Check arguments and execute the function body
        if len(func.parameters) != len(node.arguments):
            raise Exception(f"Function '{node.name}' expects {len(func.parameters)} arguments, got {len(node.arguments)}.")

        # Bind arguments to parameters
        old_vars = self.variables.copy()
        for param, arg in zip(func.parameters, node.arguments):
            self.variables[param] = arg

        # Execute the function body
        results = []
        for stmt in func.body:
            result = self.visit(stmt)
            if result is not None:
                results.append(result)

        # Restore old variables
        self.variables = old_vars
        return results

    def visit_Return(self, node):
        # Return the evaluated value of the return statement
        return node.value

    def visit_Print(self, node):
        # Handle print statement
        if node.expression is not None:
            # Handle arithmetic expression
            result = self.evaluate_arithmetic(node.expression)
            return f"Output: {result}"
            
        if node.is_variable:
            # Handle variable printing
            if node.value not in self.variables:
                raise Exception(f"Variable '{node.value}' is not defined")
            value = self.variables[node.value]
        else:
            # Handle string literal printing
            if isinstance(node.value, str) and node.value.startswith('"') and node.value.endswith('"'):
                value = node.value[1:-1]  # Remove the quotes
            else:
                value = node.value
                
        return f"Output: {value}"

    def visit_VariableDeclaration(self, node):
        # Store variable in the interpreter's variable table
        if node.var_type == 'integerNamed':
            self.variables[node.name] = int(node.value)
        elif node.var_type == 'textValueNamed':
            self.variables[node.name] = node.value
        return f"Variable '{node.name}' defined with value: {node.value}"

    def visit_IfCondition(self, node):
        # Evaluate condition
        condition = self.evaluate_condition(node.condition)
        if condition:
            return self.visit(node.body)
        elif node.else_body is not None:
            return self.visit(node.else_body)
        return None

    def evaluate_condition(self, condition):
        # Enhanced condition evaluation with support for logical operators
        condition = condition.strip()
        
        # Check for logical operators
        if ' and ' in condition:
            parts = condition.split(' and ')
            return all(self.evaluate_condition(part) for part in parts)
        
        if ' or ' in condition:
            parts = condition.split(' or ')
            return any(self.evaluate_condition(part) for part in parts)
        
        if condition.startswith('not '):
            return not self.evaluate_condition(condition[4:])
        
        # Simple comparison evaluation
        parts = condition.split()
        if len(parts) == 3:
            left, op, right = parts
            
            # Handle variable substitution
            if left in self.variables:
                left_val = self.variables[left]
            else:
                try:
                    left_val = int(left) if left.isdigit() or (left[0] == '-' and left[1:].isdigit()) else left
                except ValueError:
                    left_val = left
            
            if right in self.variables:
                right_val = self.variables[right]
            else:
                try:
                    right_val = int(right) if right.isdigit() or (right[0] == '-' and right[1:].isdigit()) else right
                except ValueError:
                    right_val = right
            
            # Handle different comparison operators
            if op == '<':
                return left_val < right_val
            elif op == '>':
                return left_val > right_val
            elif op == '<=':
                return left_val <= right_val
            elif op == '>=':
                return left_val >= right_val
            elif op == '==':
                return left_val == right_val
            elif op == '!=':
                return left_val != right_val
        
        # If we can't evaluate, default to False
        return False

    def evaluate_arithmetic(self, expression):
        """Evaluates arithmetic expressions like '1+2', '5*3', 'x+5', etc."""
        try:
            # Check if this is just a string or variable, not an arithmetic expression
            if expression.startswith('"') and expression.endswith('"'):
                # It's a string literal, just return it without quotes
                return expression[1:-1]
            
            # Check if it's a variable name
            if expression in self.variables:
                return self.variables[expression]
            
            # Replace variable names with their values
            for var_name, var_value in self.variables.items():
                # Only replace full variable names, not parts of other names
                expression = re.sub(r'\b' + var_name + r'\b', str(var_value), expression)
            
            # Check if it contains arithmetic operators
            if any(op in expression for op in '+-*/^()'):
                # Basic security check to ensure only allowed operations
                allowed_chars = set('0123456789+-*/%^() .')
                if not all(c in allowed_chars for c in expression):
                    # If it contains invalid characters but no arithmetic operators,
                    # it might be a string or variable that wasn't recognized
                    return expression
                
                # Handle power operator (^) by replacing with Python's **
                expression = expression.replace('^', '**')
                
                # Evaluate the expression
                result = eval(expression)  # In a production environment, use a safer evaluation method
                
                # Format the result based on its type
                if isinstance(result, (int, float)):
                    if result.is_integer():
                        return int(result)
                    return round(result, 6)  # Limit decimal places for floats
                
                return result
            else:
                # If no arithmetic operators, just return the expression as is
                return expression
            
        except Exception as e:
            # If evaluation fails, it might be a string or other non-arithmetic value
            return expression

    def interpret(self, ast):
        return self.visit(ast)
