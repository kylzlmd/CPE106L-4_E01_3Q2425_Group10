def mean(numbers):
    """
    Computes the mean (average) of a list of numbers.
    Returns 0 if the list is empty.
    """
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def median(numbers):
    """
    Computes the median of a list of numbers.
    Returns 0 if the list is empty.
    """
    if not numbers:
        return 0
    numbers.sort()
    midpoint = len(numbers) // 2
    if len(numbers) % 2 == 1:
        return numbers[midpoint]
    else:
        return (numbers[midpoint - 1] + numbers[midpoint]) / 2

def mode(numbers):
    """
    Computes the mode of a list of numbers.
    Returns 0 if the list is empty.
    """
    if not numbers:
        return 0
    frequency = {}
    for number in numbers:
        frequency[number] = frequency.get(number, 0) + 1
    max_frequency = max(frequency.values())
    modes = [key for key, value in frequency.items() if value == max_frequency]
    # If there are multiple modes, return the smallest one
    return min(modes)

def read_numbers_from_file(file_name):
    """
    Reads a list of numbers from a text file.
    Assumes each line in the file contains numbers separated by spaces.
    """
    numbers = []
    try:
        with open(file_name, 'r') as file:
            for line in file:
                numbers.extend([float(num) for num in line.split()])
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except ValueError:
        print("Error: File contains non-numeric data.")
    return numbers

def main():
    """
    Tests the mean, median, and mode functions with numbers read from a file.
    """
    file_name = input("Enter the file name: ")
    numbers = read_numbers_from_file(file_name)
    if not numbers:
        print("No valid numbers to process.")
        return

    print("Numbers from file:", numbers)
    print(f"Mean: {mean(numbers):.3f}")
    print("Median:", median(numbers))
    print("Mode:", mode(numbers))

if __name__ == "__main__":
    main()