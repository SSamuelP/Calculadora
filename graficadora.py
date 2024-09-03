import sympy as sy
import numpy as np
import plotly.graph_objects as go

def graficar_2d(expresion):
    try:
        # Define la variable simbólica x
        x = sy.symbols('x')
        y = sy.sympify(expresion)

        # Transforma la expresión en una función lambda
        f = sy.lambdify(x, y)

        # Crea un vector numpy desde -5000 a 5000 con paso de 0.1
        x_values = np.arange(-5000, 5000, 0.1)
        y_values = [f(val) for val in x_values]

        # Crea la gráfica
        fig = go.Figure(data=[go.Scatter(x=x_values, y=y_values, mode='lines', name='y=f(x)')])

        # Configura la gráfica
        fig.update_layout(
            title=f"Gráfico de {expresion}",
            xaxis_title="x",
            yaxis_title="y",
            xaxis_range=[-5, 5],
            yaxis_range=[-5, 5],
            template="plotly_dark"
        )

        # Convertir la gráfica en HTML
        fig_html = fig.to_html(full_html=False, include_mathjax="cdn",  default_width = "1500px", default_height = "500px")
        return fig_html

    except Exception as e:
        return f"Error al graficar: {e}"