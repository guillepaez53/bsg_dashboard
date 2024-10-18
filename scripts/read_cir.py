import pandas as pd

import os
import sys

# Obtener la ruta del directorio actual donde se encuentra el script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Añadir la carpeta raíz del proyecto (un nivel arriba de 'scripts/') al PYTHONPATH
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from config.constants import (
    DATA_RAW_CI_DIR,
    DATA_PROCESSED_CI_DIR,
    REGIONES,
    COMPANIES,
    NO_COMPANIES,
    METRICAS,
)

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
file = "Industry_2_CIR_Year_" + str(year) + ".csv"
full_path = os.path.join(DATA_RAW_CI_DIR, file)

# DataFrame desordenado
df_messy = pd.read_csv(full_path)

# Diccionario con posiciones de columna de cada región para parsear
regiones_parser = {
    "NA": [0, 0],
    "EA": [0, 0],
    "AP": [0, 0],
    "LA": [0, 0],
}

regiones_keys = list(REGIONES.keys())

regiones_firstkeys = regiones_keys[:-1]

regiones_lastkey = regiones_keys[-1]

for k in regiones_keys:
    regiones_parser[k][0] = df_messy.columns.get_loc(REGIONES[k])

for i, k in enumerate(regiones_firstkeys):
    regiones_parser[k][1] = regiones_parser[regiones_keys[i + 1]][0] - 1

regiones_parser[regiones_lastkey][1] = len(df_messy.columns) - 2

# Diccionario con DataFrames por regiones
regiones = {
    "NA": pd.DataFrame(),
    "EA": pd.DataFrame(),
    "AP": pd.DataFrame(),
    "LA": pd.DataFrame(),
}

