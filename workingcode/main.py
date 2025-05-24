from lexer import lexer
from parser import Parser
from interpreter import Interpreter

def main():
    code = '''
    % Declare some variables
    integerNamed <counter> hasTheValueOf <5>#
    textValueNamed <greeting> hasTheValueOf <"Hello, World!">#
    
    % Define a function
    functionNamed <sayHello> withParameters <n> {
        print <"Hello, "> toterminal#
        print <n> toterminal#
    }
    
    % Call the function
    callFunction <sayHello> withArguments <"LeBron">#
    
    % Simple if condition
    ifCondition <counter < 10> isTrue {
        print <"Counter is less than 10!"> toterminal#
    }
    
    % If condition with equality operator
    ifCondition <counter == 5> isTrue {
        print <"Counter is exactly 5!"> toterminal#
    }
    '''

    tokens = lexer(code)
    print("\nTokens (one per line):")
    for i, token in enumerate(tokens):
        print(f"{i}: {token[0]} = '{token[1]}'")
    print("\nTotal tokens:", len(tokens))

    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)
    interpreter = Interpreter()
    result = interpreter.interpret(ast)
    
    print("\nAST Structure:")
    for i, node in enumerate(ast):
        print(f"Node {i+1}: {type(node).__name__}")
    
    print("\nExecution Results:")
    print("------------------")
    for item in result:
        if isinstance(item, list):
            for subitem in item:
                if isinstance(subitem, str) and subitem.startswith("Output:"):
                    print(subitem[8:].strip())
        elif isinstance(item, str):
            if item.startswith("Output:"):
                print(item[8:].strip())
            else:
                print(f"[System]: {item}")

if __name__ == "__main__":
    main()
