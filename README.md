This is v1.0.0 of the interpreter. Go to branch kiwi for the latest release.

Updates & changes:
v1.0.0:
Introduced 10 new functions:
1. expr {value} {operation} {value} - can only use 2 values.
2. #v {variable name} - when you want to use a variable that has already been defined
3. @a {text} {text} {some more text} - outputs whatever comes after, does not allow variables
4. @d |name| = {value} - based from this variable, it creates a variable named 'name' and it has a value of '{value}'
5. @gl {string or #v {variable name}} - will return the length of anything
6. @type {data type or variable} - returns the type of a piece of data
7. @i |name| text and some more ~ - creates a variable called name, will output the text 'text and some more', the ~ ends the input
8. %aft% - similar to the @a function, it just allows variables by doing #i-{variable name} instead of #v; aft for after variable declaration
9. ..i - converts a number to an integer
10. bin, hex, den - with these, you can convert between base 10, 2 and 16 in the format [bin -> hex] 101110 {this converts the binary number 101110 into hexadecimal}
