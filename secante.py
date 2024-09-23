import sympy as sp
import pandas as pd

def secant(fun_str, x_a, x_b, steps=50, tol=1e-5):
    # Crear la función a partir de la cadena
    x = sp.symbols('x')
    fun = sp.sympify(fun_str)
    f = sp.lambdify(x, fun)

    # Verificar si el método de la secante es aplicable
    if f(x_a) * f(x_b) >= 0:
        print('El método de la secante no se puede aplicar')
        return None

    # Inicializar DataFrame para almacenar los resultados
    data = {
        'Iteración': [],
        'a': [],
        'b': [],
        'Raíz aproximada': [],
        'Error relativo': []
    }

    raiz_anterior = x_a
    for n in range(1, steps):
        # Cálculo de la secante
        x_n = x_a - (f(x_a) * (x_b - x_a)) / (f(x_b) - f(x_a))

        # Calcular error relativo
        error_relativo = abs((x_n - raiz_anterior) / x_n)
        raiz_anterior = x_n

        # Guardar datos en el DataFrame
        data['Iteración'].append(n)
        data['a'].append(x_a)
        data['b'].append(x_b)
        data['Raíz aproximada'].append(x_n)
        data['Error relativo'].append(error_relativo)

        # Condición de parada por tolerancia
        if error_relativo < tol:
            #Convergencia alcanzada
            break

        # Actualizar los valores de a y b
        if f(x_a) * f(x_n) < 0:
            x_b = x_n
        else:
            x_a = x_n

        iteraciones = n + 1

    # Convertir los datos en un DataFrame
    tabla = pd.DataFrame(data)
    tabla.set_index('Iteración', inplace=True)
    tabla.index.name = None #
    tabla_html = tabla.to_html(classes='data', header=True, index='Iteración')
    return x_n, error_relativo, iteraciones, tabla_html