import pandas as pd
import ttg
import boolean
import itertools
import re

VARIABLES_CONST: tuple[str] = ("x", "y", "z")
algebra = boolean.BooleanAlgebra()

# Inicializa variables globales
variables_tabla = []
evaluar = []

def simplificar_operacion(operacion):
    # Simplifica la expresión
    operacion = operacion.replace("and", "&").replace("or", "|").replace("not", "~")
    expresion = algebra.parse(operacion)
    resultado_simplificado = expresion.simplify()
    resultado_str = str(resultado_simplificado)
    resultado_simplificado = resultado_str.replace("&", " · ").replace("|", " + ")

    # Extrae las variables
    variables = sorted(set(str(expresion).replace('~', '').replace('&', '').replace('|', '').replace('(', '').replace(')', '').replace(' ', '').replace('·', '')))

    return resultado_simplificado, variables

def separar_casos_especificos(operacion):
    # Define los casos específicos que deben ser separados
    casos_especificos = ["xy", "xz", "yx", "yz", "zx", "zy"]

    # Usa regex para encontrar y reemplazar casos específicos con " and " en medio
    for caso in casos_especificos:
        operacion = re.sub(f"({caso})", lambda m: f"{m.group(0)[0]} and {m.group(0)[1]}", operacion)

    # Reemplaza "+" con "or"
    final = operacion.replace(" + ", " or ")
    
    return final

def caso_especifico(df):
    # Inicializa la máscara como una serie de True con el mismo tamaño que df para evitar errores de dimensionamiento
    mask = pd.Series([True] * len(df), index=df.index)

    for i in range(len(evaluar)):
        mask = mask & (df[variables_tabla[i]] == evaluar[i])

    mostrar = df[mask]
    return mostrar

def calculadora_booleana_especifica(cantidad_numeros, ecuacion):
    global variables_tabla, evaluar

    # Valor de inicio de variables
    for i in range(cantidad_numeros):
        variables_tabla.append(VARIABLES_CONST[i])
        estado_inicio = int(input(f"Ingrese el valor de evaluación de {VARIABLES_CONST[i]}: "))

        # Validador optimizado
        while estado_inicio not in [0, 1]:
            print("El valor ingresado no es válido. Ingrese un valor booleano (0 o 1).")
            estado_inicio = int(input(f"Ingrese el valor de evaluación de {VARIABLES_CONST[i]}: "))
        evaluar.append(estado_inicio)

# EJECUCIÓN
ecuacion = input("Ingrese la operación binaria: ")

# Simplificar la operación
resultado_simplificado, variables = simplificar_operacion(ecuacion)
print("Resultado simplificado:", resultado_simplificado)

# Separar casos específicos y realizar reemplazos
final = separar_casos_especificos(ecuacion)

# Crear la tabla de verdad
calcular = ttg.Truths(variables, [final])
df = calcular.as_pandas

print("\n Tabla de verdad ")
print(df)

print("\n Caso específico ")
calculadora_booleana_especifica(len(variables), final)
resultado_caso_especifico = caso_especifico(df)
resultado_caso_especifico