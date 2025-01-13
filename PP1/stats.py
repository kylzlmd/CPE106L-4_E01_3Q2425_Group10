def median(numbers):
    """
    Computes the median of a list of numbers.
    """
    if not numbers:
        raise ValueError("The list is empty.")
    
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
    else:
        return sorted_numbers[mid]

def mode(numbers):
    """
    Computes the mode of a list of numbers.
    """
    if not numbers:
        raise ValueError("The list is empty.")
    
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1
    
    max_frequency = max(frequency.values())
    modes = [num for num, freq in frequency.items() if freq == max_frequency]
    
    if len(modes) == 1:
        return modes[0]
    else:
        raise ValueError("The list has no unique mode.")

def mean(numbers):
    """
    Computes the mean (average) of a list of numbers.
    """
    if not numbers:
        raise ValueError("The list is empty.")
    
    return sum(numbers) / len(numbers)

def main():
    """
    Main program to prompt user for input and calculate statistics.
    """
    try:
        # Prompt user for input
        user_input = input("Enter a list of numbers separated by spaces: ")
        # Convert input to a list of numbers
        numbers = list(map(float, user_input.split()))
        
        if not numbers:
            raise ValueError("You must enter at least one number.")
        
        # Calculate and display results
        print(f"The Median is: {median(numbers)}")
        print(f"The Mode is: {mode(numbers)}")
        print(f"The Mean is: {mean(numbers)}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
