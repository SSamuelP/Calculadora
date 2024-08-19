import pandas as pd
import ttg

VARIABLES_CONST: tuple[str] = ("p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
variables_tabla = []
evaluar = []

def calculadora_logica_especifica(cantidad_numeros, ecuacion):
    for i in range(cantidad_numeros):
        variables_tabla.append(VARIABLES_CONST[i])
        estado_inicio = int(input(f"Ingrese el valor de evaluación de {VARIABLES_CONST[i]}: "))

        # Buscador optimizado
        while estado_inicio not in [0, 1]:
            print("El valor ingresado no es válido. Ingrese un valor booleano (0 o 1).")
            estado_inicio = int(input(f"Ingrese el valor de evaluación de {VARIABLES_CONST[i]}: "))
        evaluar.append(estado_inicio)

    calcular = ttg.Truths(variables_tabla, [ecuacion], ascending=True)
    df = calcular.as_pandas()

    # Inicializa la máscara como una serie de True con el mismo tamaño que df para evitar errores de dimensionamiento
    # SIN ESTO CRASHEA, NO BORRAR
    mask = pd.Series([True] * len(df), index=df.index)
    for i in range(len(evaluar)):
        mask = mask & (df[variables_tabla[i]] == evaluar[i])

    mostrar = df[mask]
    tabla_html = mostrar.to_html(classes='data', header=True, index=False)
    
    return tabla_html