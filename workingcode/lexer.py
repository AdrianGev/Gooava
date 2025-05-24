import re

def lexer(code):
    """Tokenize the input code into a list of tokens."""
    # Define token patterns
    patterns = [
        # Keywords
        ('KEYWORD', r'\b(print|toterminal|functionNamed|withParameters|callFunction|return|withArguments|integerNamed|textValueNamed|hasTheValueOf|ifCondition|isTrue|elseCondition|whileLoop|repeatUntil|forLoop|from|to|step|arrayNamed|structNamed|withFields|accessField|withIndex)\b'),
        # Logical operators (must come before NAME)
        ('LOGICAL', r'\b(and|or|not)\b'),
        # Literals
        ('NUMBER', r'-?\d+(\.\d+)?'),
        ('STRING', r'"[^"]*"'),
        # Identifiers
        ('NAME', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        # Operators
        ('OPERATOR', r'[+\-*/^]'),
        ('COMPARISON', r'(==|!=|<=|>=)'),  # Multi-char comparisons
        # Brackets and braces
        ('BRACKET', r'[<>]'),
        ('PARENTHESIS', r'[()]'),
        ('BRACE', r'[{}]'),
        ('SQUARE_BRACKET', r'[\[\]]'),
        # Other symbols
        ('COMMA', r','),
        ('TERMINATOR', r'#'),
        # Comments and whitespace (to be filtered out)
        ('COMMENT', r'%[^\n]*'),
        ('WHITESPACE', r'[ \t\n\r]+'),
    ]
    
    # Build regex pattern
    regex = '|'.join('(?P<%s>%s)' % (name, pattern) for name, pattern in patterns)
    
    # Tokenize
    tokens = []
    bracket_stack = []  # Track bracket nesting for disambiguation
    
    # Process each match
    for match in re.finditer(regex, code):
        kind = match.lastgroup
        value = match.group()
        
        # Skip comments and whitespace
        if kind in ['COMMENT', 'WHITESPACE']:
            continue
        
        # Handle bracket disambiguation
        if kind == 'BRACKET':
            if value == '<':
                # Check if this is likely a bracket or comparison
                prev_token = tokens[-1] if tokens else None
                
                if prev_token and prev_token[0] == 'KEYWORD':
                    # After keywords like 'print', 'functionNamed', etc.
                    bracket_stack.append('bracket')
                elif prev_token and prev_token[0] == 'NAME' and len(bracket_stack) == 0:
                    # Likely a comparison operator
                    kind = 'COMPARISON'
                else:
                    bracket_stack.append('bracket')
            
            elif value == '>':
                if bracket_stack and bracket_stack[-1] == 'bracket':
                    bracket_stack.pop()
                else:
                    kind = 'COMPARISON'
        
        # Add token to list
        tokens.append((kind, value))
    
    return tokens
