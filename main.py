import sys
from interpreter import Interpreter


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file.jb>")
        return

    filename = sys.argv[1]

    try:
        with open(filename, "r", encoding="utf-8") as file:
            source = file.read()

        interpreter = Interpreter()
        result = interpreter.run(source)

        if result is not None:
            print(result)

    except FileNotFoundError:
        print(f"JB ERROR: File not found: {filename}")

    except Exception as error:
        print(f"JB ERROR: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()