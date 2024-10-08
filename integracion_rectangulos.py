import numpy as np
import sympy as sp

def integracion_rectangulos_sympy(expr, a, b, n):
  """
  Calcula la integral de una expresión simbólica en el intervalo [a, b] usando el método de los rectángulos.

  Args:
    expr: La expresión simbólica a integrar.
    a: Extremo izquierdo del intervalo.
    b: Extremo derecho del intervalo.
    n: Número de subintervalos.

  Returns:
    Una tupla con las aproximaciones de la integral por el punto derecho, izquierdo y medio.
  """
  x = sp.Symbol('x')
  f = sp.parse_expr(expr)

  # Convertir la expresión simbólica en una función numérica
  f = sp.lambdify(x, f, 'numpy')

  #la altura del rectangulo
  h = (b - a) / n

  #ancho sub intervalo
  x = np.linspace(a, b, n+1)

  #nodos (extremos subintervalo)
  xm = (x[:-1] + x[1:]) / 2

  #evaluar la función
  y = f(x)
  ym = f(xm)
  area_derecha = h * np.sum(y[1:])
  area_izquierda = h * np.sum(y[:-1])
  area_medio = h * np.sum(ym)

  return area_derecha, area_izquierda, area_medio