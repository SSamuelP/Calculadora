import ttg

VARIABLES_CONST = ("p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
EVALUACION: dict[str] = {"Contingency": "Contingencia", "Tautology": "Tautología", "Contradiction": "Contradicción"}

def verificar_not(ecuacion):
  ecuacion.count("not")
  for i in range(ecuacion.count("not")):
    ubicacion_not = ecuacion.find("not")
    if ubicacion_not != -1:
        return ecuacion[ubicacion_not: ubicacion_not + 5]
    return None

def calculadora_logica(cant_variables, ecuacion):
    ecuacion = ecuacion.replace("∧", "and").replace("∨", "or").replace("¬", "not ")
    parte_ecuaciones = []

    variables_usar = [VARIABLES_CONST[i] for i in range(cant_variables)]

    ecuacion_separada = ecuacion.split(")")
    negaciones = list(map(verificar_not, ecuacion_separada))

    for negacion in negaciones:
        if negacion is not None:
            parte_ecuaciones.append(negacion)

    for elemento in ecuacion_separada:
        if elemento.strip():
            parte_ecuaciones.append(elemento)

    for index, operacion in enumerate(parte_ecuaciones):
        if "(" in operacion:
            ubicacion_parentesis = operacion.find("(")
            operacion = operacion[ubicacion_parentesis + 1:]
            parte_ecuaciones[index] = operacion

    if ecuacion not in parte_ecuaciones:
      parte_ecuaciones.append(ecuacion)
      
    resultado = ttg.Truths(variables_usar, parte_ecuaciones, ascending=True)
    resultado_df = resultado.as_pandas

    tabla_html = resultado_df.to_html(classes='data', header=True, index=False)
    evaluacion = resultado.valuation()
    evaluacion_es = EVALUACION[evaluacion]

    return tabla_html, evaluacion_es