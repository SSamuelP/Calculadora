# Calculadora Lógica

Este proyecto es una calculadora lógica basada en la web que permite a los usuarios ingresar una operación lógica y la cantidad de variables involucradas para generar una tabla de verdad. También evalúa si la operación es una Tautología o una Contradicción.

## Características

- Entrada de la cantidad de variables lógicas (hasta 11 variables: p, q, r, s, t, u, v, w, x, y, z).
- Entrada de la operación lógica a evaluar.
- Generación de la tabla de verdad para la operación lógica ingresada.
- Evaluación de la operación como Tautología o Contradicción.
- Visualización de los resultados en una tabla HTML estilizada.

## Tecnologías Utilizadas

- Python
- Flask
- pandas
- ttg (Truth Table Generator)
- HTML/CSS

## Instalación

1. Darle click al botoncito verde "<> Code"

2. Luego darle click a "open github desktop"

3. Luego de abierto github desktop, se da la opción para abrir en "visual studio code"

4. Instalar las dependencias:

    ```en la terminal
    pip install -r requirements.txt
    ```
## Uso

1. Ejecutar la aplicación Flask:

    ```bash
    python main.py
    ```

2. Abrir un navegador web y navegar a `http://127.0.0.1:5000/`.

3. Ingresar la cantidad de variables con las que se trabajará y la operación lógica a realizar, luego hacer clic en "Calcular".

4. Ver los resultados de la operación lógica y la evaluación en la tabla generada.

## Archivos del Proyecto

- `main.py`: Archivo principal de la aplicación Flask que maneja las solicitudes y genera la tabla de verdad.
- `templates/index.html`: Plantilla HTML que muestra el formulario de entrada y los resultados de la operación lógica.
- `requirements.txt`: Archivo que contiene las dependencias necesarias para el proyecto.

## Ejemplo de Operaciones Lógicas

Algunas operaciones lógicas que se pueden ingresar:

- `p and q`
- `p or q`
- `not p`
- `p and (q or r)`
- `(p => q) and (q => r)`
- `(~p and r)`

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio importante antes de enviarlo.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
