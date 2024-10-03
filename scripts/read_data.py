import pandas as pd

import os
import sys

# Obtener la ruta del directorio actual donde se encuentra el script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Añadir la carpeta raíz del proyecto (un nivel arriba de 'scripts/') al PYTHONPATH
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from config.constants import DATA_RAW_CI_DIR, DATA_PROCESSED_DIR, NO_COMPANIES, METRICAS

file = input("Ingrese el nombre del csv: ") + ".csv"

full_path = os.path.join(DATA_RAW_CI_DIR, file)

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

cod_regiones = {
    "NA": ["North America", 0, 0],
    "EA": ["Europe-Africa", 0, 0],
    "AP": ["Asia-Pacifc", 0, 0],
    "LA": ["Latin America", 0, 0],
}

df_messy = pd.read_csv(full_path)

regiones_keys = list(cod_regiones.keys())

regiones_firstkeys = regiones_keys[:-1]

regiones_lastkey = regiones_keys[-1]

for k in regiones_keys:
    cod_regiones[k][1] = df_messy.columns.get_loc(cod_regiones[k][0])

for i, k in enumerate(regiones_firstkeys):
    cod_regiones[k][2] = cod_regiones[regiones_keys[i + 1]][1] - 1

cod_regiones[regiones_lastkey][2] = len(df_messy.columns) - 2

print(cod_regiones)

regiones = {
    "NA": pd.DataFrame(),
    "EA": pd.DataFrame(),
    "AP": pd.DataFrame(),
    "LA": pd.DataFrame(),
}

print(regiones)

for k in regiones.keys():

    regiones[k] = pd.concat(
        [
            df_messy[["Unnamed: 1"]],
            df_messy.iloc[:, cod_regiones[k][1] : cod_regiones[k][2] + 1],
        ],
        axis=1,
    )

    regiones[k].loc[0, "Unnamed: 1"] = "Métrica"
    regiones[k].iloc[0, -1:] = "Canal"

    regiones[k].iloc[1:15, -1:] = ["Internet"] * 14
    regiones[k].iloc[19:38, -1:] = ["Mayorista"] * 19
    regiones[k].iloc[42:48, -1:] = ["Privada"] * 6

    regiones[k] = regiones[k][regiones[k]["Unnamed: 1"] != " "]

    regiones[k].columns = regiones[k].iloc[0]
    regiones[k] = regiones[k][1:]

    regiones[k].drop(columns=NO_COMPANIES, inplace=True)

    regiones[k]["Tipo"] = regiones[k]["Métrica"].map(METRICAS)

    regiones[k].loc[:, "Región"] = cod_regiones[k][0]

    regiones[k].loc[:, "Año"] = year

    first_column = regiones[k].pop("Canal")
    regiones[k].insert(0, "Canal", first_column)
    first_column = regiones[k].pop("Región")
    regiones[k].insert(0, "Región", first_column)
    first_column = regiones[k].pop("Región")
    regiones[k].insert(0, "Región", first_column)

    regiones[k][["A", "B", "C", "D", "E"]] = regiones[k][
        ["A", "B", "C", "D", "E"]
    ].astype(float)

    regiones[k]["AVG"] = regiones[k][["A", "B", "C", "D", "E"]].mean(axis=1)
    regiones[k]["AVG_otros"] = regiones[k][["A", "B", "C", "E"]].mean(axis=1)
    regiones[k]["diferencia"] = regiones[k]["D"] - regiones[k]["AVG_otros"]
    regiones[k]["diferencia_porcentaje"] = (
        regiones[k]["diferencia"] / regiones[k]["AVG_otros"]
    )

    regiones[k].reset_index(drop=True, inplace=True)

df = pd.concat([regiones["NA"], regiones["EA"], regiones["AP"], regiones["LA"]])

df.reset_index(drop=True, inplace=True)

df.loc[:, "Año"] = year
first_column = df.pop("Año")
df.insert(0, "Año", first_column)

print(df.columns)

df.to_csv(os.path.join(DATA_PROCESSED_DIR, "ci_" + str(year) + ".csv"), index=False)
df.to_excel(os.path.join(DATA_PROCESSED_DIR, "ci_" + str(year) + ".xlsx"), index=False)
