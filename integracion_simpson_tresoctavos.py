import numpy as np
import sympy as sp
from scipy import integrate
import random

def integracion_simpson_tresoctavos_con_error(expr, a, b, n):
    """
    Calcula la integral de una expresión simbólica en el intervalo [a, b] usando el método de Simpson 3/8 y estima el error.

    Args:
        expr: La expresión simbólica a integrar.
        a: Extremo izquierdo del intervalo.
        b: Extremo derecho del intervalo.
        n: Número de subintervalos (debe ser múltiplo de 3).

    Returns:
        Una tupla (resultado, error_estimado) con la aproximación de la integral y una estimación del error.
    """

    # Verificar que el número de subintervalos sea múltiplo de 3
    if n % 3 != 0:
        raise ValueError("El número de subintervalos debe ser múltiplo de 3 para el método de Simpson 3/8.")

    # Convertir la expresión simbólica en una función numérica
    x = sp.Symbol('x')
    f = sp.lambdify(x, sp.parse_expr(expr), 'numpy')
    f_cuarta = sp.lambdify(x, sp.diff(expr, x, 4), 'numpy')  # Cuarta derivada

    # Generar los puntos de evaluación
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = f(x)

    # Calcular la integral usando el método de Simpson 3/8
    area = integrate.simpson(y, x=x) #NO REMOVER EL X=X bugea la función en colab

    # Estimar el error usando la fórmula del error de truncamiento de Simpson 3/8
    # Generamos un valor aleatorio para ξ dentro del intervalo [a, b]
    xi = a + random.random() * (b - a)
    M4 = np.abs(f_cuarta(xi))
    error_estimado = -(3/80) * h**5 * M4

    return area, error_estimado