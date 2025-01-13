def main():
    try:
        # Prompt the user for a filename
        filename = input("Enter the filename: ")
        
        # Open and read the file into a list of lines
        with open(filename, 'r') as file:
            lines = file.readlines()
        
        # Remove trailing newlines for cleaner output
        lines = [line.rstrip('\n') for line in lines]
        total_lines = len(lines)
        
        print(f"The file contains {total_lines} lines.")
        
        # Main loop for navigation
        while True:
            try:
                # Prompt the user for a line number
                line_number = int(input("Enter a line number (0 to quit): "))
                
                if line_number == 0:
                    print("Exiting program.")
                    break
                elif 1 <= line_number <= total_lines:
                    print(f"Line {line_number}: {lines[line_number - 1]}")
                else:
                    print(f"Invalid line number. Please enter a number between 1 and {total_lines}, or 0 to quit.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    except FileNotFoundError:
        print("File not found. Please check the filename and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
