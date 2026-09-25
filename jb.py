import sys
from interpreter import Interpreter


def main():
    interpreter = Interpreter()

    if len(sys.argv) > 1:
        filename = sys.argv[1]

        try:
            with open(filename, "r", encoding="utf-8") as file:
                source = file.read()

            interpreter.run(source)

        except FileNotFoundError:
            print(f"JB Error: file not found: {filename}")

        except Exception as error:
            print(f"JB Error: {error}")

        return

    print("JB Language V4")
    print("Type 'exit' to quit.")

    while True:
        try:
            source = input("JB> ")

            if source.strip() == "exit":
                break

            if not source.strip():
                continue

            interpreter.run(source)

        except Exception as error:
            print(f"JB Error: {error}")


if __name__ == "__main__":
    main()