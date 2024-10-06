import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import os
import sys


# Configuración de la página para usar todo el ancho
st.set_page_config(layout="wide")

# Obtener la ruta del directorio actual donde se encuentra el script
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)


from config.constants import DATA_ACCUMULATED_DIR, COMPANY, COMPANIES


# Cargar los datos
def cargar_datos():
    df = pd.read_csv(os.path.join(DATA_ACCUMULATED_DIR, "ci_acumulado.csv"))
    df["AVG"] = pd.to_numeric(df["AVG"], errors="coerce").fillna(0)
    df["AVG_otros"] = pd.to_numeric(df["AVG_otros"], errors="coerce").fillna(0)
    # df["diferencia_porcentaje"] = df["diferencia_porcentaje"] * 100
    return df


df_accumulated = cargar_datos()


# --- PESTAÑA UNIFICADA: ANÁLISIS IC ---

st.title("BSG Dashboard: Inteligencia Competitiva")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("###### Regiones, Empresas y Rango de años a analizar")

col1, col2 = st.columns(2)

with col1:
    # Checkboxes para las Regiones
    regiones = df_accumulated["Región"].unique()
    region_selected = []
    cols = st.columns(len(regiones))

    for i, region in enumerate(regiones):
        # Asignar una clave única específica
        if cols[i].checkbox(region, value=True, key=f"region_temporal_{region}"):
            region_selected.append(region)

    # Checkbox para seleccionar empresas y agregados
    with st.container():
        cols = st.columns([1, 1, 1, 1, 1, 3, 2])
        A_selected = cols[0].checkbox("A", value=False)
        B_selected = cols[1].checkbox("B", value=False)
        C_selected = cols[2].checkbox("C", value=False)
        D_selected = cols[3].checkbox("D", value=True)  # Por defecto seleccionado
        E_selected = cols[4].checkbox("E", value=False)
        AVG_otros_selected = cols[5].checkbox(
            "AVG_otros", value=True
        )  # Por defecto seleccionado
        AVG_selected = cols[6].checkbox("AVG", value=False)

with col2:
    # Slider para seleccionar el rango de años (Inicio y Fin)
    if df_accumulated["Año"].max() > df_accumulated["Año"].min():
        start_year, end_year = st.slider(
            "Seleccionar el rango de años a analizar",
            min_value=int(df_accumulated["Año"].min()),
            max_value=int(df_accumulated["Año"].max()),
            value=(
                int(df_accumulated["Año"].min()),
                int(df_accumulated["Año"].max()),
            ),
            step=1,
            key="slider_temporal",
        )
    else:
        start_year = df_accumulated["Año"].min()
        end_year = df_accumulated["Año"].max()

st.markdown("<br>", unsafe_allow_html=True)

# Segunda fila - Checkboxes de Canal y Tipo
col1, col2 = st.columns([3, 6])  # Ajustando la proporción para canales y tipos

with col1:
    st.markdown("###### Selección de Canales")
    canales_disponibles = df_accumulated["Canal"].unique()
    canal_selected = []
    cols_canal = st.columns(len(canales_disponibles))

    for i, canal in enumerate(canales_disponibles):
        # Checkboxes para los canales
        if cols_canal[i].checkbox(canal, value=True, key=f"canal_temporal_{canal}"):
            canal_selected.append(canal)

with col2:
    st.markdown("###### Selección de Tipos")
    tipos_disponibles = df_accumulated["Tipo"].unique()
    tipo_selected = []
    cols_tipo = st.columns(len(tipos_disponibles))

    for i, tipo in enumerate(tipos_disponibles):
        # Checkboxes para los tipos
        if cols_tipo[i].checkbox(tipo, value=True, key=f"tipo_temporal_{tipo}"):
            tipo_selected.append(tipo)

# Filtrar las métricas disponibles según el canal y tipo seleccionados
metricas_disponibles_temporal = df_accumulated[
    (df_accumulated["Canal"].isin(canal_selected))
    & (df_accumulated["Tipo"].isin(tipo_selected))
]["Métrica"].unique()

# Tercera fila - Multiselects de Métricas (ahora filtradas por Canal y Tipo)
col1, col2 = st.columns(2)

with col1:
    selected_metricas_1 = st.multiselect(
        "Métricas 1",
        metricas_disponibles_temporal,
        default=(
            metricas_disponibles_temporal[:1]
            if len(metricas_disponibles_temporal) > 0
            else None
        ),
        key="metricas_1",
    )
with col2:
    selected_metricas_2 = st.multiselect(
        "Métricas 2",
        metricas_disponibles_temporal,
        default=None,
        key="metricas_2",
    )

st.markdown("<br>", unsafe_allow_html=True)

