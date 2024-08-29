import ttg

EVALUACION: dict[str] = {"Contingency": "Contingencia", "Tautology": "Tautología", "Contradiction": "Contradicción"}

def verificar_not(ecuacion):
  ecuacion.count("not")
  for i in range(ecuacion.count("not")):
    ubicacion_not = ecuacion.find("not")
    if ubicacion_not != -1:
        return ecuacion[ubicacion_not:] #Dada que la ecuación que es enviada acá está separada por l
    return None

def calculadora_logica(ecuacion):
    ecuacion = ecuacion.replace("∧", "and").replace("∨", "or").replace("¬", "not ")
    parte_ecuaciones = []

    lista_variables = []
    for letra in ecuacion:
        if letra == "P" or letra == "Q" or letra == "R" or letra == "S" or letra == "T" or letra == "U" or letra == "V" or letra == "W" or letra == "X" or letra == "Y" or letra == "Z":
            if letra in lista_variables:
                pass
            else:
              lista_variables.append(letra) 

    ecuacion_separada = ecuacion.split(")")
    negaciones = list(map(verificar_not, ecuacion_separada))

    for negacion in negaciones:
        if negacion is not None:
            parte_ecuaciones.append(negacion)

    for elemento in ecuacion_separada:
        if elemento.strip():
          if elemento[0] == " ":
            pass
          else:
            parte_ecuaciones.append(elemento)

    for index, operacion in enumerate(parte_ecuaciones):
        if "(" in operacion:
            ubicacion_parentesis = operacion.find("(")
            operacion = operacion[ubicacion_parentesis + 1:]
            parte_ecuaciones[index] = operacion

    if ecuacion not in parte_ecuaciones:
      parte_ecuaciones.append(ecuacion)
      
    resultado = ttg.Truths(lista_variables, parte_ecuaciones, ascending=True, ints= False)
    evaluacion = resultado.valuation()
    resultado_df = resultado.as_pandas
    resultado_df.replace({True: "V", False: "F"}, inplace=True)

    #Por errores de las funciones e iteraciones anteriores pueden haber columnas repetidas, por eso las borramos
    resultado_df = resultado_df.loc[:, ~resultado_df.columns.duplicated()]
   
    tabla_html = resultado_df.to_html(classes='data', header=True, index=False)
    evaluacion_es = EVALUACION[evaluacion]

    return tabla_html, evaluacion_es