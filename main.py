import boolean
import numpy as np
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
from falsa_posicion import regla_falsa
from derivadas import derivar_funcion
from secante import secant
from newton import newton_raphson
from polinomios import calcular_raices
from integracion_rectangulos import integracion_rectangulos_sympy
from integracion_trapecios import integracion_trapecio_con_error
from integracion_simson_untercio import integracion_simpson_untercio_con_error
from integracion_simpson_tresoctavos import integracion_simpson_tresoctavos_con_error
from integracion_montecarlo import integracion_montecarlo_contar_puntos

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
    funcion = ""
    if request.method == 'POST':
        expresion = request.form['expresion']
        funcion = expresion #Se crea esta variable para que se pueda mostrar en la pagina una vez se haya enviado el formulario
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
                           resultado_grados=resultado_grados, error=error, variables=variables_usadas,
                           funcion = funcion)

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
    expresion = ""
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

#Método de falsa posición
@app.route("/falsa_posicion", methods=["GET", "POST"])
def falsa_posicion():
    resultado = None
    iteraciones = None
    error_relativo = None
    tabla_html = None
    expresion = ""

    if request.method == "POST":
        expresion = request.form['funcion']
        limite_a = float(request.form['lim_inferior'])  
        limite_b = float(request.form['lim_superior'])  
        tolerancia = float(request.form['tolerancia'])  

        # Convertir la expresión en una función simbólica
        expresion_simb = parse_expr(expresion)

        # Llamar al método de bisección con la expresión simbólica
        resultado, iteraciones, error_relativo, tabla_html = regla_falsa(expresion_simb, limite_a, limite_b, tolerancia)
    
    return render_template("falsa_regla.html",
                           expresion = expresion,
                           resultado=resultado,
                           iteraciones=iteraciones,
                           error_relativo=error_relativo,
                           tabla_html=tabla_html)

#Calculadora de derivadas
@app.route("/derivadas", methods=["GET", "POST"])
def derivadas():
    derivadas = None
    funcion = ""
    if request.method == "POST":
        funcion = request.form['funcion']
        orden = int(request.form['orden'])

        derivadas = derivar_funcion(funcion, orden)

    return render_template("calculadora_derivadas.html", derivadas=derivadas, funcion=funcion)

# Método de la Secante
@app.route('/metodo_secante', methods=['GET', 'POST'])
def met_secante():
    fig_html = None
    secante_result = None
    funcion = ""

    if request.method == 'POST':
        if 'graficar' in request.form:
            # Graficar la función
            funcion = request.form['funcion']
            fig_html = graficar_2d(funcion)
        
        if 'calcular_secante' in request.form:
            # Obtener datos para el método de la secante
            funcion = request.form['funcion']
            a = float(request.form['a'])
            b = float(request.form['b'])
            tol = float(request.form['tol'])

            # Volver a graficar la función si ya se ingresó
            fig_html = graficar_2d(funcion)

            # Llamar al método de la secante
            raiz, error_relativo, iteraciones, tabla_html = secant(funcion, a, b, tol=tol)
            secante_result = {
                'raiz': raiz,
                'error_relativo': error_relativo,
                'iteraciones': iteraciones,
                'tabla': tabla_html
            }

    # Renderizar la página principal
    return render_template('secante.html', fig_html=fig_html, secante_result=secante_result, funcion=funcion)

# Método de Newton-Raphson
@app.route('/newton', methods=['GET', 'POST'])
def newton():
    fig_html = None
    newton_result = None
    funcion = ""
    if request.method == 'POST':
        if 'graficar' in request.form:
            # Graficar la función
            funcion = request.form['funcion']
            fig_html = graficar_2d(funcion)
        
        if 'calcular_newton' in request.form:
            # Obtener datos para el método de Newton-Raphson
            funcion = request.form['funcion']
            x_0 = float(request.form['x_0'])
            tol = float(request.form['tol'])

            # Volver a graficar la función si ya se ingresó
            fig_html = graficar_2d(funcion)

            # Llamar al método de Newton-Raphson
            raiz, error_relativo, iteraciones, tabla_html = newton_raphson(funcion, x_0, tol=tol)
            newton_result = {
                'raiz': raiz,
                'error_relativo': error_relativo,
                'iteraciones': iteraciones,
                'tabla': tabla_html
            }

    return render_template('newton.html', fig_html=fig_html, newton_result=newton_result, funcion=funcion)

