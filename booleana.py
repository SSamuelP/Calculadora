import boolean
import re
import ttg
import pandas as pd

algebra = boolean.BooleanAlgebra()

def simplificar_operacion(operacion):
    # Reemplazo de operadores personalizados por los de boolean.py
    # Reemplazamos las negaciones de la forma A' a not A
    operacion = re.sub(r"(\w)'", r"not \1", operacion)
    operacion = operacion.replace("·", "&").replace("+", "|")

    # Parsear y simplificar la expresión usando boolean.py
    expresion = algebra.parse(operacion)
    resultado_simplificado = expresion.simplify()

    # Convertir el resultado simplificado de vuelta a los operadores personalizados
    resultado_str = str(resultado_simplificado)
    resultado_simplificado = resultado_str.replace("&", " · ").replace("|", " + ").replace("~", "'")

    bool_resultado = resultado_simplificado.replace("·", "and").replace("+", "or").replace("'", "not")

    lista_variables = []
    for letra in bool_resultado:
        if letra == "A" or letra == "B" or letra == "C":
            if letra in lista_variables:
                pass
            else:
              lista_variables.append(letra)


    tabla_bool = ttg.Truths(lista_variables, [bool_resultado])
    tabla_df = tabla_bool.as_pandas
    bool_html = tabla_df.to_html(classes='data', header=True, index=False)

    return bool_html, resultado_simplificado

