import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import os
import sys

# Configuración de la página para usar todo el ancho
st.set_page_config(layout="wide")

# Obtener la ruta del directorio actual donde se encuentra el script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Añadir la carpeta raíz del proyecto (un nivel arriba de 'scripts/') al PYTHONPATH
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from config.constants import DATA_ACCUMULATED_DIR, COMPANY, COMPANIES


# Usar @st.cache_data para cachear la carga de datos y mejorar el rendimiento
# @st.cache_data
def cargar_datos():
    # Cargamos los datos
    df = pd.read_csv(os.path.join(DATA_ACCUMULATED_DIR, "ci_acumulado.csv"))

    # Asegurarnos de que las columnas AVG y AVG_otros sean numéricas
    df["AVG"] = pd.to_numeric(df["AVG"], errors="coerce").fillna(0)
    df["AVG_otros"] = pd.to_numeric(df["AVG_otros"], errors="coerce").fillna(0)

    # Escalar diferencia_porcentaje al 100%
    df["diferencia_porcentaje"] = df["diferencia_porcentaje"] * 100

    return df


# Cargar los datos
df_accumulated = cargar_datos()

# Organizar los filtros en columnas
st.title("BSG Dashboard")

# Dropdown para seleccionar el año, ordenados de mayor a menor, con el mayor seleccionado por defecto
years = sorted(df_accumulated["Año"].unique(), reverse=True)
selected_year = st.selectbox(
    "Año", years, index=0
)  # El mayor (primero) está seleccionado por defecto

# Filtrar los datos por el año seleccionado
df_filtrado = df_accumulated[df_accumulated["Año"] == selected_year]

# Agregar columnas para los filtros
col1, col2, col3, col4 = st.columns(4)

# Filtro de Región
with col1:
    selected_region = st.selectbox(
        "Región", ["Todas"] + list(df_filtrado["Región"].unique())
    )

# Filtro de Canal
with col2:
    selected_canal = st.selectbox(
        "Canal", ["Todas"] + list(df_filtrado["Canal"].unique())
    )

# Filtro de Tipo, dependiente de Canal
with col3:
    if selected_canal == "Todas":
        tipos_disponibles = df_filtrado["Tipo"].unique()
    else:
        tipos_disponibles = df_filtrado[df_filtrado["Canal"] == selected_canal][
            "Tipo"
        ].unique()
    selected_tipo = st.selectbox("Tipo", ["Todas"] + list(tipos_disponibles))

# Filtro de Métrica, dependiente de Canal y Tipo
with col4:
    if selected_canal == "Todas" and selected_tipo == "Todas":
        metricas_disponibles = df_filtrado["Métrica"].unique()
    elif selected_canal == "Todas":
        metricas_disponibles = df_filtrado[df_filtrado["Tipo"] == selected_tipo][
            "Métrica"
        ].unique()
    elif selected_tipo == "Todas":
        metricas_disponibles = df_filtrado[df_filtrado["Canal"] == selected_canal][
            "Métrica"
        ].unique()
    else:
        metricas_disponibles = df_filtrado[
            (df_filtrado["Canal"] == selected_canal)
            & (df_filtrado["Tipo"] == selected_tipo)
        ]["Métrica"].unique()

    selected_metricas = st.multiselect(
        "Métricas", metricas_disponibles, default=metricas_disponibles[:1]
    )

# Nuevo dropdown para elegir el tipo de comparación
tipo_comparacion = st.selectbox(
    "Tipo de Comparación",
    [
        f"Comparar {COMPANY} contra el promedio de la competencia (AVG_otros)",
        "Comparar las 5 empresas",
        f"Comparar {COMPANY} contra el promedio general (AVG)",
    ],
    index=0,  # Hacer que "Comparar D contra el promedio de la competencia" sea la opción por defecto
)

