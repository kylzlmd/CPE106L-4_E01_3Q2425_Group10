def navigate_file_lines():
    try:
        # Prompt the user for the filename
        filename = input("Enter the filename: ")

        # Read lines from the file and store them in a list
        with open(filename, 'r') as file:
            lines = file.readlines()

        # Remove any trailing newlines from the lines
        lines = [line.strip() for line in lines]

        # Enter a loop to navigate the lines
        while True:
            print(f"The file contains {len(lines)} lines.")

            # Prompt the user for a line number
            try:
                line_number = int(input("Enter a line number (or 0 to quit): "))
            except ValueError:
                print("Please enter a valid number.")
                continue

            # Exit the loop if the user enters 0
            if line_number == 0:
                print("Exiting the program.")
                break

            # Check if the line number is valid
            if 1 <= line_number <= len(lines):
                print(f"Line {line_number}: {lines[line_number - 1]}")
            else:
                print(f"Invalid line number. Please enter a number between 1 and {len(lines)}.")
    except FileNotFoundError:
        print("File not found. Please check the filename and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the program
if __name__ == "__main__":
    navigate_file_lines()
