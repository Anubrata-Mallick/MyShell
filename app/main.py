import sys


def main():
    # Create a REPL (Read-Execute-Print-Loop)
    while True :
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input
        command = input()

        # Print every command as invalid 
        print(f"{command}: command not found")

if __name__ == "__main__":
    main()
