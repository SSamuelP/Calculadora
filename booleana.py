import boolean
import re
import ttg
import pandas as pd

algebra = boolean.BooleanAlgebra()

def simplificar_operacion(operacion):
    # Paso 1: Reemplazo de operadores personalizados por los de boolean.py
    # Reemplazar negaciones de la forma (A+B)' por not (A+B)
    operacion = re.sub(r"\(([^()]+)\)'", r"not (\1)", operacion)
    
    # Reemplazar negaciones de la forma A' por not A
    operacion = re.sub(r"(\w)'", r"not \1", operacion)

    # Reemplazo de otros operadores
    operacion = operacion.replace("·", "&").replace("+", "|")

    try:
        # Paso 2: Parsear la expresión usando boolean.py
        expresion = algebra.parse(operacion)

        # Simplificar la expresión si es posible
        resultado_simplificado = expresion.simplify()

        # Paso 3: Convertir el resultado simplificado de vuelta a los operadores personalizados
        resultado_str = str(resultado_simplificado)
        resultado_simplificado = resultado_str.replace("&", " · ").replace("|", " + ").replace("~", "not ")

    except Exception as e:
        # Si ocurre un error durante la simplificación, manejarlo y continuar
        resultado_simplificado = "No se pudo simplificar"

    # Paso 4: Generar la tabla de verdad
    bool_expr = resultado_simplificado.replace("·", "and").replace("+", "or").replace("'", "not ")

    # Limitar las variables solo a A, B, C, D
    lista_variables = sorted(set(re.findall(r'[ABCD]', operacion)))

    # Generar la tabla de verdad usando ttg
    tabla_bool = ttg.Truths(lista_variables, [bool_expr])
    tabla_df = tabla_bool.as_pandas

    bool_html = tabla_df.to_html(classes='data', header=True, index=False)

    return bool_html, resultado_simplificado

