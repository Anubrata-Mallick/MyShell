import sys
import os
import subprocess
from typing import Optional
import shlex

COMMANDS = ["echo", "exit", "type", "pwd", "cd"]
PATH = os.environ.get("PATH", "")

def print_to_shell(output:str)-> None:
    sys.stdout.write(output)

def locate_executable(command) -> Optional[str]:

    for directory in PATH.split(":"):
        file_path = os.path.join(directory, command)

        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return command

def handle_cd(command) -> None:
    # check if user want to go home
    if command.split(maxsplit=1)[1] == "~":
        home_directory = os.path.expanduser("~")
        os.chdir(home_directory)
    #check if the file path exists or not
    elif os.path.exists(command.split(maxsplit=1)[1]):
        os.chdir(command.split(maxsplit=1)[1]) # change the directory
    else:
        print_to_shell(f"cd: {command.split(maxsplit=1)[1]}: No such file or directory\n")

def handle_type(command)-> str :
    cmd = command.split(maxsplit=1)[1]
    cmd_path = None
    paths = PATH.split(":")

    for path in paths:
        if os.path.isfile(f"{path}/{cmd}"):
            cmd_path = f"{path}/{cmd}"

    output = ""
    if cmd in COMMANDS:
        output = f"{cmd} is a shell builtin \n"
    elif cmd_path:
        output = f"{cmd} is {cmd_path}\n"
    else:
        output = f"{cmd}: not found \n"
    return output 

def handle_echo(command)->str:
    m = shlex.split(command, posix=True)
    output = ' '.join(m[1:])
    return f"{output}\n"

def handle_cat(command, modify=False)->str:
    buffer = []
    if modify:
        file_paths = shlex.split(command, posix=True)[1:]
    else:
        # args = command.split(maxsplit=1)[1]
        # file_paths = shlex.split(args)
        file_paths = shlex.split(command)[1:]

    for file_path in file_paths:
        try: 
            with open(file_path, "r") as file:
                content = file.read()
                buffer.append(f"{content}")
        except FileNotFoundError:
            return f"cat: {file_path}: No such file or directory\n"
        except PermissionError:
            return f"Permission denied for {file_path}\n"
    output = " ".join(buffer)
    return f"{output}\n"

# def handle_ls(command)-> str:
#     output = ""
#     args = shlex.split(command, posix=True)
#     if len(args) == 1:
#         paths = '.'
#     else:
#         paths = args[1:]

#     item_box = []
#     for path in paths:
#         item = os.listdir(path)
#         item_box.append(item)
    
#     for item in item_box:
#         output = " ".join(item)
#     return f"{output}\n"

def handle_ls(command)->str:
    cmd_parts = shlex.split(command)
    result = subprocess.run(cmd_parts, capture_output=True, text=True, check=True)
    return result.stdout

def Shell_Engine(command)-> str:
    Engine_Output = ""

    match command :
        case command if " 1> " in command or " > " in command:
            Engine_Output = handle_redirect_output(command)
            
        case command if command.startswith("type "):
            Engine_Output = handle_type(command)

        case command if command.startswith("echo "):
            Engine_Output = handle_echo(command)

        case "exit 0":
            exit(0)

        case "pwd":
            Engine_Output = handle_pwd()

        case command if command.startswith("ls ") or command=="ls":
            Engine_Output = handle_ls(command)

        case command if command.startswith("cd "):
            handle_cd(command)

        case command if command.startswith("cat "):
            Engine_Output = handle_cat(command)

        case command if command.startswith("'") or command.startswith('"'):
            Engine_Output = handle_cat(command, modify=True)

        case _:
            if executable := locate_executable(command.split(maxsplit=1)[0]): # execute external executables
                subprocess.run([executable, command.split(maxsplit=1)[1]])
            else:
                Engine_Output = f"{command}: command not found\n"

    return Engine_Output

def handle_pwd()-> str:
    output = f"{os.getcwd()}\n"
    return output

# echo 'Hello James' 1> /tmp/foo/foo.md
def handle_redirect_output(command)->str:
    if "1>" in command:
        args = command.split(" 1> ")
    else:
        args = command.split(" > ")
    
    source, destination = args[0], args[1]
    
    source_output = Shell_Engine(source)

    if source_output.startswith("cat:"):
        return source_output

    # then store the output into a file specified
    with open(destination, "w") as file :
        file.write(source_output.rstrip("\n"))

    return ""


def main():
        
    sys.stdout.write("$ ")
    sys.stdout.flush()

    command = input()
    output = Shell_Engine(command)

    if output != "" :
        print_to_shell(output)

    main()

if __name__ == "__main__":
    main()
