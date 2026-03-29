# Origin

Origin is an experimental interpreted programming language written in Python. The project currently includes a tokenizer, a token-based executor, a small runtime, custom language-level errors, and a CLI entrypoint.

## Current State

Implemented now:
- variable declarations with explicit types
- built-in types `int` and `str`
- `print`
- `type()`
- `scan()`
- `if ... start ... end;`
- `if ... start ... else ... end;`
- `for`
- expressions inside `{}`
- custom language errors instead of raw Python tracebacks in normal cases

Not fully implemented yet:
- full `bool` support
- full `float` support as a first-class type
- functions
- `while`
- AST-based parser/executor
- source positions for errors (line/column)

## Project Structure

- `main.py` — CLI entrypoint
- `core/parser.py` — tokenizer
- `core/executor.py` — instruction reader and executor
- `core/runtime.py` — runtime singleton
- `core/errors.py` — Origin error classes
- `commands/advanced.py` — built-in commands and control flow
- `variables/factory.py` — variable/value parsing and expression handling
- `memory/memory.py` — variable storage
- `language_syntax_overview.md` — extra syntax notes

## Run

```bash
python3 main.py file.ogn
```

If no file is passed, the interpreter prints:

```text
FileError: Потрібно передати шлях до файлу програми
```

## Language Syntax

### Variable Declaration

Every variable declaration must include an explicit type.

```origin
int x = 10;
str name = "Ihor";
```

Re-typing is allowed, but the type keyword must still be written explicitly.

```origin
int value = 10;
str value = "ten";
```

## Types

Currently stable:
- `int`
- `str`

Notes:
- `int` is currently used for numeric values in the interpreter
- `bool` and `float` appear in some places in the codebase, but they are not complete language features yet

## Print

`print` outputs values to the console.

```origin
print("Hello");
print(x);
print("Hello" \ name);
```

Rules:
- commas are not used in `print`
- spaces are written with `\`
- expressions can be embedded with `{}`

Examples:

```origin
int x = 5;
print({x + 5});
print("Result" \ {x * 2});
```

## Built-in Functions

### `type()`

Returns the variable type.

```origin
int x = 5;
str t = (type(x));
print(t);
```

### `scan()`

Reads user input.

```origin
int age = (scan(int));
str name = (scan(str));
```

If `scan(int)` receives a non-integer value, Origin raises a runtime error.

## If

### Basic `if`

```origin
int x = 5;

if x < 10 start
    print("small");
end;
```

### `if / else`

```origin
int x = 12;

if x < 10 start
    print("small");
else
    print("big");
end;
```

### Expression Conditions

```origin
int x = 5;

if {x + 2} == 7 start
    print("match");
else
    print("no match");
end;
```

### String Comparison

```origin
str name = "Ihor";

if name == "Ihor" start
    print("hello");
end;
```

### Nested `if`

```origin
int x = 5;

if x < 10 start
    if x == 5 start
        print("nested-true");
    else
        print("nested-false");
    end;
else
    print("outer-false");
end;
```

## For

`for` has four parts:
1. initialization
2. condition
3. update
4. body

Syntax:

```origin
for int i = 0, i < 10, int i = {i + 1},
    print(i);
end;
```

Example with nested `if`:

```origin
for int i = 0, i <= 11, int i = {i + 1},
    if i > 4 start
        print(i);
    end;
end;
```

Example with `if/else` inside `for`:

```origin
for int i = 0, i < 4, int i = {i + 1},
    if i == 2 start
        print("two");
    else
        print(i);
    end;
end;
```

## Expressions

Expressions are currently evaluated inside `{}`.

```origin
int x = 3;
int y = {x + 7};
print({y * 2});
```

This is also used in loop updates:

```origin
for int i = 0, i < 3, int i = {i + 1},
    print(i);
end;
```

## Error System

Origin now has its own error layer.

Current error types:
- `SyntaxError`
- `NameError`
- `TypeError`
- `RuntimeError`
- `FileError`
- `InternalError`

Examples:

```text
NameError: Змінна 'x' не існує
TypeError: Змінна 'x' має тип int
SyntaxError: Умова має бути у форматі left OP right
FileError: Файл 'file.ogn' не знайдено
```

`InternalError` is reserved for unexpected interpreter failures inside Python.

## Example Program

```origin
int total = 0;
str label = "sum:";

for int i = 1, i <= 5, int i = {i + 1},
    int total = {total + i};

    if total > 6 start
        print(label \ total \ "large");
    else
        print(label \ total \ "small");
    end;
end;

str total_type = (type(total));
print("type:" \ total_type);
```

## Known Limitations

- execution is still largely token-based, not AST-based
- parser errors do not yet include line and column
- some syntax is strict and low-level by design
- command parsing is still minimalistic
- there is no module system or function system yet

## Main.py Assessment

`main.py` is currently good enough for a small interpreter:
- it works as a real CLI entrypoint
- it reads source files safely
- it converts language errors into Origin-style messages
- it returns a non-zero exit code on failure

What can be improved later:
- print errors to `stderr`
- add CLI flags
- add a REPL mode
- add a `--no-timing` mode
- add debug/token dump modes

## Next Recommended Steps

1. Add line and column tracking to tokens and errors.
2. Stabilize `bool` and `float` as real language types.
3. Move from token-driven execution toward AST.
4. Add `while` and functions.
5. Add tests for syntax, runtime, and nested control flow.

## Version

Current documented state: `0.1`.
