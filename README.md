# JB-Script

**JB-Script** is a programming language project I’m developing from scratch in Python.

The project started as an interpreter and has grown into a more complete programming-language environment, with support for variables, functions, control flow, arrays, objects, classes, and a web framework layer.

## Current Features

### Core Language

* Variables and reassignment
* Numbers, strings, booleans, arrays, objects, and null
* Arithmetic operators
* Comparison operators
* Logical operators
* `if / otherwise`
* `while` loops
* `for` loops
* `break`
* `continue`
* Functions
* Return statements
* Classes and objects
* Property access and assignment
* Error handling with `try / catch`
* `throw`
* Import support

### Built-in Features

* `say()`
* Type checking
* Range generation
* Array methods
* String methods
* Object/property operations

### Web Framework

JB-Script also includes a web framework layer for building web applications using the language.

The goal is to make it possible to write application logic using JB-Script instead of relying only on Python.

## Example

```jb
let x = 10

x = 20

say(x)
```

Output:

```text
20
```

### Functions

```jb
function add(a, b) {
    return a + b
}

say(add(10, 20))
```

Output:

```text
30
```

### Classes

```jb
class Person {
    name = "John"
}

let person = Person()

say(person.name)
```

## Project Structure

```text
JB/
├── lexer.py
├── parser.py
├── interpreter.py
├── main.py
├── test_all.jb
└── README.md
```

## Running JB-Script

Make sure Python is installed.

Run a JB-Script file with:

```bash
python main.py test_all.jb
```

Or run another `.jb` file:

```bash
python main.py your_file.jb
```

## Testing

The project includes `test_all.jb`, which is used to test the language features.

It currently covers areas such as:

* Variables
* Assignment
* Arithmetic
* Comparisons
* Logical operators
* Conditions
* Arrays
* Array methods
* Objects
* Strings
* Built-in functions
* Ranges
* Loops
* Functions
* Classes

Run:

```bash
python main.py test_all.jb
```

## Technology

* **Python**
* Custom lexer
* Custom parser
* Custom interpreter
* JB-Script runtime
* Web framework layer

## Development Status

JB-Script is currently under active development.

The language is functional, and I’m continuing to expand its syntax, runtime, standard features, and web capabilities.

## GitHub

**Repository:**
https://github.com/jiya1928/JB-Script

## Why I’m Building This

I wanted to understand what actually happens behind a programming language instead of only using existing languages.

Building JB-Script has given me hands-on experience with:

* Lexing
* Parsing
* ASTs
* Interpreters
* Runtime environments
* Functions and closures
* Object-oriented features
* Error handling
* Language design
* Web application architecture

This project is still evolving, and the current implementation is only one stage of the larger idea.
