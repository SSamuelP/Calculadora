import pandas as pd
import ttg

VARIABLES_CONST = ("p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")


def calculadora_logica_especifica(variables, ecuacion, valores_simbolos):
    calcular = ttg.Truths(variables, [ecuacion], ascending=True)
    df = calcular.as_pandas

    mask = pd.Series([True] * len(df), index=df.index)
    for i in range(len(valores_simbolos)):
        mask = mask & (df[variables[i]] == int(valores_simbolos[i]))

    mostrar = df[mask]
    tabla_html = mostrar.to_html(classes='data', header=True, index=False)

    return tabla_html