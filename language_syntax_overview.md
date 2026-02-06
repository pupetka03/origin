# Language Syntax Overview

This document describes the basic syntax and core rules of the language.

---

## 1. Data Types

The language has two basic built-in types:

* `int` – represents **all real numbers** (integers and floating-point values).
* `str` – represents **strings**.

### Variable Declaration

Variables are declared using the following syntax:

```text
int x = 10;
str y = "10";
```

⚠️ The semicolon (`;`) is **mandatory** at the end of every statement.

### Dynamic Re-typing

A variable can be reassigned with a **different type**, but the **type keyword must always be explicitly written**, even if the variable was already initialized before.

````text
int x = 10;
str x = "hello";
```text
int x = 10;
x = "hello";
````

---

## 2. Printing Output

### Basic Print

The `print` function outputs values to the console.

```text
print(x, "text");
```

### Spacing Rules

* A **comma followed by one space** separates printed values
* Two commas mean **two spaces**, three commas → three spaces, etc.

```text
print(x, , "hello");   // one extra space
print(x, , , "hello"); // two extra spaces
```

---

## 3. Expressions Inside Print

To evaluate expressions inside `print`, use curly braces `{}`.

```text
print({x + 5});
```

The expression inside `{}` is calculated first, then printed.

You can mix expressions and strings:

```text
print("Result:", {x + 5});
```

---

## 4. Functions and Type Inspection

### Getting Variable Type

The built-in function `type()` returns the type of a variable.

```text
str state = (type(x));
```

The returned value is stored as a string.

---

## 5. Important Rules (Short Version)

* Every statement **must end with ****;**
* `int` supports all real numbers
* Variables can change type freely
* `{}` inside `print` forces evaluation
* Commas control spacing in output

---

This syntax is intentionally minimal and flexible, designed for simplicity and fast rewriting of logic.