# Filtrar el dataframe por los años, regiones seleccionadas y por las métricas
df_metrica_filtrada_temporal = df_accumulated[
    (df_accumulated["Año"] >= start_year)
    & (df_accumulated["Año"] <= end_year)
    & (df_accumulated["Región"].isin(region_selected))  # Filtro por regiones
]

# Verificar si es un análisis transversal o temporal
is_transversal = start_year == end_year

if is_transversal:
    # Análisis Transversal (Gráfico de Barras)
    if selected_metricas_1 and selected_metricas_2:
        # Mostrar dos gráficos en paralelo si ambos multiselects tienen métricas
        max_len = max(len(selected_metricas_1), len(selected_metricas_2))
        for i in range(max_len):
            col_graph1, col_graph2 = st.columns(2)

            if i < len(selected_metricas_1):
                with col_graph1:
                    fig_1 = go.Figure()
                    metrica_1 = selected_metricas_1[i]
                    df_metrica_1 = df_metrica_filtrada_temporal[
                        df_metrica_filtrada_temporal["Métrica"] == metrica_1
                    ]
                    for region in region_selected:
                        df_region = df_metrica_1[df_metrica_1["Región"] == region]
                        for company in COMPANIES + ["AVG", "AVG_otros"]:
                            if eval(f"{company}_selected"):
                                fig_1.add_trace(
                                    go.Bar(
                                        x=[region],
                                        y=[df_region[company].mean()],
                                        name=f"{company} - {region}",
                                    )
                                )
                    fig_1.update_layout(
                        barmode="group",
                        title=f"{metrica_1}",
                        xaxis_title="Regiones",
                        yaxis_title="Valor de la Métrica",
                        template="plotly_white",
                    )
                    st.plotly_chart(fig_1, use_container_width=True)

            if i < len(selected_metricas_2):
                with col_graph2:
                    fig_2 = go.Figure()
                    metrica_2 = selected_metricas_2[i]
                    df_metrica_2 = df_metrica_filtrada_temporal[
                        df_metrica_filtrada_temporal["Métrica"] == metrica_2
                    ]
                    for region in region_selected:
                        df_region = df_metrica_2[df_metrica_2["Región"] == region]
                        for company in COMPANIES + ["AVG", "AVG_otros"]:
                            if eval(f"{company}_selected"):
                                fig_2.add_trace(
                                    go.Bar(
                                        x=[region],
                                        y=[df_region[company].mean()],
                                        name=f"{company} - {region}",
                                    )
                                )
                    fig_2.update_layout(
                        barmode="group",
                        title=f"{metrica_2}",
                        xaxis_title="Regiones",
                        yaxis_title="Valor de la Métrica",
                        template="plotly_white",
                    )
                    st.plotly_chart(fig_2, use_container_width=True)

    else:
        # Si solo hay métricas en uno de los multiselects, mostrar gráfico y tabla
        metricas_to_plot = selected_metricas_1 or selected_metricas_2
        for metrica in metricas_to_plot:
            df_metrica = df_metrica_filtrada_temporal[
                df_metrica_filtrada_temporal["Métrica"] == metrica
            ]

            st.markdown("<br>", unsafe_allow_html=True)

            col_graph, col_kpi = st.columns(2)

            with col_graph:
                fig = go.Figure()
                for region in region_selected:
                    df_region = df_metrica[df_metrica["Región"] == region]
                    for company in COMPANIES + ["AVG", "AVG_otros"]:
                        if eval(f"{company}_selected"):
                            fig.add_trace(
                                go.Bar(
                                    x=[region],
                                    y=[df_region[company].mean()],
                                    name=f"{company} - {region}",
                                )
                            )
                fig.update_layout(
                    barmode="group",
                    title=f"{metrica}",
                    xaxis_title="Regiones",
                    yaxis_title="Valor de la Métrica",
                    template="plotly_white",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_kpi:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"###### Empresa D vs AVG_otros")
                st.markdown("<br>", unsafe_allow_html=True)

                kpi_data = {"Región": [], "Diferencia": [], "Dif. %": []}

                # Recorrer las regiones seleccionadas
                for _, row in df_metrica.iterrows():
                    kpi_data["Región"].append(row["Región"])
                    kpi_data["Diferencia"].append(row["diferencia"])
                    kpi_data["Dif. %"].append(f"{row['diferencia_porcentaje']:.2%}")

                # Crear DataFrame con los KPIs
                kpi_df = pd.DataFrame(kpi_data).reset_index(drop=True)
                st.dataframe(kpi_df.style.hide(axis="index"), use_container_width=True)

