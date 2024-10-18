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

df_bpa = pd.concat(
    [df_messy.iloc[72:82, 5:11], df_messy.iloc[72:82, 18]], axis=1
).copy()

df_bpa.reset_index(drop=True, inplace=True)

df_bpa.rename(
    columns={
        " .4": "Año",
        " .5": "A",
        " .6": "B",
        " .7": "C",
        " .8": "D",
        " .9": "E",
        " .17": "Inv_exp",
    },
    inplace=True,
)

df_bpa["Año"] = df_bpa["Año"].str[2:].astype(int)

for c in df_bpa.columns[1:]:
    df_bpa[c] = df_bpa[c].astype(float)

df_roe = pd.concat(
    [df_messy.iloc[94:104, 5:11], df_messy.iloc[94:104, 18]], axis=1
).copy()

df_roe.reset_index(drop=True, inplace=True)

df_roe.rename(
    columns={
        " .4": "Año",
        " .5": "A",
        " .6": "B",
        " .7": "C",
        " .8": "D",
        " .9": "E",
        " .17": "Inv_exp",
    },
    inplace=True,
)

df_roe["Año"] = df_roe["Año"].str[2:].astype(int)

for c in df_roe.columns[1:]:
    df_roe[c] = df_roe[c].astype(float)

df_pa = pd.concat(
    [df_messy.iloc[116:126, 5:11], df_messy.iloc[116:126, 18]], axis=1
).copy()

df_pa.reset_index(drop=True, inplace=True)

df_pa.rename(
    columns={
        " .4": "Año",
        " .5": "A",
        " .6": "B",
        " .7": "C",
        " .8": "D",
        " .9": "E",
        " .17": "Inv_exp",
    },
    inplace=True,
)

df_pa["Año"] = df_pa["Año"].str[2:].astype(int)

for c in df_pa.columns[1:]:
    df_pa[c] = df_pa[c].astype(float)

df_cc = pd.concat(
    [df_messy.iloc[141:151, 5:11], df_messy.iloc[141:151, 18]], axis=1
).copy()

df_cc.reset_index(drop=True, inplace=True)

df_cc.rename(
    columns={
        " .4": "Año",
        " .5": "A",
        " .6": "B",
        " .7": "C",
        " .8": "D",
        " .9": "E",
        " .17": "Inv_exp",
    },
    inplace=True,
)

df_cc["Año"] = df_cc["Año"].str[2:]  # .astype(int)

for c in df_cc.columns:
    df_cc[c] = df_cc[c].astype(int)

df_ci = pd.concat(
    [df_messy.iloc[161:171, 5:11], df_messy.iloc[161:171, 18]], axis=1
).copy()

df_ci.reset_index(drop=True, inplace=True)

df_ci.rename(
    columns={
        " .4": "Año",
        " .5": "A",
        " .6": "B",
        " .7": "C",
        " .8": "D",
        " .9": "E",
        " .17": "Inv_exp",
    },
    inplace=True,
)

df_ci["Año"] = df_ci["Año"].str[2:]  # .astype(int)

for c in df_ci.columns:
    df_ci[c] = df_ci[c].astype(int)

df_rss = pd.concat(
    [df_messy.iloc[183, 5:16].to_frame().T, df_messy.iloc[185:191, 5:16]], axis=0
).copy()

df_rss.iloc[0, 0] = "Año"

df_rss.iloc[1:4, 0] = " $000s -" + df_rss.iloc[1:4, 0]
df_rss.iloc[4:, 0] = " $/Unit -" + df_rss.iloc[4:, 0]

df_rss = df_rss.T

df_rss.columns = df_rss.iloc[0].astype(str).values
df_rss = df_rss[1:]

df_rss.reset_index(drop=True, inplace=True)

for c in df_rss.columns[:4]:
    df_rss[c] = df_rss[c].astype(int)

for c in df_rss.columns[4:]:
    df_rss[c] = df_rss[c].astype(float)

df_mat = pd.concat(
    [df_messy.iloc[290, 6:8].to_frame().T, df_messy.iloc[297, 6:8].to_frame().T]
).copy()

df_mat.columns = df_mat.iloc[0].astype(str).values
df_mat = df_mat[1:]

df_mat.reset_index(drop=True, inplace=True)

for c in df_mat.columns:
    df_mat[c] = df_mat[c].astype(float)

df_mat.loc[:, "Año"] = int(year)