# Construcción de un DataFrame por cada región
for k in regiones.keys():

    # Concatenación horizontal de la columna con los nombres de las métricas y las columnas con la info de las empresas para esa región
    regiones[k] = pd.concat(
        [
            df_messy[["Unnamed: 1"]],
            df_messy.iloc[:, regiones_parser[k][0] : regiones_parser[k][1] + 1],
        ],
        axis=1,
    )

    # Nombre de columnas (en la primera fila del DataFrame)
    regiones[k].loc[0, "Unnamed: 1"] = "Métrica"
    regiones[k].iloc[0, -1:] = "Canal"

    # Clasificación de métricas por canal
    regiones[k].iloc[1:15, -1:] = ["2 - Internet"] * 14
    regiones[k].iloc[19:38, -1:] = ["1 - Mayorista"] * 19
    regiones[k].iloc[42:48, -1:] = ["3 - Privada"] * 6

    # DataFrame filtrado
    regiones[k] = regiones[k][regiones[k]["Unnamed: 1"] != " "]

    # Primera fila como encabezado de columnas
    regiones[k].columns = regiones[k].iloc[0].astype(str).values
    regiones[k] = regiones[k][1:]

    # Eliminación de columnas de compañías que no juegan
    regiones[k].drop(columns=NO_COMPANIES, inplace=True)

    # Clasificación de métricas por tipo
    regiones[k]["Tipo"] = regiones[k]["Métrica"].map(METRICAS)

    # Conversión de datos a float
    regiones[k][COMPANIES] = regiones[k][COMPANIES].astype(float)

    # Cálculos de nuevas métricas
    new_metrics = {}

    for company in COMPANIES:

        new_metrics[company] = {}

        new_metrics[company]["wholesale_net_price"] = (
            regiones[k]
            .loc[regiones[k]["Métrica"] == " Wholesale Price ($ per pair)", company]
            .item()
            - regiones[k]
            .loc[regiones[k]["Métrica"] == " Rebate Offer ($ per pair)", company]
            .item()
        )

        new_metrics[company]["wholesale_income"] = (
            new_metrics[company]["wholesale_net_price"]
            * regiones[k]
            .loc[
                (regiones[k]["Canal"] == "1 - Mayorista")
                & (regiones[k]["Métrica"] == " Pairs Sold (000s)"),
                company,
            ]
            .item()
        )

        new_metrics[company]["retail_income"] = (
            regiones[k]
            .loc[regiones[k]["Métrica"] == " Retail Price ($ per pair)", company]
            .item()
            * regiones[k]
            .loc[
                (regiones[k]["Canal"] == "2 - Internet")
                & (regiones[k]["Métrica"] == " Pairs Sold (000s)"),
                company,
            ]
            .item()
        )
        new_metrics[company]["offer_income"] = (
            regiones[k]
            .loc[regiones[k]["Métrica"] == " Offer Price (max = $40.00)", company]
            .item()
            * regiones[k]
            .loc[
                (regiones[k]["Canal"] == "3 - Privada")
                & (regiones[k]["Métrica"] == " Pairs Sold (000s)"),
                company,
            ]
            .item()
        )

    # Concatenación de nuevas métricas en el DataFrame
    regiones[k] = pd.concat(
        [
            regiones[k],
            pd.DataFrame(
                {
                    "Canal": "1 - Mayorista",
                    "Tipo": "b - Precio",
                    "Métrica": " Wholesale Net Price ($ per pair)",
                    "A": new_metrics["A"]["wholesale_net_price"],
                    "B": new_metrics["B"]["wholesale_net_price"],
                    "C": new_metrics["C"]["wholesale_net_price"],
                    "D": new_metrics["D"]["wholesale_net_price"],
                    "E": new_metrics["E"]["wholesale_net_price"],
                },
                index=[0],
            ),
            pd.DataFrame(
                {
                    "Canal": "1 - Mayorista",
                    "Tipo": "a - Ingreso",
                    "Métrica": " Wholesale Income ($000s)",
                    "A": new_metrics["A"]["wholesale_income"],
                    "B": new_metrics["B"]["wholesale_income"],
                    "C": new_metrics["C"]["wholesale_income"],
                    "D": new_metrics["D"]["wholesale_income"],
                    "E": new_metrics["E"]["wholesale_income"],
                },
                index=[0],
            ),
            pd.DataFrame(
                {
                    "Canal": "2 - Internet",
                    "Tipo": "a - Ingreso",
                    "Métrica": " Retail Income ($000s)",
                    "A": new_metrics["A"]["retail_income"],
                    "B": new_metrics["B"]["retail_income"],
                    "C": new_metrics["C"]["retail_income"],
                    "D": new_metrics["D"]["retail_income"],
                    "E": new_metrics["E"]["retail_income"],
                },
                index=[0],
            ),
            pd.DataFrame(
                {
                    "Canal": "3 - Privada",
                    "Tipo": "a - Ingreso",
                    "Métrica": " Offer Income ($000s)",
                    "A": new_metrics["A"]["offer_income"],
                    "B": new_metrics["B"]["offer_income"],
                    "C": new_metrics["C"]["offer_income"],
                    "D": new_metrics["D"]["offer_income"],
                    "E": new_metrics["E"]["offer_income"],
                },
                index=[0],
            ),
        ],
        ignore_index=True,
    )

    # Renombrado de métricas por canal y tipo
    regiones[k]["Métrica"] = (
        regiones[k]["Canal"].str[:4]
        + regiones[k]["Tipo"].str[:3]
        + regiones[k]["Métrica"]
    )

    # Ordenamiento de métricas por canal y tipo
    regiones[k].sort_values(by="Métrica", inplace=True)

    # Columna con la región
    regiones[k].loc[:, "Región"] = REGIONES[k]

    # Reordenamiento de columnas
    nueva_orden = ["Región", "Canal", "Tipo"] + [
        col for col in regiones[k].columns if col not in ["Región", "Canal", "Tipo"]
    ]
    regiones[k] = regiones[k][nueva_orden]

    # Cálculos de promedios y diferencias
    regiones[k]["AVG"] = regiones[k][["A", "B", "C", "D", "E"]].mean(axis=1)
    regiones[k]["AVG_otros"] = regiones[k][["A", "B", "C", "E"]].mean(axis=1)
    regiones[k]["diferencia"] = regiones[k]["D"] - regiones[k]["AVG_otros"]
    regiones[k]["diferencia_porcentaje"] = (
        regiones[k]["diferencia"] / regiones[k]["AVG_otros"]
    )

    # Reseteo index
    regiones[k].reset_index(drop=True, inplace=True)

# Concatenación de los DataFrames de las 4 regiones
df = pd.concat([regiones["NA"], regiones["EA"], regiones["AP"], regiones["LA"]])

# Reseteo de índice
df.reset_index(drop=True, inplace=True)

# Mover Año a primera columna
df.loc[:, "Año"] = year + 2000
first_column = df.pop("Año")
df.insert(0, "Año", first_column)

# Exportación
df.to_csv(os.path.join(DATA_PROCESSED_CI_DIR, "ci_" + str(year) + ".csv"), index=False)
df.to_excel(
    os.path.join(DATA_PROCESSED_CI_DIR, "ci_" + str(year) + ".xlsx"), index=False
)
