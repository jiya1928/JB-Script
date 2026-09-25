# JB-Script

JB-Script is a programming language I’m building from scratch using Python.

The project started as an experiment to understand how programming languages work internally, and it has gradually grown into a working interpreter with its own syntax and features.

## Current Features

* Variables and assignment
* Arithmetic and comparison operators
* Logical operators
* `if / otherwise`
* `while` loops
* `for` loops
* `break` and `continue`
* Functions
* Arrays
* Array methods
* Objects
* String methods
* Built-in functions
* Range
* Classes and objects
* Error handling with `try / catch`
* `throw`
* Import support

## Example

```jb
let x = 10

x = 20

if x > 10 {
    say("x is greater than 10")
} otherwise {
    say("x is 10 or less")
}
```

## Running JB-Script

Clone the repository:

```bash
git clone https://github.com/jiya1928/JB-Script.git
cd JB-Script
```

Run a JB-Script file:

```bash
python main.py test_all.jb
```

Or run your own program:

```bash
python main.py program.jb
```

## Project Structure

```text
JB-Script/
│
├── lexer.py
├── parser.py
├── interpreter.py
├── main.py
├── test_all.jb
└── README.md
```

## Development Status

JB-Script is still being built.

The interpreter is already capable of executing a wide range of language features, but the project is actively evolving. I’m currently focusing on improving the language, fixing edge cases, expanding the class system, and making the interpreter more reliable.

This project is mainly a way for me to learn by building something from the ground up rather than only studying how programming languages work theoretically.

## Repository

GitHub: https://github.com/jiya1928/JB-Script

More features and improvements are coming as I continue building it.
