from src import calculator

def main():
    try:
        num1 = float(input("Enter first number: "))
    except ValueError:
        print("Invalid input! Please enter a valid number for the first input.")
        return

    try:
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid input! Please enter a valid number for the second input.")
        return

    operator = input("Enter operator: ")

    try:
        result = calculator.calculate(num1, num2, operator)
        print(f"Result: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