# Método para hallar las raíces en los polinomios
@app.route('/polinomio', methods=['GET', 'POST'])
def polinomio():
    raices = None
    polinomio_str = ""
    if request.method == 'POST':
        # Obtener el polinomio desde el formulario
        polinomio_str = request.form['polinomio']
        
        # Calcular las raíces
        raices = calcular_raices(polinomio_str)

    return render_template('polinomio.html', raices=raices, polinomio_str = polinomio_str)

# Ruta para integración por rectángulos
@app.route("/integracion_rectangulos", methods=["GET", "POST"])
def integracion_rectangulos():
    resultado_derecha = None
    resultado_izquierda = None
    resultado_medio = None

    if request.method == "POST":
        funcion = request.form['funcion']
        limite_inferior = float(request.form['lim_inferior'])
        limite_superior = float(request.form['lim_superior'])
        particiones = int(request.form['particiones'])

        # Llamar a la función de integración
        resultado_derecha, resultado_izquierda, resultado_medio = integracion_rectangulos_sympy(
            funcion, limite_inferior, limite_superior, particiones)

    return render_template("integracion_rectangulos.html",
                           resultado_derecha=resultado_derecha,
                           resultado_izquierda=resultado_izquierda,
                           resultado_medio=resultado_medio)

# Ruta para integración por trapecios
@app.route("/integracion_trapecios", methods=["GET", "POST"])
def integracion_trapecios():
    resultado = None
    error_richardson = None
    error_truncamiento = None

    if request.method == "POST":
        funcion = request.form['funcion']
        limite_inferior = float(request.form['lim_inferior'])
        limite_superior = float(request.form['lim_superior'])
        particiones = int(request.form['particiones'])

        # Llamar a la función de integración
        resultado, error_richardson, error_truncamiento = integracion_trapecio_con_error(
            funcion, limite_inferior, limite_superior, particiones)

    return render_template("integracion_trapecios.html",
                           resultado=resultado,
                           error_richardson=error_richardson,
                           error_truncamiento=error_truncamiento)

# Ruta para integración de Simpson 1/3
@app.route("/integracion_simpson_untercio", methods=["GET", "POST"])
def integracion_simpson_untercio():
    resultado = None
    error_estimado = None

    if request.method == "POST":
        funcion = request.form['funcion']
        limite_inferior = float(request.form['lim_inferior'])
        limite_superior = float(request.form['lim_superior'])
        particiones = int(request.form['particiones'])

        # Verificar que el número de particiones sea par
        if particiones % 2 != 0:
            error_estimado = "El número de particiones debe ser par para el método de Simpson."
        else:
            # Llamar a la función de integración de Simpson
            resultado, error_estimado = integracion_simpson_untercio_con_error(
                funcion, limite_inferior, limite_superior, particiones)

    return render_template("integracion_simpson_untercio.html",
                           resultado=resultado,
                           error_estimado=error_estimado)

# Ruta para integración de Simpson 3/8
@app.route("/integracion_simpson_tresoctavos", methods=["GET", "POST"])
def integracion_simpson_tresoctavos():
    resultado = None
    error_estimado = None
    error_msg = None

    if request.method == "POST":
        try:
            funcion = request.form['funcion']
            limite_inferior = float(request.form['lim_inferior'])
            limite_superior = float(request.form['lim_superior'])
            particiones = int(request.form['particiones'])

            # Llamar a la función de integración de Simpson 3/8
            resultado, error_estimado = integracion_simpson_tresoctavos_con_error(
                funcion, limite_inferior, limite_superior, particiones)
        except ValueError as e:
            error_msg = str(e)

    return render_template("integracion_simpson_tresoctavos.html",
                           resultado=resultado,
                           error_estimado=error_estimado,
                           error_msg=error_msg)

# Ruta para integración por Monte Carlo
@app.route("/integracion_montecarlo", methods=["GET", "POST"])
def integracion_montecarlo():
    resultado = None
    puntos_dentro = None
    error_msg = None

    if request.method == "POST":
        try:
            funcion = request.form['funcion']
            limite_inferior = float(request.form['lim_inferior'])
            limite_superior = float(request.form['lim_superior'])
            num_puntos = int(request.form['num_puntos'])

            # Llamar a la función de integración de Monte Carlo
            resultado, puntos_dentro = integracion_montecarlo_contar_puntos(
                funcion, limite_inferior, limite_superior, num_puntos)
        except ValueError as e:
            error_msg = str(e)

    return render_template("integracion_montecarlo.html",
                           resultado=resultado,
                           puntos_dentro=puntos_dentro,
                           error_msg=error_msg)

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port = 5000, debug=True)