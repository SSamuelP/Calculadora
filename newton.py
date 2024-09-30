import sympy as sp
import pandas as pd

def newton_raphson(fun_str, x_0, steps=50, tol=1e-5):
    x = sp.symbols('x')
    fun = sp.sympify(fun_str)
    f = sp.lambdify(x, fun)
    f_prime = sp.lambdify(x, sp.diff(fun, x))

    data = {
        'Iteración': [],
        'Valor inicial': [],
        'Imagen Valor': [],
        'Raíz aproximada': [],
        'Error relativo': []
    }

    raiz_anterior = x_0
    for n in range(1, steps):
        # Método de Newton-Raphson
        x_n = x_0 - f(x_0) / f_prime(x_0)

        # Calcular error relativo
        error_relativo = abs((x_n - raiz_anterior) / x_n)
        raiz_anterior = x_n

        #Calculo de f(a)
        f_a = f(x_0)

        # Guardar datos en el DataFrame
        data['Iteración'].append(n)
        data['Valor inicial'].append(x_0)
        data['Imagen Valor'].append(f_a)
        data['Raíz aproximada'].append(x_n)
        data['Error relativo'].append(error_relativo)

        # Condición de parada por tolerancia
        if error_relativo < tol:
            iteraciones = n
            break

        # Actualizar el valor inicial
        x_0 = x_n


    tabla = pd.DataFrame(data)
    tabla.set_index('Iteración', inplace=True)
    tabla.index.name = None #Le quitamos el nombre a la columna de indices 
    tabla_html = tabla.to_html(classes='data', header=True, index=True)

    return x_n, error_relativo, iteraciones, tabla_html