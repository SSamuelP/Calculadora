import numpy as np
import sympy as sy
from sympy.parsing.sympy_parser import parse_expr
from sympy import *

VARIABLES = ["x", "y", "z"]
variables_usadas = []

def validar_expresion(expresion):
    for letra in expresion:
        if (letra in VARIABLES) and (letra not in variables_usadas):
            variables_usadas.append(letra)

    if len(variables_usadas) > 0:
        return True
    else:
        raise ValueError("Error en la expresión, ingrese variables válidas")
    
def encontrar_trigonometricas(n):
    if n.find("sin") == -1 and n.find("cos") == -1 and n.find("tan") == -1 and n.find("asin") == -1 and n.find("acos") == -1 and n.find("atan") == -1:
      return False
    else:
      return True