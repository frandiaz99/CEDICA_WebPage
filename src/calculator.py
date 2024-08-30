def calculate(a,b, operator):
    if operator == "*":
        return multiplicacion(a,b)
    else: 
        raise ValueError(f"Operador no valido: {operator}")

def multiplicacion(a,b):
    return a * b
