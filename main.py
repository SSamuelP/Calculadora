import boolean
from booleana import simplificar_operacion
from flask import Flask, render_template, request
from logica import calculadora_logica
from logica_especifica import calculadora_logica_especifica
from conversor_bases import convert_to_bases

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
        
        tabla_html, evaluacion = calculadora_logica(cantidad_vars, operacion)

        return render_template('calc_logica.html', 
                               tabla_html=tabla_html, 
                               evaluacion=evaluacion,
                               operacion=operacion)
    return render_template('calc_logica.html')

#Calculadora lógica casos especificos
@app.route('/calc_logica_esp', methods=['GET', 'POST'])
def calc_logica_casos():
    if request.method == 'POST':
        cantidad_vars = int(request.form['cantidad_vars'])
        operacion = request.form['operacion']
        tabla_html = calculadora_logica_especifica(cantidad_vars, operacion)

        return render_template('calc_logica_esp.html', 
                               tabla_html=tabla_html, 
                               operacion=operacion)
    return render_template('calc_logica_esp.html')

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

#Calculadora de bases
@app.route('/convert')
def converter():
    return render_template('complemento_convert.html')

@app.route('/convert', methods=['POST'])
def convert():
    number = request.form['number']
    result = convert_to_bases(number)
    return result

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port = 5000, debug=True)