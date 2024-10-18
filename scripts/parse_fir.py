import os
import sys

# Obtener la ruta del directorio actual donde se encuentra el script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Añadir la carpeta raíz del proyecto (un nivel arriba de 'scripts/') al PYTHONPATH
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from config.constants import DATA_RAW_FI_DIR, DATA_PARSED_FI_DIR

# Año al que corresponde el archivo
while True:
    try:
        year = int(
            input(
                "Ingresa el año del Reporte de Inteligencia Competitiva (entre 10 y 20): "
            )
        )
        if 10 <= year <= 20:
            print(f"Has ingresado el año {year}.")
            break
        else:
            print("El año debe estar entre 10 y 20, ingrésalo nuevamente: ")
    except ValueError:
        print(
            "El año ingresado debe ser un número entero (entre 10 y 20), ingrésalo nuevamente: "
        )

# Ruta del archivo de Inteligencia Competitiva descargado de BSG online
file = "Industry_2_FIR_Year_" + str(year) + ".csv"
full_path = os.path.join(DATA_RAW_FI_DIR, file)

# Diccionario con las posiciones de las comas a eliminar
comas_a_borrar = {
    # 328: [146, 241],
    328: [148, 243],
    # 340: [85, 136, 185, 327, 385],
    469: [25, 32],
    489: [25, 32],
    509: [25, 32],
    529: [25, 32],
}

# Leer el archivo csv
with open(full_path, "r", newline="", encoding="utf-8") as archivo_entrada:
    lineas = archivo_entrada.readlines()

# Borrar las comas de las posiciones específicas
for fila, posiciones in comas_a_borrar.items():
    if fila < len(lineas):
        linea = list(
            lineas[fila]
        )  # Convertir la línea a lista para modificar caracteres
        # Ordenar las posiciones en orden decreciente para evitar problemas de desplazamiento de índices
        posiciones.sort(reverse=True)
        for posicion in posiciones:
            if posicion < len(linea) and linea[posicion] == ",":
                del linea[posicion]  # Eliminar la coma en la posición específica
        lineas[fila] = "".join(linea)  # Volver a convertir la línea a string


# Guardar el nuevo archivo corregido
with open(
    os.path.join(DATA_PARSED_FI_DIR, "fi_parsed_") + str(year) + ".csv",
    "w",
    newline="",
    encoding="utf-8",
) as archivo_salida:
    archivo_salida.writelines(lineas)

print("Archivo corregido generado con éxito.")