# Aplicar los filtros según la selección
if selected_region == "Todas":
    # No filtramos por región, mostramos todas
    df_region = df_filtrado[
        (
            df_filtrado["Canal"].isin(
                [selected_canal]
                if selected_canal != "Todas"
                else df_filtrado["Canal"].unique()
            )
        )
        & (
            df_filtrado["Tipo"].isin(
                [selected_tipo]
                if selected_tipo != "Todas"
                else df_filtrado["Tipo"].unique()
            )
        )
        & (df_filtrado["Métrica"].isin(selected_metricas))
    ].drop_duplicates(
        subset=["Métrica", "Región"]
    )  # Evitar duplicados por métricas repetidas
else:
    df_region = df_filtrado[
        (df_filtrado["Región"] == selected_region)
        & (
            df_filtrado["Canal"].isin(
                [selected_canal]
                if selected_canal != "Todas"
                else df_filtrado["Canal"].unique()
            )
        )
        & (
            df_filtrado["Tipo"].isin(
                [selected_tipo]
                if selected_tipo != "Todas"
                else df_filtrado["Tipo"].unique()
            )
        )
        & (df_filtrado["Métrica"].isin(selected_metricas))
    ]

# Crear gráfico según el tipo de comparación seleccionado
if not df_region.empty:
    for metrica in selected_metricas:
        df_metrica = df_region[df_region["Métrica"] == metrica]

        # Ajustar las proporciones de las columnas (1.5:1 para gráfico:KPI)
        col_graph, col_kpi = st.columns([1.5, 1])

        with col_graph:
            fig = go.Figure()

            if tipo_comparacion == "Comparar las 5 empresas":
                # Para comparar las 5 empresas, mostrar una barra para cada empresa por cada región
                for _, row in df_metrica.iterrows():
                    y = [row[company] for company in COMPANIES]
                    fig.add_trace(go.Bar(x=COMPANIES, y=y, name=row["Región"]))

            elif (
                tipo_comparacion
                == f"Comparar {COMPANY} contra el promedio general (AVG)"
            ):
                # Comparar la empresa D contra el promedio general
                for _, row in df_metrica.iterrows():
                    y = [row[COMPANY], row["AVG"]]
                    fig.add_trace(go.Bar(x=[COMPANY, "AVG"], y=y, name=row["Región"]))

            elif (
                tipo_comparacion
                == f"Comparar {COMPANY} contra el promedio de la competencia (AVG_otros)"
            ):
                # Comparar la empresa D contra el promedio de la competencia
                for _, row in df_metrica.iterrows():
                    y = [row[COMPANY], row["AVG_otros"]]
                    fig.add_trace(
                        go.Bar(x=[COMPANY, "AVG_otros"], y=y, name=row["Región"])
                    )

            # Configurar layout del gráfico
            fig.update_layout(
                barmode="group",
                title=f"{metrica}",
                xaxis_title="Empresas",
                yaxis_title="Valor de la Métrica",
                template="plotly_white",
            )

            # Mostrar el gráfico en Streamlit
            st.plotly_chart(fig, use_container_width=True)

        # KPI de diferencia y diferencia_porcentaje
        with col_kpi:
            st.markdown(f"###### Empresa D vs AVG_otros")  # Subtítulo del KPI
            kpi_data = {"Región": [], "Diferencia": [], "Dif. %": []}
            if selected_region == "Todas":
                for _, row in df_metrica.iterrows():
                    kpi_data["Región"].append(row["Región"])
                    kpi_data["Diferencia"].append(row["diferencia"])
                    kpi_data["Dif. %"].append(f"{row['diferencia_porcentaje']:.2f}%")
            else:
                row = df_metrica.iloc[0]  # Solo una fila si la región no es 'Todas'
                kpi_data["Región"].append(row["Región"])
                kpi_data["Diferencia"].append(row["diferencia"])
                kpi_data["Dif. %"].append(f"{row['diferencia_porcentaje']:.2f}%")

            # Convertir a DataFrame y ocultar el índice
            kpi_df = pd.DataFrame(kpi_data).reset_index(drop=True)

            # Mostrar la tabla sin índice
            st.dataframe(kpi_df.style.hide(axis="index"), use_container_width=True)
