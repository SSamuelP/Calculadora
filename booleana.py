import boolean

algebra = boolean.BooleanAlgebra()

def simplificar_operacion(operacion):
  operacion = operacion.replace("and", "&").replace("or", "|").replace("not", "~")
  expresion = algebra.parse(operacion)
  resultado_simplificado = expresion.simplify()
  resultado_str = str(resultado_simplificado)
  resultado_simplificado = resultado_str.replace("&", " · ").replace("|", " + ")

  return resultado_simplificado
