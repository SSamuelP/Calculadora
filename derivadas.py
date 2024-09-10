from sympy.parsing.sympy_parser import parse_expr
import sympy as sy

def derivar_funcion(funcion, orden):
    lista_derivadas = []

    x = sy.Symbol("x")
    y = parse_expr(funcion, transformations="all")

    for i in range(1, orden + 1):
        
        yprime = y.diff(x, i)
        yprime_latex = sy.latex(yprime)
        lista_derivadas.append(yprime_latex)

    return lista_derivadas