import sys


def main():
    # Uncomment this block to pass the first stage
    sys.stdout.write("$ ")

    # Create a REPL (Read-Execute-Print-Loop)
    while True :
        # Wait for user input
        command = input()

        # Print every command as invalid 
        print(f"{command}: command not found")

if __name__ == "__main__":
    main()
