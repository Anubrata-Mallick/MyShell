import sys
import os

COMMANDS = ["echo", "exit", "type"]
PATH = os.environ.get("PATH")

def main():
        
    sys.stdout.write("$ ")
    sys.stdout.flush()

    command = input()
    match command :
        case command if command.startswith("type "):

            cmd = command.split(maxsplit=1)[1]
            cmd_path = None
            paths = PATH.split(":")

            for path in paths:
                if os.path.isfile(f"{path}/{cmd}"):
                    cmd_path = f"{path}/{cmd}"

            if cmd in COMMANDS:
                sys.stdout.write(f"{cmd} is a shell builtin \n") 
            elif cmd_path:
                sys.stdout.write(f"{cmd} is {cmd_path}\n")
            else:
                sys.stdout.write(f"{cmd}: not found \n")

        case command if command.startswith("echo "):
            sys.stdout.write(f"{command[ len("echo "): ]}\n")
        case "exit 0":
            exit(0)
        case _:
            for path in PATH :
                if os.path.isfile(command.split(" ")[0]):
                    os.system(command)
                    main()   
            print(f"{command}: command not found")

    main()

if __name__ == "__main__":
    main()
