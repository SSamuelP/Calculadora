import numpy as np
from scipy.linalg import lu
# Funciones para operaciones de matrices
def calcular_determinante(matriz):
    return np.linalg.det(matriz)

def calcular_traspuesta(matriz):
    return matriz.T

def calcular_inversa(matriz):
    try:
        return np.linalg.inv(matriz)
    except np.linalg.LinAlgError:
        return "No invertible"

def calcular_diagonal(matriz):
    return np.diag(matriz)

def factorizacion_LU(matriz):
    P, L, U = lu(matriz)
    return P, L, U

def calcular_potencia(matriz, potencia):
    return np.linalg.matrix_power(matriz, potencia)

def gauss_jordan(matriz_aumentada):
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