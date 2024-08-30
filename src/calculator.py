def calculate(a,b, operator):
    if operator == "*":
        return multiplicacion(a,b)
    elif operator == "/":
        return division(a,b)
    else: 
        raise ValueError(f"Operador no valido: {operator}")

def multiplicacion(a,b):
    return a * b

def division(a,b):
    if b == 0:
        raise ValueError("No puedes dividir por 0")
    return a / b