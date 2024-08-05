import ttg

# Definimos constantes
VARIABLES_CONST: tuple[str] = ("p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")


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