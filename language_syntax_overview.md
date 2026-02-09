Language Syntax Overview (Updated)

This document describes the basic syntax and core rules of the language, updated for the new rules.

⸻

1. Data Types

The language has two basic built-in types:
	•	int – represents all real numbers (integers and floating-point values).
	•	str – represents strings.

Variable Declaration

Variables are declared using the following syntax:

int x = 10;
str y = "10";

⚠️ The semicolon (;) is mandatory at the end of every statement.

Dynamic Re-typing

A variable can be reassigned with a different type, but the type keyword must always be explicitly written, even if the variable was already initialized before.

int x = 10;
str x = "hello";

Notice: Writing only x = "hello"; without str is not allowed in the new rules.

⸻

2. Printing Output

Basic Print

The print function outputs values to the console.

print(x \ "text");

Spacing Rules
	•	Commas are forbidden in print.
	•	To add spaces between printed values, use \ (backslash):

print(x \ "hello");   // one space between x and "hello"
print(x \ \ "hello"); // two spaces between x and "hello"


⸻

3. Expressions Inside Print

To evaluate expressions inside print, use curly braces {}.

print({x + 5});

The expression inside {} is calculated first, then printed.

You can mix expressions and strings with spaces via \:

print("Result" \ {x + 5});


⸻

4. Functions and Type Inspection

Getting Variable Type

The built-in function type() returns the type of a variable.

str state = (type(x));

The returned value is stored as a string.

⸻

5. Loops

For Loop

The for loop follows the syntax:

for int i = 0, i < 10, int i = {i + 1},
    print({i});
end;

	•	init (e.g., int i = 0) – always declare type explicitly
	•	condition (e.g., i < 10) – evaluated before each iteration
	•	step (e.g., int i = {i + 1}) – executed after each iteration
	•	Body statements can be multiple, separated by ,
	•	The loop ends with end;

You can also write a for loop on a single line:

for int i = 0, i < x, int i = {i + 1}, print({i}); end;


⸻

6. Important Rules (Short Version)
	•	Every statement must end with ;
	•	Variables must always declare type, even on reassignment
	•	int supports all real numbers
	•	{} inside print forces evaluation
	•	Spaces in print are controlled by \, commas are not allowed
	•	For loops require explicit init, condition, and step with type keywords

⸻

This syntax is intentionally minimal and flexible, designed for simplicity and fast rewriting of logic.