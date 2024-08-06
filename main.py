import ttg
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Definimos constantes
VARIABLES_CONST: tuple[str] = ("p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

@app.route('/', methods=['GET', 'POST'])
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

if __name__ == '__main__':
    app.run(debug=True)

# Debido a que en la función Truths() se debe ingresar las variables que se van a usar, pedimos el número de variables que se usarán  
cantidad_vars: int = int(input("Con cuántas variables trabajará la operación:"))

# Para decirle al programa qué variables usaremos en la(s) operación iteramos en la lista que 
# tiene las variables constantes para agregarlas a la lista que usaremos en la función de la librería ttg
variables_usar: list[str] = []

for i in range(cantidad_vars):
  variables_usar.append(VARIABLES_CONST[i])


operacion: str = input("Ingrese la operación lógica a realizar: ")

def OperacionesLogicas(variables_tabla: list[str], ecuacion: str):
    operacion = ttg.Truths(variables_tabla, [ecuacion], ascending = True)
    return operacion

resultado = OperacionesLogicas(variables_usar, operacion)
resultado_df = resultado.as_pandas  # Se guarda como un dataframe de Pandas para iterar sobre los resultados
print(resultado_df)

# Para ser más específico en la entrega de resultados haremos uso de la función integrada de la librería ttg para decir si el resultado es una Tautología o una Contradicción
evaluacion: str = resultado.valuation()
print(f"El resultado de esta operación es una {evaluacion}")

# Prueba: Iteramos en el resultado de la operación así sabemos que en Flask, por medio de jinja, podremos mostrar el resultado de la operación 
for i in resultado_df[operacion]:
   print(i)