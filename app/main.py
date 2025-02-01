import sys
import config
COMMANDS = ["echo", "exit"]

def main():
        
    sys.stdout.write("$ ")
    sys.stdout.flush()

    command = input()
    match command :
        case command if command.startswith("type "):
            keyword = command.split(maxsplit=1)[1]
            if keyword in COMMANDS:
                sys.stdout.write(f"{keyword} is a shell builtin \n")
            else:
                sys.stdout.write(f"{keyword}: not found \n")
        case command if command.startswith("echo "):
            sys.stdout.write(f"{command[ len("echo "): ]}\n")
        case "exit 0":
            exit(0)
        case _:
            print(f"{command}: command not found")

    main()

if __name__ == "__main__":
    main()
