import pandas as pd

import os
import sys

# Obtener la ruta del directorio actual donde se encuentra el script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Añadir la carpeta raíz del proyecto (un nivel arriba de 'scripts/') al PYTHONPATH
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from config.constants import DATA_PARSED_FI_DIR, DATA_PROCESSED_FI_DIR

# Año al que corresponde el archivo
while True:
    try:
        year = int(
            input(
                "Ingresa el año del Reporte de la Industria de Calzado (entre 10 y 20): "
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
file = "fi_parsed_" + str(year) + ".csv"
full_path = os.path.join(DATA_PARSED_FI_DIR, file)

# DataFrame desordenado
df_messy = pd.read_csv(full_path)

print(df_messy)

df_messy.to_csv(
    os.path.join(DATA_PROCESSED_FI_DIR, "fi_" + str(year) + ".csv"), index=False
)

df_messy.to_excel(
    os.path.join(DATA_PROCESSED_FI_DIR, "fi_" + str(year) + ".xlsx"), index=False
)
