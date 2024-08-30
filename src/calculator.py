def calculate(a,b, operator):
    if operator == "/":
        return division(a,b)
    else: 
        raise ValueError(f"Operador no valido: {operator}")

def division(a,b):
    if b == 0:
        raise ValueError("No puedes dividir por 0")
    return a / b
