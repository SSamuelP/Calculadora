import numpy as np
import sympy as sp
from scipy import integrate

def integracion_trapecio_con_error(expr, a, b, n):
    """
    Calcula la integral de una expresión simbólica en el intervalo [a, b] usando el método del trapecio y estima el error.

    Args:
        expr: La expresión simbólica a integrar.
        a: Extremo izquierdo del intervalo.
        b: Extremo derecho del intervalo.
        n: Número de subintervalos.

    Returns:
        Una tupla (resultado, error) con la aproximación de la integral y una estimación del error.
    """
    # Convertir la expresión simbólica en una función numérica
    x = sp.Symbol('x')
    f = sp.lambdify(x, sp.parse_expr(expr), 'numpy')
    f_prime = sp.lambdify(x, sp.diff(sp.parse_expr(expr), x, 2), 'numpy')  # Segunda derivada

    # Generar los puntos de evaluación
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)

    # Calcular la integral usando el método del trapecio
    area = integrate.trapezoid(y, x=x)

    # Calcular la integral con el doble de subintervalos
    area2 = integrate.trapezoid(f(np.linspace(a, b, 2 * n + 1)))

    # Estimar el error usando extrapolación de Richardson
    error = (area2 - area) / 3

    # Estimar el error usando la fórmula del error de truncamiento
    M2 = np.max(np.abs(f_prime(x)))  # Estimación simple de la cota superior
    error_estimado = (1 / 12) * h ** 3 * M2 * (b - a)

    return area, error, error_estimado