import sys
import os
import subprocess
from typing import Optional

COMMANDS = ["echo", "exit", "type", "pwd", "cd"]
PATH = os.environ.get("PATH", "")

def locate_executable(command) -> Optional[str]:

    for directory in PATH.split(":"):
        file_path = os.path.join(directory, command)

        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return command



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
        case "pwd":
            sys.stdout.write(f"{os.getcwd()}\n")
        case command if command.startswith("cd "):
            #check if the file path exists or not
            if os.path.exists(command.split(maxsplit=1)[1]):
                os.chdir(command.split(maxsplit=1)[1]) # change the directory
            else:
                sys.stdout.write(f"cd: /{command.split(maxsplit=1)[1]}: No such file or directory")
        case _:
            if executable := locate_executable(command.split(maxsplit=1)[0]):
                subprocess.run([executable, command.split(maxsplit=1)[1]])
            else:
                print(f"{command}: command not found")

    main()

if __name__ == "__main__":
    main()
