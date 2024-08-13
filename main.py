import ttg
from flask import Flask, render_template, request
import pandas as pd
import boolean
from booleana import simplificar_operacion

algebra = boolean.BooleanAlgebra()
app = Flask(__name__)

# Definimos constantes
VARIABLES_CONST: tuple[str] = ("p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

#Menú principal
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#Calculadora lógica
@app.route('/calculadora_logica', methods=['GET', 'POST'])
def calc_logica():
    if request.method == 'POST':
        cantidad_vars = int(request.form['cantidad_vars'])
        operacion = request.form['operacion']
        
        variables_usar = [VARIABLES_CONST[i] for i in range(cantidad_vars)]
        
        resultado = ttg.Truths(variables_usar, [operacion], ascending=True)
        resultado_df = resultado.as_pandas
        
        evaluacion = resultado.valuation()
        
        tabla_html = resultado_df.to_html(classes='data', header=True, index=False)
        
        return render_template('calc_logica.html', 
                               tabla_html=tabla_html, 
                               evaluacion=evaluacion,
                               operacion=operacion)
    return render_template('calc_logica.html')

#Calculadora booleana
@app.route('/calculadora_booleana', methods=['GET', 'POST'])
def calc_booleana():
    if request.method == "POST":
        operacion_logica = str(request.form["operacion_logica"])
        resultado_simplificado = simplificar_operacion(operacion_logica)

        return render_template("calc_booleana.html", 
                               operacion_logica=operacion_logica, 
                               resultado_simplificado=resultado_simplificado)
    return render_template("calc_booleana.html")

if __name__ == '__main__':
    app.run(debug=True)
