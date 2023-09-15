import cv2
import numpy as np

# Función para detectar píxeles negros y agruparlos en rangos
def detectar_pixeles(imagen_gris, opcion):
    coordenadas = np.argwhere((imagen_gris == 0) if opcion == '1' else (imagen_gris != 255))
    coordenadas = sorted(coordenadas, key=lambda coord: (coord[0], coord[1]))

    rangos = []
    rango_actual = []

    for coord in coordenadas:
        x, y = coord

        if not rango_actual or (y == rango_actual[-1][-1] + 1 and opcion == '1') or (y == rango_actual[-1][-1] - 1 and opcion == '2'):
            rango_actual.append((x, y))
        else:
            if rango_actual:
                min_x = rango_actual[0][0]
                min_y = rango_actual[0][1]
                max_x = rango_actual[-1][0]
                max_y = rango_actual[-1][1]
                rangos.append((min_x, min_y, max_x, max_y))
            rango_actual = [(x, y)]

    if rango_actual:
        min_x = rango_actual[0][0]
        min_y = rango_actual[0][1]
        max_x = rango_actual[-1][0]
        max_y = rango_actual[-1][1]
        rangos.append((min_x, min_y, max_x, max_y))

    return rangos

# Cargar la imagen
imagen = cv2.imread('imagen.png')

# Convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Opción para elegir qué píxeles detectar
opcion = input("¿Qué píxeles deseas detectar? (1 para negros, 2 para no blancos): ")

if opcion not in ['1', '2']:
    print("Opción no válida. Debes ingresar 1 o 2 para seleccionar la opción.")
else:
    resultados = detectar_pixeles(imagen_gris, opcion)

    # Guardar el resultado en un archivo de texto
    with open('pixeles.txt', 'w') as archivo:
        for x1, y1, x2, y2 in resultados:
            archivo.write(f'({x1}, {y1}) - ({x2}, {y2})\n')

    print("Los resultados se han guardado en 'pixeles.txt'.")


# Abrir el archivo de entrada para lectura
with open('pixeles.txt', 'r') as archivo_entrada:
    lineas = archivo_entrada.readlines()

# Lista para almacenar las salidas
salidas = []

# Iterar sobre cada línea del archivo de entrada
for linea in lineas:
    # Extraer los valores de las coordenadas
    partes = linea.strip().split(') - (')
    inicio = partes[0].strip('(').split(', ')
    fin = partes[1].strip(')').split(', ')

    # Convertir los valores a enteros
    inicio_x, inicio_y = int(inicio[0]), int(inicio[1])
    fin_x, fin_y = int(fin[0]), int(fin[1])

    # Crear la cadena de salida
    salida = f'for (x = {inicio_y}; x < {fin_y}; x++)\n'
    salida += f'  gfx->drawPixel(x, {inicio_x}, WHITE);\n'

    # Agregar la salida a la lista
    salidas.append(salida)

# Abrir el archivo de salida para escritura
with open('Arduino_GFX.txt', 'w') as archivo_salida:
    # Escribir las salidas en el archivo de salida
    for salida in salidas:
        archivo_salida.write(salida)

print("El archivo de salida 'Arduino_GFX.txt' ha sido generado.")






# Diccionario para mapear opciones del usuario a colores en inglés
colores_ingles = {
    '1': 'BLACK',
    '2': 'NAVY',
    '3': 'DARKGREEN',
    '4': 'DARKCYAN',
    '5': 'MAROON',
    '6': 'PURPLE',
    '7': 'OLIVE',
    '8': 'LIGHTGREY ',
    '9': 'DARKGREY',
    '10': 'BLUE',
    '11': 'GREEN',
    '12': 'CYAN',
    '13': 'RED',
    '14': 'MAGENTA',
    '15': 'YELLOW',
    '16': 'ORANGE',
    '17': 'GREENYELLOW',
    '18': 'PINK',

    # Agrega más colores según sea necesario
}

# Solicitar al usuario que seleccione un color para reemplazar "WHITE"
print("Selecciona un color para reemplazar 'WHITE':")
for opcion, color in colores_ingles.items():
    print(f"{opcion} - {color}")

opcion_color_reemplazo = input("Ingresa el número del color que deseas utilizar (por ejemplo, 1 para negro): ")

# Verificar si la opción de color ingresada es válida
if opcion_color_reemplazo in colores_ingles:
    color_reemplazo = colores_ingles[opcion_color_reemplazo]
else:
    print("Opción de color no válida. Se utilizará el color predeterminado (WHITE).")
    color_reemplazo = 'WHITE'  # Color predeterminado si la opción no es válida

# Nombre del archivo de entrada y archivo de salida
archivo_entrada = 'Arduino_GFX.txt'
archivo_salida = 'Arduino_GFX_color.txt'

# Abrir el archivo de entrada para lectura
with open(archivo_entrada, 'r') as archivo_entrada:
    lineas = archivo_entrada.readlines()

# Lista para almacenar las salidas
salidas = []

# Iterar sobre cada línea del archivo de entrada
for linea in lineas:
    # Reemplazar "WHITE" por el color seleccionado
    linea_modificada = linea.replace('WHITE', color_reemplazo)
    salidas.append(linea_modificada)

# Abrir el archivo de salida para escritura
with open(archivo_salida, 'w') as archivo_salida:
    # Escribir las salidas en el archivo de salida
    for salida in salidas:
        archivo_salida.write(salida)

print(f"El archivo de salida '{archivo_salida}' ha sido generado con el color '{color_reemplazo}'.")


