import boolean
import numpy as np
import sympy as sy
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from booleana import simplificar_operacion
from flask import Flask, render_template, request
from logica import calculadora_logica
from logica_especifica import calculadora_logica_especifica
from conversor_bases import convert_to_bases
from graficadora import graficar_2d
from evaluador_expresiones import validar_expresion, encontrar_trigonometricas, variables_usadas
from biseccion import metodo_biseccion

algebra = boolean.BooleanAlgebra()
app = Flask(__name__)

# Definimos constantes
VARIABLES_CONST: tuple[str] = ("P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")

#Menú principal
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

#Calculadora lógica
@app.route('/calculadora_logica', methods=['GET', 'POST'])
def calc_logica():
    if request.method == 'POST':
        operacion = request.form['operacion']
        
        tabla_html, evaluacion = calculadora_logica(operacion)

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
        tabla_booleana, resultado_simplificado = simplificar_operacion(operacion_logica)

        return render_template("calc_booleana.html", 
                               operacion_logica=operacion_logica, 
                               resultado_simplificado=resultado_simplificado,
                               tabla_booleana = tabla_booleana)
    return render_template("calc_booleana.html")

#Calculadora lógica casos especificos
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

            resultado, resultado_completo = calculadora_logica_especifica(variables_usar,
                                                      operacion, evaluar)
            return render_template('calc_logica_esp.html',
                                   resultado=resultado,
                                   resultado_completo = resultado_completo,
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

#Evaluador de expresiones
@app.route('/evaluador_expresiones', methods =["GET", "POST"])
def evaluador():
    resultado_radianes = None
    resultado_grados = None
    error = None
    if request.method == 'POST':
        expresion = request.form['expresion']
        hay_trigonometricas = encontrar_trigonometricas(expresion)
        
        variables_usadas.clear()  # Limpia las variables usadas en cada nuevo envío
        continuidad_operacion = validar_expresion(expresion)
        expresion = parse_expr(expresion, transformations="all")

        for variable in variables_usadas:
            valor = float(request.form[variable])  # Convertir el valor a float
            expresion = expresion.subs(variable, valor)

        resultado_radianes = expresion.evalf(12)  # Resultado en radianes

        if hay_trigonometricas == True:
            resultado_grados = np.degrees(float(resultado_radianes))  # Conversión a grados
        
        else:
            resultado_grados = "No aplica."

    return render_template('evaluador_expresiones.html', resultado_radianes=resultado_radianes, 
                           resultado_grados=resultado_grados, error=error, variables=variables_usadas)

#Graficadora
@app.route("/graficadora", methods=["GET", "POST"])
def graficadora():
    fig = None
    funcion = ""
    error = None

    if request.method == "POST":
        funcion = request.form.get('funcion', '')
        if funcion:
            fig = graficar_2d(funcion)

    return render_template("graficadora.html", funcion=funcion, fig=fig, error=error)

#Metodo de bisección
@app.route("/biseccion", methods=["GET", "POST"])
def biseccion():
    resultado = None
    iteraciones = None
    error_relativo = None
    tabla_html = None

    if request.method == "POST":
        expresion = request.form['funcion']
        limite_a = float(request.form['lim_inferior'])  # Convertir a float
        limite_b = float(request.form['lim_superior'])  # Convertir a float
        tolerancia = float(request.form['tolerancia'])  # Convertir a float

        # Convertir la expresión en una función simbólica
        expresion_simb = parse_expr(expresion)

        # Llamar al método de bisección con la expresión simbólica
        resultado, iteraciones, error_relativo, tabla_html = metodo_biseccion(expresion_simb, limite_a, limite_b, tolerancia)
    
    return render_template("metodo_biseccion.html",
                           expresion = expresion,
                           resultado=resultado,
                           iteraciones=iteraciones,
                           error_relativo=error_relativo,
                           tabla_html=tabla_html)



if __name__ == '__main__':
    app.run(host= "0.0.0.0", port = 5000, debug=True)