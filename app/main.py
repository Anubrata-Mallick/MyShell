import sys
import os
import subprocess
from typing import Optional
import shlex

COMMANDS = ["echo", "exit", "type", "pwd", "cd"]
PATH = os.environ.get("PATH", "")

def locate_executable(command) -> Optional[str]:

    for directory in PATH.split(":"):
        file_path = os.path.join(directory, command)

        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return command

def handle_cd(command):
    # check if user want to go home
    if command.split(maxsplit=1)[1] == "~":
        home_directory = os.path.expanduser("~")
        os.chdir(home_directory)
    #check if the file path exists or not
    elif os.path.exists(command.split(maxsplit=1)[1]):
        os.chdir(command.split(maxsplit=1)[1]) # change the directory
    else:
        sys.stdout.write(f"cd: {command.split(maxsplit=1)[1]}: No such file or directory\n")

def handle_type(command):
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

def handle_echo(command):
    if command[len("echo ")] == "'":
        args = command[len("echo "):].replace("'", "")
        sys.stdout.write(args)
        print()
    else:
        args = command[ len("echo "): ].strip()
        sys.stdout.write(f"{' '.join(args.split())}\n")

def handle_cat(command):
    args = command.split(maxsplit=1)[1]
    file_paths = shlex.split(args)

    for file_path in file_paths:
        try: 
            with open(file_path, "r") as file:
                content = file.read()
                sys.stdout.write(f"{content}    ")
        except FileNotFoundError:
            sys.stdout.write(f"{file_path} Not Found \n")
        except PermissionError:
            sys.stdout.write(f"Permission denied for {file_path}\n")



def main():
        
    sys.stdout.write("$ ")
    sys.stdout.flush()

    command = input()
    match command :
        case command if command.startswith("type "):
            handle_type(command)
        case command if command.startswith("echo "):
            handle_echo(command)
        case "exit 0":
            exit(0)
        case "pwd":
            sys.stdout.write(f"{os.getcwd()}\n")
        case command if command.startswith("cd "):
            handle_cd(command)
        case command if command.startswith("cat "):
            handle_cat(command)
        case _:
            if executable := locate_executable(command.split(maxsplit=1)[0]):
                subprocess.run([executable, command.split(maxsplit=1)[1]])
            else:
                print(f"{command}: command not found")

    main()

if __name__ == "__main__":
    main()
