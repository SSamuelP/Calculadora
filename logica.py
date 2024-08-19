import ttg

VARIABLES_CONST: tuple[str] = ("p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
EVALUACION: dict[str] = {"Contingency": "Contingencia", "Tautology": "Tautología", "Contradiction": "Contradicción"}


def calculadora_logica(cant_variables, ecuacion):
  
  variables_usar = [VARIABLES_CONST[i] for i in range(cant_variables)]
  
  resultado = ttg.Truths(variables_usar, [ecuacion], ascending = True)
  resultado_df = resultado.as_pandas
  tabla_html = resultado_df.to_html(classes = 'data', header = True, index = False)
  
  evaluacion = resultado.valuation()
  evaluacion_es = EVALUACION[evaluacion]

  return tabla_html, evaluacion_es