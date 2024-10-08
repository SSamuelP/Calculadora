import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar

def integracion_montecarlo_contar_puntos(expr, a, b, N):
    """
    Calcula la integral de una expresión simbólica en el intervalo [a, b] usando el método de Monte Carlo
    y cuenta los puntos dentro de la región definida por la función.

    Args:
        expr: La expresión simbólica a integrar.
        a: Extremo izquierdo del intervalo.
        b: Extremo derecho del intervalo.
        N: Número de disparos aleatorios (puntos a generar).

    Returns:
        Una tupla (area, puntos_dentro), donde:
            area: La aproximación de la integral.
            puntos_dentro: El número de puntos dentro de la región definida por la función.
    """

    try:
        # Convertir la expresión simbólica en una función numérica
        x = sp.Symbol('x')
        f = sp.lambdify(x, sp.parse_expr(expr), 'numpy')

        # Encontrar el valor máximo de la función en el intervalo [a, b]
        def neg_f(x):
            return -f(x)

        #Minimización local de una variable
        res = minimize_scalar(neg_f, bounds=(a, b))
        max_y = -res.fun

        # Generar N puntos aleatorios dentro del rectángulo
        puntos_x = np.random.uniform(a, b, N)
        puntos_y = np.random.uniform(0, max_y, N)

        # Evaluar la función en los puntos x y contar los puntos dentro de la región
        valores_funcion = f(puntos_x)
        puntos_dentro = np.sum(puntos_y <= valores_funcion)

        # Calcular el área bajo la curva
        area = (puntos_dentro / N) * (b - a) * max_y

        return area, puntos_dentro

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return None, None