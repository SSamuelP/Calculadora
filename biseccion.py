from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import pandas as pd

def metodo_biseccion(f, a, b, tolerancia):
    #para que maneje compatibilidad con el evaluador
    x = Symbol("x")
    fa = f.subs(x,a)
    fb = f.subs(x,b)

    data = {'Iteración': [], 'a': [], 'b': [], 'Medio': [], 'Error Relativo': []}
    iteracion = 0
    raiz_anterior = None

    #no hay raíz en la función
    if fa * fb >= 0:
        return f"Los valores iniciales no tienen raíz.", "No aplica", "No aplica", "No aplica", "No aplica"

    # a mas iteraciones mas precisión pero se demora
    while (b - a)/2.0 > tolerancia or iteracion <= 100:
        medio = (a + b)/2.0
        f_medio = f.subs(x, medio)

        #para el error relativo
        if raiz_anterior is not None:
            error_relativo = abs((medio - raiz_anterior) / medio)
            if error_relativo < tolerancia:
                break
        else:
            error_relativo = 0

        data['Iteración'].append(iteracion+1)
        data['a'].append(a)
        data['b'].append(b)
        data['Medio'].append(medio)
        data['Error Relativo'].append(error_relativo)

        if f_medio * fa < 0:
            b = medio
        else:
            a = medio
        iteracion += 1
        raiz_anterior = medio

    tabla = pd.DataFrame(data)

    tabla.set_index('Iteración', inplace=True) #El índice representa cada iteración, por ello se reemplaza el índice por el número e iteración en especifico.
    tabla.index.name = None #Le quitamos el nombre a la columna de indices 
    tabla_html = tabla.to_html(classes='data', header=True, index='Iteración')

    return medio, iteracion, error_relativo, tabla_html
