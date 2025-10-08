def add_numbers(*args):
    if not args:
        print("No numbers provided.")
        return 0
    try:
        total = sum(float(num) for num in args)
        return total
    except ValueError:
        print("Invalid input! Please provide numbers only.")
        return None

# Example usage:
result = add_numbers(2, 5, 6, 77)
print(result)  # Output: should display the sum
