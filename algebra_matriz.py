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
    return np.diag(matriz)

#Factorización LU
def LU(matriz):
    P, L, U = lu(matriz)
    return P, L, U

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

def formatear_matriz_latex(resultado):
    # Convierte la matriz en formato LaTeX para MathJax sin añadir delimitadores adicionales
    filas = [" & ".join(map(str, fila)) for fila in resultado]  # Une elementos de cada fila con "&"
    matriz_latex = "\\begin{bmatrix} " + " \\\\ ".join(filas) + " \\end{bmatrix}"
    return matriz_latex

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