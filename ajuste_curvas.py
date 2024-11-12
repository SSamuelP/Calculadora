def format_polynomial_expression_latex(coeffs):
    """
    Formatea la ecuación del polinomio en formato LaTeX.

    Parámetros:
        coeffs (list): Coeficientes del polinomio en orden descendente de grados.

    Retorna:
        str: Representación del polinomio en formato LaTeX.
    """
    terms = []
    degree = len(coeffs) - 1

    for i, coeff in enumerate(coeffs):
        if coeff == 0:
            continue  # Ignorar términos con coeficiente cero

        exponent = degree - i
        term = ""

        # Agregar signo positivo si el coeficiente es positivo y no es el primer término
        if coeff > 0 and terms:
            term += "+ "

        # Agregar coeficiente y variable en formato adecuado
        if exponent == 0:
            term += f"{coeff:.4f}"
        elif exponent == 1:
            term += f"{coeff:.4f} x"
        else:
            term += f"{coeff:.4f} x^{exponent}"
        
        terms.append(term)

    return " ".join(terms)
