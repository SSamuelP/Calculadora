import numpy as np
import sympy as sp
from scipy import integrate
import random

def integracion_simpson_untercio_con_error(expr, a, b, n):
    """
    Calcula la integral de una expresión simbólica en el intervalo [a, b] usando el método de Simpson 1/3 y estima el error.

    Args:
        expr: La expresión simbólica a integrar.
        a: Extremo izquierdo del intervalo.
        b: Extremo derecho del intervalo.
        n: Número de subintervalos (debe ser par).

    Returns:
        Una tupla (resultado, error_estimado) con la aproximación de la integral y una estimación del error.
    """

    # Convertir la expresión simbólica en una función numérica
    x = sp.Symbol('x')
    f = sp.lambdify(x, sp.parse_expr(expr), 'numpy')
    f_cuarta = sp.lambdify(x, sp.diff(expr, x, 4), 'numpy')  # Cuarta derivada

    # Generar los puntos de evaluación
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = f(x)

    # Calcular la integral usando el método de Simpson 1/3
    area = integrate.cumulative_trapezoid(y, x, initial=0)[-1]

    # Estimar el error usando la fórmula del error de truncamiento de Simpson 1/3
    # Generamos un valor aleatorio para ξ dentro del intervalo [a, b]
    xi = a + random.random() * (b - a)
    M4 = np.abs(f_cuarta(xi))
    error_estimado = -(h**5 / 90) * M4

    return area, error_estimado