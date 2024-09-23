import numpy as np
import sympy as sp

# Función para obtener coeficientes de una expresión
def obtener_coeficientes(polinomio_str):
    x = sp.symbols('x')
    polinomio = sp.sympify(polinomio_str)
    coeficientes = sp.Poly(polinomio, x).all_coeffs()

    # Sympy devuelve los coeficientes en orden descendente, por lo que invertimos el orden
    coeficientes = [float(c) for c in coeficientes][::-1]
    return coeficientes

# Función para calcular raíces de polinomios
def calcular_raices(polinomio_str):
    try:
        # Obtener los coeficientes de la expresión del polinomio
        coeficientes = obtener_coeficientes(polinomio_str)

        # Instanciar el polinomio con numpy
        polinomio = np.polynomial.polynomial.Polynomial(coeficientes)

        # Calcular las raíces
        raices = polinomio.roots()

        # Formatear las raíces
        raices_formateadas = []
        for raiz in raices:
            if raiz.imag == 0:
                raiz_formateada = f"x = {raiz.real:.5f}"
            else:
                raiz_formateada = f"x = {raiz:.5f}".replace("j", "i")
            raices_formateadas.append(raiz_formateada)
        
        return raices_formateadas
    except Exception as e:
        return [f"Error: {e}"]