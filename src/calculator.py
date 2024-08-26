
def calculate(a,b, operator):
    if operator == "+":
        return suma(a,b)
    else: 
        raise ValueError(f"Operador no valido: {operator}")

def suma(a,b):
    return a + b
