import sys

def main():
    # Create a REPL (Read-Execute-Print-Loop)
    while True :
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input ------ READ 
        command = input()
        #--------------------------- EXECUTE
        match command :
            case "exit 0":
                break
            case _ :
                print(f"{command}: command not found")

if __name__ == "__main__":
    main()
