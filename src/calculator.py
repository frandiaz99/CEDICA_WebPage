def calculate(a,b, operator):
    if operator == "/":
        return division(a,b)
    else: 
        raise ValueError(f"Operador no valido: {operator}")

def division(a,b):
    return a / b
