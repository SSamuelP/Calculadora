from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import pandas as pd

def regla_falsa(f, a, b, tolerancia):

    x = Symbol("x")
    fa = f.subs(x, a)
    fb = f.subs(x, b)

    #optimización
    if fa * fb >= 0:
        return f"No hay raíz en el intervalo específicado", "No aplica", "No aplica", "No aplica", "No aplica" # Return an empty DataFrame here

    data = {'Iteración': [], 'a': [], 'b': [], "f(a)": [], "f(b)": [], 'Raíz (r)': [], "f(r)": [], 'Error Relativo': []}
    iteracion = 0
    raiz_anterior = None
    max_iter = 100
    while iteracion < max_iter:
        medio = (a * fb - b * fa) / (fb - fa)
        f_medio = f.subs(x, medio)


        if raiz_anterior is not None:
            error_relativo = abs((medio - raiz_anterior) / medio)
            data['Error Relativo'].append(error_relativo)
            if error_relativo < tolerancia:
                break
        
        data['Iteración'].append(iteracion+1)
        data['a'].append(a)
        data['b'].append(b)
        data['f(a)'].append(fa)
        data['f(b)'].append(fb)
        data['Raíz (r)'].append(medio)
        data['f(r)'].append(f_medio)

        if f_medio * fa < 0:
            b = medio
            fb = f_medio
        else:
            a = medio
            fa = f_medio
        raiz_anterior = medio
        iteracion += 1
    
    # Crear DataFrame y formatear
    tabla = pd.DataFrame(data)
    tabla.set_index('Iteración', inplace=True)
    tabla.index.name = None
    tabla_html = tabla.to_html(classes='data', header=True, index='Iteración')

    return medio, iteracion, error_relativo, tabla_html