# kiwi

How to run:
(assuming you already have python installed as this is an interpreter made from python)

In a terminal, run: python interp.py {your filename}

Current version: v1.0.2

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

v1.0.2:
Introduced 1 new function, removed 1, updated syntax and functions as well as bug fixes
1. expr now allows powers and can perform any calculation that an actual calculator could using ast
2. #v {variable name} has now changed to #v-varName
3. @a also allows variables inside along with other plain text, can also use expressions, but will not print any text after the expression if it is at the start
4. if there is just plain text after a @d, it will capture all the text
5. removed %aft% as it had no real use after @a could handle variables
6. fixed bugs with base conversions.
7. added new function called @randNum val1 val2 - generates a random number between val1 and val2. can be used in @a and @d functions
8. smaller file size due to removing unnecessary code