# Mover Año a primera columna

first_column = df_mat.pop("Año")
df_mat.insert(0, "Año", first_column)

df_prod = df_messy.iloc[305:323, 3:11].copy()
df_prod.iloc[0, 0] = "Métrica"
df_prod.iloc[8, 0] = " Footwear Demand -"
df_prod.iloc[7, 0] = df_prod.iloc[7, 0][:18] + df_prod.iloc[7, 2]
df_prod.iloc[8, 0] = df_prod.iloc[8, 0][:18] + df_prod.iloc[8, 2]
df_prod.iloc[16, 0] = " Demand -"
df_prod.iloc[15, 0] = df_prod.iloc[15, 0][:9] + df_prod.iloc[15, 2]
df_prod.iloc[16, 0] = df_prod.iloc[16, 0][:9] + df_prod.iloc[16, 2]
df_prod.drop(columns=[" .3", " .4"], inplace=True)
df_prod.columns = df_prod.iloc[0].astype(str).values
df_prod = df_prod[1:]
df_prod = df_prod[df_prod["Métrica"] != " "]
df_prod.loc[:, "Año"] = int(year)
first_column = df_prod.pop("Año")
df_prod.insert(0, "Año", first_column)
df_prod.reset_index(drop=True, inplace=True)

df_prod_uso = df_prod.iloc[:2, :].copy()
df_prod_uso.reset_index(drop=True, inplace=True)

for c in df_prod_uso.columns[2:]:
    df_prod_uso[c] = df_prod_uso[c].astype(float)

df_prod_sales = df_prod.iloc[2:, :].copy()
df_prod_sales.reset_index(drop=True, inplace=True)

for c in df_prod_sales.columns[2:-1]:
    df_prod_sales[c] = df_prod_sales[c].astype(int)

if df_prod_sales.iloc[4, -1] == " ":
    df_prod_sales.iloc[4, -1] = 0
    for c in df_prod_sales.columns[2:-1]:
        df_prod_sales.iloc[4, -1] += df_prod_sales.loc[4, c]

df_prod_sales[" Total"] = df_prod_sales[" Total"].astype(int)

df_prev = df_messy.iloc[324:333, 5:11].copy()
df_prev.iloc[0, 0] = "Previsión Año"
df_prev.columns = df_prev.iloc[0].astype(str).values
df_prev = df_prev[1:]
df_prev = df_prev[df_prev["Previsión Año"] != " "]
df_prev.iloc[:3, 0] = " Branded Demand -" + df_prev.iloc[:3, 0]
df_prev.iloc[3:, 0] = " P-Label Demand -" + df_prev.iloc[3:, 0]
df_prev.loc[:, "Año"] = int(year)
first_column = df_prev.pop("Año")
df_prev.insert(0, "Año", first_column)
df_prev.reset_index(drop=True, inplace=True)

for c in df_prev.columns[2:]:
    df_prev[c] = df_prev[c].astype(int)


with pd.ExcelWriter(
    os.path.join(DATA_PROCESSED_FI_DIR, "fir_" + str(year) + ".xlsx"),
    engine="openpyxl",
) as writer:
    df_bpa.to_excel(writer, sheet_name="Beneficios x acción")
    df_roe.to_excel(writer, sheet_name="ROE")
    df_pa.to_excel(writer, sheet_name="Precio acción")
    df_cc.to_excel(writer, sheet_name="Calificación crediticia")
    df_ci.to_excel(writer, sheet_name="Calificación imagen")
    df_rss.to_excel(writer, sheet_name="RSE")
    df_mat.to_excel(writer, sheet_name="Precio materiales")
    df_prod_uso.to_excel(writer, sheet_name="Producción - Recursos")
    df_prod_sales.to_excel(writer, sheet_name="Producción - Ventas")
    df_prev.to_excel(writer, sheet_name="Previsión demanda")

print()
print(df_bpa)
print(df_bpa.info())
print()
print(df_roe)
print(df_roe.info())
print()
print(df_pa)
print(df_pa.info())
print()
print(df_cc)
print(df_cc.info())
print()
print(df_ci)
print(df_ci.info())
print()
print(df_rss)
print(df_rss.info())
print()
print(df_mat)
print(df_mat.info())
print()
print(df_prod_uso)
print(df_prod_uso.info())
print()
print(df_prod_sales)
print(df_prod_sales.info())
print()
print(df_prev)
print(df_prev.info())
print()
