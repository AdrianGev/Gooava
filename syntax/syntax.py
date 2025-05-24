'''

Gooava Syntax Guide
Comments
Single-line comment: Use % at the beginning of a line.
Example:

% This is a single-line comment

Multi-line comment: Wrap text between %- and -%.
Example:

%-
This is a multi-line comment
which can span multiple lines.
-%
Note: There are no comments for documentation because that takes the fun out of coding.

Variable Declarations
integerNamed
Declares an integer variable.
Syntax:

integerNamed <name> hasTheValueOf <value>#  

Example:

integerNamed <counter> hasTheValueOf <5>#  




decimalNamed
Declares a decimal (floating-point) variable.

Syntax:

decimalNamed <name> hasTheValueOf <value>#  

Example:

decimalNamed <pi> hasTheValueOf <3.14>#  

textValueNamed
Declares a text string.

Syntax:

textValueNamed <name> hasTheValueOf <"value">#  

Example:

textValueNamed <greeting> hasTheValueOf <"Hello, World!">#  

trueOrFalseValueNamed
Declares a boolean variable (true or false).

Syntax:

trueOrFalseValueNamed <name> hasTheValueOf <true/false>#  

Example:

trueOrFalseValueNamed <isRunning> hasTheValueOf <true>#  

listNamed
Declares a list variable.

Syntax:

listNamed <name> hasTheValueOf <[value1, value2, ...]>#  

Example:

listNamed <numbers> hasTheValueOf <[1, 2, 3, 4]>#  


Conditionals
If Condition
Executes code if the condition is true.
Syntax:


ifCondition <condition> isTrue { ... }  
Example:


ifCondition <counter < 10> isTrue {  
    print <"Counter is less than 10!"> toterminal#  
}  


Otherwise If Condition (else if)
Executes code if the previous condition failed and this condition is true.
Syntax:

otherwiseIfCondition <condition> isTrue { ... }  

Example:

otherwiseIfCondition <counter == 10> isTrue {  
    print <"Counter is equal to 10!"> toterminal#  
}  

If All Fail (else)

Executes code if all previous conditions failed.

Syntax:

ifAllFail { ... }  

Example:


ifAllFail {  
    print <"Counter is greater than 10!"> toterminal#  
}  


Loops
Version 1: Range-Based Loop
Syntax:

iterateFrom <start> to <end> incrementUp <step> { ... }  

Example:

iterateFrom <1> to <10> incrementUp <1> {  
    print <"Current value is: " .. counter> toterminal#  
}  

Version 2: Iterable Loop
Syntax:

iterateThroughEach <item> in <[list]> { ... }  

Example:

iterateThroughEach <item> in <[1, 2, 3]> {  
    print <"Item: " .. item> toterminal#  
}  







Version 3: Condition-Based Loop
Syntax:

whileCondition <condition> isTrue { ... }  

Example:

whileCondition <counter < 5> isTrue {  
    integerNamed <counter> hasTheValueOf <counter + 1>#  
}  

Version 4: Key-Value Loop
Syntax:

iterateThroughEach <key>, <value> in <{dictionary}> { ... }  

Example:

iterateThroughEach <key>, <value> in <{"a": 1, "b": 2}> {  
    print <"Key: " .. key .. ", Value: " .. value> toterminal#  
}  








Version 5: Fixed Iteration Loop
Syntax:

repeatTimes <number> { ... }  

Example:

repeatTimes <5> {  
    print <"Repeating this message."> toterminal#  
}  


Logical Operators
and: Logical AND.
Example: <condition1 and condition2>
or: Logical OR.
Example: <condition1 or condition2>
-isFALSE: Negates the condition, because “!” is for factorials and factorials only.

Example:

whileCondition <counter > 5-isFALSE> isTrue {  
    print <"Counter is not greater than 5"> toterminal#  
}  







Example Combined Script


% Initialize variables 
integerNamed <counter> hasTheValueOf <0>#  
listNamed <fruits> hasTheValueOf <["apple", "banana", "cherry"]>#  

% Print initial message
print <"Starting the loop..."> toterminal#  

% Range-Based Loop 
iterateFrom <1> to <5> incrementUp <1> {  
    print <"Range value: " .. counter> toterminal#  
}  

% Iterable Loop 
iterateThroughEach <fruit> in <fruits> {  
    print <"Fruit: " .. fruit> toterminal#  
}  

% Condition-Based Loop 
whileCondition <counter <3> isTrue {  
    print <"Counter: " .. counter> toterminal#  
    integerNamed <counter> hasTheValueOf <counter + 1>#  
}  

% Key-Value Loop  
iterateThroughEach <key>, <value> in <{"x": 1, "y": 2}> {  
    print <"Key: " .. key .. ", Value: " .. value> toterminal#  
}  

% Fixed Iteration Loop
repeatTimes <3> {  
    print <"This repeats exactly three times!"> toterminal#  
} 

Functions

Standard Function (with Default Parameters)
Declares a function with optional default parameter values.
Syntax:
functionNamed <name> withParameters <param1=value1>, <param2=value2> { ... }  

Example:
functionNamed <greet> withParameters <name="World"> {  
    print <"Hello, " .. name .. "!"> toterminal#  
    return <"Greeting Completed">  
}  

Calling the Function:
callFunction <greet> withArguments <>#  
callFunction <greet> withArguments <"Alice">#  

Output:
Hello, World!  
Hello, Alice!  


Nested Functions
Defines a function within another function (nightmare fuel).
Syntax:
functionNamed <outerFunction> withParameters <param1> {  
    functionNamed <innerFunction> withParameters <param2> { ... }  
    return <callFunction <innerFunction> withArguments <value>>  
}  

Example:
functionNamed <calculate> withParameters <x> {  
    functionNamed <square> withParameters <y> {  
        return <y * y>  
    }  
    return <callFunction <square> withArguments <x>>  
}  

Calling the Function:
callFunction <calculate> withArguments <5>#  

Output:
25  


Anonymous Functions
Creates a function without a name and assigns it to a variable.
Syntax:
anonymousFunction withParameters <param1>, <param2> { ... } assignedTo <variableName>#  

Example:
anonymousFunction withParameters <a>, <b> {  
    return <a + b>  
} assignedTo <add>#  

print <add withArguments <10>, <15>> toterminal#  

Output:
25  


Higher-Order Functions
Accepts functions as arguments or returns functions as results.
Syntax:
functionNamed <higherOrderFunction> withParameters <func>, <value> { ... }  

Example:
anonymousFunction withParameters <x> {  
    return <x * 2>  
} assignedTo <double>#  

functionNamed <applyFunction> withParameters <func>, <value> {  
    return <callFunction <func> withArguments <value>>  
}  

print <callFunction <applyFunction> withArguments <double>, <10>> toterminal#  

Output:
20  


Recursive Functions
A function that calls itself.
Syntax:
functionNamed <name> withParameters <param1> { ... }  

Example:
functionNamed <factorial> withParameters <n> {  
    ifCondition <n <= 1> isTrue {  
        return <1>  
    }  
    return <n * callFunction <factorial> withArguments <n - 1>>  
}  

print <callFunction <factorial> withArguments <5>> toterminal#  

Output:
120  

'''