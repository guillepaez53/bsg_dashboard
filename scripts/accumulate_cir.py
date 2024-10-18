import pandas as pd

import os
import sys

# Obtener la ruta del directorio actual donde se encuentra el script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Añadir la carpeta raíz del proyecto (un nivel arriba de 'scripts/') al PYTHONPATH
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from config.constants import DATA_PROCESSED_CI_DIR, DATA_ACCUMULATED_CI_DIR

while True:
    try:
        year = int(
            input(
                "Ingresa el año del Reporte de Inteligencia Competitiva (entre 10 y 20) a acumular: "
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

try:
    df_old = pd.read_csv(os.path.join(DATA_ACCUMULATED_CI_DIR, "ci_acumulado.csv"))
    df_new = pd.read_csv(
        os.path.join(DATA_PROCESSED_CI_DIR, "ci_" + str(year) + ".csv")
    )
    df_accumulated = pd.concat([df_old, df_new], axis=0)
except FileNotFoundError:
    df_accumulated = pd.read_csv(
        os.path.join(DATA_PROCESSED_CI_DIR, "ci_" + str(year) + ".csv")
    )

df_accumulated.to_csv(
    os.path.join(DATA_ACCUMULATED_CI_DIR, "ci_acumulado.csv"), index=False
)
df_accumulated.to_excel(
    os.path.join(DATA_ACCUMULATED_CI_DIR, "ci_acumulado.xlsx"), index=False
)
