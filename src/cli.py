import sys
from .engine import Engine

def main():
    engine = Engine()
    args = sys.argv[1:]

    if not args:
        print("Usage: python -m src.cli <command> [args]")
        print("Commands: put, get, delete, compact")
        return

    command = args[0]

    if command == "put":
        if len(args) < 3:
            print("Usage: python -m src.cli put <key> <value>")
            return
        engine.put(args[1], args[2])
        print(f"OK")

    elif command == "get":
        if len(args) < 2:
            print("Usage: python -m src.cli get <key>")
            return
        value = engine.get(args[1])
        print(value if value is not None else "Not found")

    elif command == "delete":
        if len(args) < 2:
            print("Usage: python -m src.cli delete <key>")
            return
        engine.delete(args[1])
        print("Deleted")

    elif command == "compact":
        engine.compact()

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()