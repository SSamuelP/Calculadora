import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvas
import sympy as sp

# Definir una función para convertir cadenas en funciones de sympy
def parse_function(func_str):
    x = sp.symbols('x')
    return sp.lambdify(x, sp.sympify(func_str), "numpy")

# Encontrar los puntos de intersección de las curvas
def intersection(x, f1, f2):
    return f1(x) - f2(x)

# Calcular las raíces (puntos de intersección)
def calculate_intersections(f1, f2, initial_guesses=[1, 5]):
    roots = fsolve(intersection, initial_guesses, args=(f1, f2))
    return roots

# Función para generar el sólido de revolución
def generate_3d_graph(func1_str, func2_str):
    # Parsear las funciones ingresadas por el usuario
    f1 = parse_function(func1_str)
    f2 = parse_function(func2_str)

    # Calcular los puntos de intersección
    roots = calculate_intersections(f1, f2)

    # Rango de valores de x
    x_vals = np.linspace(roots[0], roots[1], 500)
    
    # Rango de ángulos para la rotación
    theta_vals = np.linspace(0, 2 * np.pi, 200)

    # Función para generar el sólido de revolución
    def generate_revolution_surface(f, x_vals, theta_vals):
        X = np.outer(x_vals, np.ones_like(theta_vals))
        Y = np.outer(f(x_vals), np.cos(theta_vals))
        Z = np.outer(f(x_vals), np.sin(theta_vals))
        return X, Y, Z

    # Generar las superficies para las dos curvas
    X1, Y1, Z1 = generate_revolution_surface(f1, x_vals, theta_vals)
    X2, Y2, Z2 = generate_revolution_surface(f2, x_vals, theta_vals)

    # Crear la figura
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Graficar la superficie de revolución para ambas curvas
    ax.plot_surface(X1, Y1, Z1, color='blue', alpha=0.5, rstride=10, cstride=10)
    ax.plot_surface(X2, Y2, Z2, color='red', alpha=0.5, rstride=10, cstride=10)

    # Configuración del gráfico
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Sólido de revolución generado al girar el área')

    # Convertir la gráfica a imagen y codificarla en base64
    png_image = io.BytesIO()
    FigureCanvas(fig).print_png(png_image)
    png_image_b64 = "data:image/png;base64," + base64.b64encode(png_image.getvalue()).decode('utf8')
    
    return png_image_b64
