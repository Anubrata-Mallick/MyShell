import sys

def main():
    # Create a REPL (Read-Execute-Print-Loop)
    while True :
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input ------ READ 
        command = input()
        #--------------------------- EXECUTE
        if command == "exit 0":
            break
        elif command.split(maxsplit=1)[0] == "echo" :
            print(command.split(maxsplit=1)[1])
        else:
            print(f"{command}: command not found")

if __name__ == "__main__":
    main()
