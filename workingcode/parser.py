from ast import Function, Call, Return, Print, VariableDeclaration, IfCondition, ASTNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, expected_type=None):
        token = self.current_token()
        if token and (expected_type is None or token[0] == expected_type):
            self.pos += 1
            return token
        raise ValueError(f"Expected {expected_type}, got {token}")

    def parse(self):
        nodes = []
        while self.pos < len(self.tokens):
            token = self.current_token()
            if not token:
                break
                
            if token[0] == 'BRACE' and token[1] == '}':
                break
                
            if token[0] == 'KEYWORD':
                if token[1] == 'functionNamed':
                    nodes.append(self.parse_function())
                elif token[1] == 'callFunction':
                    nodes.append(self.parse_call())
                elif token[1] == 'return':
                    nodes.append(self.parse_return())
                elif token[1] == 'print':
                    nodes.append(self.parse_print())
                elif token[1] in ['integerNamed', 'textValueNamed']:
                    nodes.append(self.parse_variable_declaration())
                elif token[1] == 'ifCondition':
                    nodes.append(self.parse_if_condition())
                else:
                    raise ValueError(f"Unexpected keyword: {token[1]}")
            else:
                raise ValueError(f"Unexpected token: {token}")
        return nodes

    def parse_function(self):
        self.eat('KEYWORD')  # functionNamed
        self.eat('BRACKET')  # <
        name = self.eat('NAME')[1]
        self.eat('BRACKET')  # >
        self.eat('KEYWORD')  # withParameters
        self.eat('BRACKET')  # <
        parameters = self.eat('NAME')[1]
        self.eat('BRACKET')  # >
        self.eat('BRACE')  # {
        body = self.parse()  # Parse until we hit the closing brace
        self.eat('BRACE')  # }
        return Function(name=name, parameters=[parameters], body=body)

    def parse_call(self):
        self.eat('KEYWORD')  # callFunction
        self.eat('BRACKET')  # <
        name = self.eat('NAME')[1]
        self.eat('BRACKET')  # >
        self.eat('KEYWORD')  # withArguments
        self.eat('BRACKET')  # <
        arguments = [self.eat('STRING')[1].strip('"')]
        self.eat('BRACKET')  # >
        self.eat('TERMINATOR')  # #
        return Call(name=name, arguments=arguments)

    def parse_return(self):
        self.eat('KEYWORD')  # return
        self.eat('BRACKET')  # <
        value = self.eat('STRING')[1]
        self.eat('BRACKET')  # >
        return Return(value=value)

    def parse_print(self):
        self.eat('KEYWORD')  # print
        self.eat('BRACKET')  # <
        token = self.current_token()
        
        # Check if this is an arithmetic expression
        if token[0] in ['NUMBER', 'OPERATOR', 'NAME', 'PARENTHESIS']:
            expression = ''
            # Keep track of parentheses balance
            paren_count = 0
            
            while True:
                token = self.current_token()
                if token[0] == 'PARENTHESIS':
                    if token[1] == '(':
                        paren_count += 1
                    else:
                        paren_count -= 1
                        if paren_count < 0:
                            raise ValueError("Unmatched parentheses in expression")
                
                if token[0] in ['NUMBER', 'OPERATOR', 'NAME', 'PARENTHESIS']:
                    expression += token[1]
                    self.eat()
                else:
                    break
                    
            if paren_count != 0:
                raise ValueError("Unmatched parentheses in expression")
                
            self.eat('BRACKET')  # >
            self.eat('KEYWORD')  # toterminal
            self.eat('TERMINATOR')  # #
            return Print(value=None, is_variable=False, expression=expression)
            
        # Regular print statement
        if token[0] == 'STRING':
            value = self.eat('STRING')[1].strip('"')
            is_variable = False
        else:
            value = self.eat('NAME')[1]
            is_variable = True
        self.eat('BRACKET')  # >
        self.eat('KEYWORD')  # toterminal
        self.eat('TERMINATOR')  # #
        return Print(value=value, is_variable=is_variable)

    def parse_variable_declaration(self):
        var_type = self.eat('KEYWORD')[1]  # integerNamed or textValueNamed
        self.eat('BRACKET')  # <
        name = self.eat('NAME')[1]
        self.eat('BRACKET')  # >
        self.eat('KEYWORD')  # hasTheValueOf
        self.eat('BRACKET')  # <
        if var_type == 'integerNamed':
            value = self.eat('NUMBER')[1]
        else:
            value = self.eat('STRING')[1].strip('"')
        self.eat('BRACKET')  # >
        self.eat('TERMINATOR')  # #
        return VariableDeclaration(var_type=var_type, name=name, value=value)

    def parse_if_condition(self):
        self.eat('KEYWORD')  # ifCondition
        self.eat('BRACKET')  # <
        
        # Parse the condition
        condition_tokens = []
        
        # Keep parsing until we find the closing bracket for the condition
        while self.pos < len(self.tokens):
            token = self.current_token()
            if not token:
                raise ValueError("Unexpected end of tokens while parsing condition")
                
            # If we find the closing bracket, we're done parsing the condition
            if token[0] == 'BRACKET' and token[1] == '>':
                break
                
            # Add the token to our condition tokens
            condition_tokens.append(token)
            self.pos += 1
        
        # Reconstruct the condition as a string
        condition = ' '.join(token[1] for token in condition_tokens)
        
        # Consume the closing bracket
        if self.pos < len(self.tokens) and self.current_token()[0] == 'BRACKET' and self.current_token()[1] == '>':
            self.eat('BRACKET')  # >
        else:
            raise ValueError(f"Expected closing bracket '>', got {self.current_token() if self.pos < len(self.tokens) else 'None'}")
        
        self.eat('KEYWORD')  # isTrue
        self.eat('BRACE')  # {
        body = self.parse()  # Parse until we hit the closing brace
        self.eat('BRACE')  # }
        
        # Check for else condition
        else_body = None
        if self.pos < len(self.tokens) and self.current_token()[0] == 'KEYWORD' and self.current_token()[1] == 'elseCondition':
            self.eat('KEYWORD')  # elseCondition
            self.eat('BRACE')  # {
            else_body = self.parse()  # Parse until we hit the closing brace
            self.eat('BRACE')  # }
            
        return IfCondition(condition=condition, body=body, else_body=else_body)
