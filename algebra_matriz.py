import numpy as np
from scipy.linalg import lu

matrices = {} #Almacenamiento de las matrices

#El determinante
def Det(matriz):
    return np.linalg.det(matriz)

#La traspuesta
def Trasp(matriz):
    return np.matrix.transpose(np.array(matriz))

#La inversa
def Inv(matriz):
    try:
        return np.linalg.inv(matriz)
    except np.linalg.LinAlgError:
        return "No invertible"

#La diagonal
def Diag(matriz):
    matriz = np.array(matriz)
    # Check if matriz is 2D
    if matriz.ndim != 2:
        return "Error: Input must be a 2D matrix."
    return np.diag(matriz)  # Return diagonal elements as a 1D array


#Factorización LU
def LU(matriz):
    matriz = np.array(matriz)
    # Asegurar que sea cuadrada la matriz
    if matriz.shape[0] != matriz.shape[1]:
        return "La descomposición LU requiere una matriz cuadrada."

    try:
        P, L, U = lu(matriz)
        # Format each component in LaTeX for rendering
        P_latex = formatear_matriz_latex(P)
        L_latex = formatear_matriz_latex(L)
        U_latex = formatear_matriz_latex(U)
        return f"P: {P_latex}, L: {L_latex}, U: {U_latex}"
    except Exception as e:
        return f"Error in LU decomposition: {str(e)}"

#Potenciación
def Pot(matriz, potencia):
    return np.linalg.matrix_power(matriz, potencia)

#Gauss Jordan
def GaussJordan(matriz_aumentada):
    matriz_aumentada = np.array(matriz_aumentada)
    matriz_aumentada = matriz_aumentada.astype(np.float64)
    filas, columnas = matriz_aumentada.shape

    for j in range(min(filas, columnas - 1)):
        pivote_fila = np.argmax(np.abs(matriz_aumentada[j:, j])) + j
        if pivote_fila != j:
            matriz_aumentada[[j, pivote_fila], :] = matriz_aumentada[[pivote_fila, j], :]

        pivote = matriz_aumentada[j, j]
        if pivote != 0:
            matriz_aumentada[j, :] /= pivote

        for i in range(filas):
            if i != j:
                factor = matriz_aumentada[i, j]
                matriz_aumentada[i, :] -= factor * matriz_aumentada[j, :]

    return matriz_aumentada

# Se actualiza el metodo para que devuelva el resultado en formato LaTeX y debugee el error cuando trabaja con Numpy
def formatear_matriz_latex(a):
    """Returns a LaTeX bmatrix

    :a: numpy array
    :returns: LaTeX bmatrix as a string
    """
    if len(a.shape) > 2:
        raise ValueError('bmatrix solo puede mostrar 2 dimensiones')
    lines = str(a).replace('[', '').replace(']', '').splitlines()
    rv = [r'\begin{bmatrix}']
    rv += ['  ' + ' & '.join(l.split()) + r'\\' for l in lines]
    rv +=  [r'\end{bmatrix}']
    return '\n'.join(rv)

def crear_matriz(nom_matriz, tam_filas, tam_columnas, elementos):
    matriz = []
    for i in range(tam_filas):
        fila = []
        for j in range(tam_columnas):
            elemento = float(elementos.get(f"elemento_{i}_{j}", 0))  # Obtiene cada elemento según su nombre
            fila.append(elemento)
        matriz.append(fila)
    matriz = np.array(matriz)
    matrices[nom_matriz] = matriz
    return matriz

# Función para evaluar operaciones matriciales
def evaluar_operacion(operacion):
    # Definir el contexto de matrices y funciones
    contexto = {
        "Det": Det, 
        "Trasp": Trasp, 
        "Inv": Inv, 
        "Diag": Diag, 
        "LU": LU, 
        "Pot": Pot, 
        "GaussJordan": GaussJordan,
        **matrices  # Agregar matrices guardadas al contexto
    }

    try:
        # Evaluar la operación con eval y el contexto definido
        resultado = eval(operacion, {"__builtins__": None}, contexto)

        # Si el resultado es una matriz, convertirlo al formato LaTeX
        if isinstance(resultado, np.ndarray):
            resultado = formatear_matriz_latex(resultado)

        return resultado
    except Exception as e:
        return f"Error al realizar la operación: {str(e)}"

def evaluar_operacion(operacion):
    contexto = {
        "Det": Det, 
        "Trasp": Trasp, 
        "Inv": Inv, 
        "Diag": Diag, 
        "LU": LU, 
        "Pot": Pot, 
        "GaussJordan": GaussJordan,
        **matrices  # Agregar matrices guardadas al contexto
    }

    try:
        # Evaluar la operación con eval y el contexto definido
        resultado = eval(operacion, {"__builtins__": None}, contexto)

        # # Si el resultado es una matriz, convertirlo al formato LaTeX
        if isinstance(resultado, np.ndarray):
            resultado = formatear_matriz_latex(resultado)

        return resultado
    except Exception as e:
        return f"Error al realizar la converción: {str(e)}"