else:
    # Análisis Temporal (Gráfico de líneas y tabla de variación porcentual)
    if selected_metricas_1 and selected_metricas_2:
        # Mostrar dos gráficos en paralelo si ambos multiselects tienen métricas
        max_len = max(len(selected_metricas_1), len(selected_metricas_2))
        for i in range(max_len):
            col_graph1, col_graph2 = st.columns(2)

            if i < len(selected_metricas_1):
                with col_graph1:
                    fig_1 = go.Figure()
                    metrica_1 = selected_metricas_1[i]
                    df_metrica_1 = df_metrica_filtrada_temporal[
                        df_metrica_filtrada_temporal["Métrica"] == metrica_1
                    ]
                    for region in region_selected:
                        df_region = df_metrica_1[df_metrica_1["Región"] == region]
                        for company in COMPANIES + ["AVG", "AVG_otros"]:
                            if eval(f"{company}_selected"):
                                df_company = (
                                    df_region.groupby("Año")[company]
                                    .mean()
                                    .reset_index()
                                )
                                fig_1.add_trace(
                                    go.Scatter(
                                        x=df_company["Año"],
                                        y=df_company[company],
                                        mode="lines",
                                        name=f"{company} - {region}",
                                    )
                                )
                    fig_1.update_layout(
                        title=f"Evolución temporal de {metrica_1}",
                        xaxis_title="Año",
                        yaxis_title="Valor de la Métrica",
                        template="plotly_white",
                    )
                    st.plotly_chart(fig_1, use_container_width=True)

            if i < len(selected_metricas_2):
                with col_graph2:
                    fig_2 = go.Figure()
                    metrica_2 = selected_metricas_2[i]
                    df_metrica_2 = df_metrica_filtrada_temporal[
                        df_metrica_filtrada_temporal["Métrica"] == metrica_2
                    ]
                    for region in region_selected:
                        df_region = df_metrica_2[df_metrica_2["Región"] == region]
                        for company in COMPANIES + ["AVG", "AVG_otros"]:
                            if eval(f"{company}_selected"):
                                df_company = (
                                    df_region.groupby("Año")[company]
                                    .mean()
                                    .reset_index()
                                )
                                fig_2.add_trace(
                                    go.Scatter(
                                        x=df_company["Año"],
                                        y=df_company[company],
                                        mode="lines",
                                        name=f"{company} - {region}",
                                    )
                                )
                    fig_2.update_layout(
                        title=f"Evolución temporal de {metrica_2}",
                        xaxis_title="Año",
                        yaxis_title="Valor de la Métrica",
                        template="plotly_white",
                    )
                    st.plotly_chart(fig_2, use_container_width=True)

    else:
        # Si solo hay métricas en uno de los multiselects, mostrar gráfico y tabla
        metricas_to_plot = selected_metricas_1 or selected_metricas_2
        for metrica in metricas_to_plot:
            df_metrica_filtrada = df_metrica_filtrada_temporal[
                df_metrica_filtrada_temporal["Métrica"] == metrica
            ]

            # Crear las columnas para el gráfico y la tabla antes de generar el contenido
            col_graph, col_table = st.columns(2)

            # Crear gráfico de líneas para las empresas seleccionadas y por región
            with col_graph:
                fig = go.Figure()

                for region in region_selected:
                    df_region = df_metrica_filtrada[
                        df_metrica_filtrada["Región"] == region
                    ]
                    for company in COMPANIES + ["AVG", "AVG_otros"]:
                        if eval(f"{company}_selected"):
                            df_company = (
                                df_region.groupby("Año")[company].mean().reset_index()
                            )
                            fig.add_trace(
                                go.Scatter(
                                    x=df_company["Año"],
                                    y=df_company[company],
                                    mode="lines",
                                    name=f"{company} - {region}",
                                )
                            )

                fig.update_layout(
                    title=f"Evolución temporal de {metrica}",
                    xaxis_title="Año",
                    yaxis_title="Valor de la Métrica",
                    template="plotly_white",
                )

                st.plotly_chart(fig, use_container_width=True)

            # Crear tabla de variación porcentual para cada métrica, empresa y región
            with col_table:
                variacion_data = {
                    "Empresa": [],
                    "Región": [],
                    "Variación %": [],
                }

                for region in region_selected:
                    df_region = df_metrica_filtrada[
                        df_metrica_filtrada["Región"] == region
                    ]
                    for company in COMPANIES + ["AVG", "AVG_otros"]:
                        if eval(f"{company}_selected"):
                            inicio = df_region[df_region["Año"] == start_year][
                                company
                            ].mean()
                            fin = df_region[df_region["Año"] == end_year][
                                company
                            ].mean()
                            variacion_relativa = (
                                (fin - inicio) / inicio if inicio != 0 else None
                            )
                            variacion_data["Empresa"].append(company)
                            variacion_data["Región"].append(region)
                            variacion_data["Variación %"].append(
                                f"{variacion_relativa:.2%}"
                                if variacion_relativa is not None
                                else "N/A"
                            )

                variacion_df = pd.DataFrame(variacion_data)

                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown(
                    f"###### Variación porcentual entre el año {start_year} y el año {end_year}"
                )
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(variacion_df, use_container_width=True)
