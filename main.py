from src import calculator

def main():
    num1= float(input("Enter first number: "))
    num2= float(input("Enter second number: "))
    operator= input("Enter operator: ")
    result= calculator.calculate(num1, num2, operator)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
    