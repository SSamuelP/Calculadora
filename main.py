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
@app.route('/calculadora_logica_especifica', methods=['GET', 'POST'])
def calc_logica_esp():
    if request.method == 'POST':
        try:
            cant_vars = int(request.form['cant_vars'])
            variables_usar = [VARIABLES_CONST[i] for i in range(cant_vars)]
            operacion = request.form['operacion']
            evaluar = [
                int(request.form[f'valor_{i}']) for i in range(cant_vars)
            ]

            resultado = calculadora_logica_especifica(variables_usar,
                                                      operacion, evaluar)
            return render_template('calc_logica_esp.html',
                                   resultado=resultado,
                                   cant_vars=cant_vars)
        except Exception as e:
            return render_template('calc_logica_esp.html', error=str(e), cant_vars=0)

    return render_template('calc_logica_esp.html')

#Calculadora booleana
@app.route('/calculadora_booleana', methods=['GET', 'POST'])
def calc_booleana():
    if request.method == "POST":
        operacion_logica = str(request.form["operacion_logica"])
        tabla_booleana, resultado_simplificado = simplificar_operacion(operacion_logica)

        return render_template("calc_booleana.html", 
                               operacion_logica=operacion_logica, 
                               resultado_simplificado=resultado_simplificado,
                               tabla_booleana = tabla_booleana)
    return render_template("calc_booleana.html")

# Ruta para la calculadora lógica específica
@app.route('/calculadora_logica_especifica', methods=['GET', 'POST'])
def calc_logica_especifica():
    if request.method == 'POST':
        try:
            cant_vars = int(request.form['cant_vars'])
            variables_usar = [VARIABLES_CONST[i] for i in range(cant_vars)]
            operacion = request.form['operacion']
            evaluar = [
                int(request.form[f'valor_{i}']) for i in range(cant_vars)
            ]

            resultado = calculadora_logica_especifica(variables_usar,
                                                      operacion, evaluar)
            return render_template('calc_logica_esp.html',
                                   resultado=resultado,
                                   cant_vars=cant_vars)
        except Exception as e:
            return render_template('calc_logica_esp.html', error=str(e), cant_vars=0)

    return render_template('calc_logica_esp.html')

#Calculadora de bases
@app.route('/convert', methods=['GET', 'POST'])
def converter():
    if request.method == 'POST':
        number = request.form['number']
        result = convert_to_bases(number)
        return result  # Retornar directamente el resultado en formato JSON para ser usado por el front-end
    return render_template('convert.html')  # Renderizar solo un archivo HTML unificado

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port = 5000, debug=True)