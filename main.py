import ttg
from flask import Flask, render_template, request
import pandas as pd
import boolean
from booleana import simplificar_operacion

algebra = boolean.BooleanAlgebra()
app = Flask(__name__)

# Definimos constantes
VARIABLES_CONST: tuple[str] = ("p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

@app.route('/calculadora_logica', methods=['GET', 'POST'])
def index():
    # Verificamos si la solicitud es de tipo POST para procesar los datos enviados por el formulario
    if request.method == 'POST':
        # Obtenemos la cantidad de variables y la operación lógica del formulario
        cantidad_vars = int(request.form['cantidad_vars'])
        operacion = request.form['operacion']
        
        # Seleccionamos las variables a usar en base a la cantidad indicada
        variables_usar = [VARIABLES_CONST[i] for i in range(cantidad_vars)]
        
        # Creamos la tabla de verdad usando la librería ttg
        resultado = ttg.Truths(variables_usar, [operacion], ascending=True)
        resultado_df = resultado.as_pandas  # Convertimos el resultado a un DataFrame de Pandas
        
        # Evaluamos si la operación es una Tautología o una Contradicción
        evaluacion = resultado.valuation()
        
        # Convertimos el DataFrame a HTML para mostrarlo en la plantilla
        tabla_html = resultado_df.to_html(classes='data', header=True, index=False)
        
        # Renderizamos la plantilla con los datos calculados
        return render_template('index.html', 
                               tabla_html=tabla_html, 
                               evaluacion=evaluacion,
                               operacion=operacion)
    # Si no es una solicitud POST, simplemente renderizamos la plantilla sin datos
    return render_template('index.html')

@app.route("/calculadora_booleana", methods =["GET", "POST"])
def calc_booleana():
    if request.method == "POST":
      operacion_logica = str(request.form["operacion_logica"])
      resultado_simplificado = simplificar_operacion(operacion_logica)

      return render_template("calc_booleana.html", 
                            operacion_logica = operacion_logica, 
                            resultado_simplificado = resultado_simplificado)
    return render_template("calc_booleana.html")

if __name__ == '__main__':
    app.run(debug=True)