import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import os
import sys
import plotly.colors as pc

# Configuración de la página para usar todo el ancho
st.set_page_config(layout="wide", page_title="BSG Dashboard", page_icon="🟠")

# Obtener la ruta del directorio actual donde se encuentra el script
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from config.constants import DATA_ACCUMULATED_CI_DIR, COMPANY, COMPANIES


# Cargar los datos
def cargar_datos():
    df = pd.read_csv(os.path.join(DATA_ACCUMULATED_CI_DIR, "ci_acumulado.csv"))
    df["AVG"] = pd.to_numeric(df["AVG"], errors="coerce").fillna(0)
    df["AVG_otros"] = pd.to_numeric(df["AVG_otros"], errors="coerce").fillna(0)
    # df["diferencia_porcentaje"] = df["diferencia_porcentaje"] * 100
    return df


df_accumulated = cargar_datos()

# Definir colores consistentes para cada empresa
base_colors = {
    "A": "#9467bd",
    "B": "#ff7f0e",
    "C": "#e377c2",
    "D": "#d62728",
    "E": "#1f77b4",
    "AVG": "#8c564b",
    "AVG_otros": "#2ca02c",
}

# Definir tipos de línea para cada región
line_styles = ["solid", "dot", "dash", "longdash", "dashdot"]

# Crear un mapeo de estilo de línea para cada región
line_style_mapping = {
    region: line_styles[i % len(line_styles)]
    for i, region in enumerate(df_accumulated["Región"].unique())
}

# --- PESTAÑA UNIFICADA: ANÁLISIS IC ---

st.title("BSG Dashboard: Inteligencia Competitiva")

st.markdown("<br>", unsafe_allow_html=True)

# Crear barra lateral
with st.sidebar:

    # Slider para seleccionar el rango de años (Inicio y Fin)
    if "start_year" not in st.session_state or "end_year" not in st.session_state:
        st.session_state.start_year = int(df_accumulated["Año"].min())
        st.session_state.end_year = int(df_accumulated["Año"].max())

    if df_accumulated["Año"].max() > df_accumulated["Año"].min():
        start_year, end_year = st.slider(
            "Seleccione un año para gráficos de barras, o un rango de años para gráficos de líneas",
            min_value=int(df_accumulated["Año"].min()),
            max_value=int(df_accumulated["Año"].max()),
            value=(
                st.session_state.start_year,
                st.session_state.end_year,
            ),
            step=1,
            key="slider_temporal",
        )
        st.session_state.start_year = start_year
        st.session_state.end_year = end_year

    # Checkboxes para las Regiones
    st.markdown("###### Filtrar Regiones")
    regiones = df_accumulated["Región"].unique()
    if "region_selected" not in st.session_state:
        st.session_state.region_selected = regiones.tolist()

    for region in regiones:
        if st.checkbox(
            region,
            value=region in st.session_state.region_selected,
            key=f"region_temporal_{region}",
        ):
            if region not in st.session_state.region_selected:
                st.session_state.region_selected.append(region)
        else:
            if region in st.session_state.region_selected:
                st.session_state.region_selected.remove(region)

    # Checkbox para seleccionar empresas y agregados
    st.markdown("###### Filtrar Empresas")
    st.session_state.A_selected = st.checkbox(
        "A", value=st.session_state.get("A_selected", False)
    )
    st.session_state.B_selected = st.checkbox(
        "B", value=st.session_state.get("B_selected", False)
    )
    st.session_state.C_selected = st.checkbox(
        "C", value=st.session_state.get("C_selected", False)
    )
    st.session_state.D_selected = st.checkbox(
        "D", value=st.session_state.get("D_selected", True)
    )  # Por defecto seleccionado
    st.session_state.E_selected = st.checkbox(
        "E", value=st.session_state.get("E_selected", False)
    )
    st.session_state.AVG_otros_selected = st.checkbox(
        "AVG_otros", value=st.session_state.get("AVG_otros_selected", True)
    )  # Por defecto seleccionado
    st.session_state.AVG_selected = st.checkbox(
        "AVG", value=st.session_state.get("AVG_selected", False)
    )

    # Checkboxes de Canal y Tipo
    st.markdown("###### Filtrar Métricas disponibles por Canal")
    canales_disponibles = df_accumulated["Canal"].unique()
    if "canal_selected" not in st.session_state:
        st.session_state.canal_selected = canales_disponibles.tolist()

    for canal in canales_disponibles:
        if st.checkbox(
            canal,
            value=canal in st.session_state.canal_selected,
            key=f"canal_temporal_{canal}",
        ):
            if canal not in st.session_state.canal_selected:
                st.session_state.canal_selected.append(canal)
        else:
            if canal in st.session_state.canal_selected:
                st.session_state.canal_selected.remove(canal)

    st.markdown("###### Filtrar Métricas disponibles por Tipo")
    tipos_disponibles = df_accumulated["Tipo"].unique()
    if "tipo_selected" not in st.session_state:
        st.session_state.tipo_selected = tipos_disponibles.tolist()

    for tipo in tipos_disponibles:
        if st.checkbox(
            tipo,
            value=tipo in st.session_state.tipo_selected,
            key=f"tipo_temporal_{tipo}",
        ):
            if tipo not in st.session_state.tipo_selected:
                st.session_state.tipo_selected.append(tipo)
        else:
            if tipo in st.session_state.tipo_selected:
                st.session_state.tipo_selected.remove(tipo)

# Filtrar las métricas disponibles según el canal y tipo seleccionados
metricas_disponibles_temporal = df_accumulated[
    (df_accumulated["Canal"].isin(st.session_state.canal_selected))
    & (df_accumulated["Tipo"].isin(st.session_state.tipo_selected))
]["Métrica"].unique()

# Agregar estilos CSS para los multiselect
st.markdown(
    """
    <style>
        div[data-baseweb="select"] {
            border: 2px solid #A50034 !important; /* Borde de color rojo similar al tema UBP */
            border-radius: 4px; /* Bordes redondeados */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

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
    (df_accumulated["Año"] >= st.session_state.start_year)
    & (df_accumulated["Año"] <= st.session_state.end_year)
    & (
        df_accumulated["Región"].isin(st.session_state.region_selected)
    )  # Filtro por regiones
]

# Verificar si es un análisis transversal o temporal
is_transversal = st.session_state.start_year == st.session_state.end_year

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
                    for region in st.session_state.region_selected:
                        df_region = df_metrica_1[df_metrica_1["Región"] == region]
                        for company in COMPANIES + ["AVG", "AVG_otros"]:
                            if st.session_state.get(f"{company}_selected"):
                                fig_1.add_trace(
                                    go.Bar(
                                        x=[region],
                                        y=[df_region[company].mean()],
                                        name=f"{company} - {region}",
                                        marker_color=base_colors[company],
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
                    for region in st.session_state.region_selected:
                        df_region = df_metrica_2[df_metrica_2["Región"] == region]
                        for company in COMPANIES + ["AVG", "AVG_otros"]:
                            if st.session_state.get(f"{company}_selected"):
                                fig_2.add_trace(
                                    go.Bar(
                                        x=[region],
                                        y=[df_region[company].mean()],
                                        name=f"{company} - {region}",
                                        marker_color=base_colors[company],
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
                for region in st.session_state.region_selected:
                    df_region = df_metrica[df_metrica["Región"] == region]
                    for company in COMPANIES + ["AVG", "AVG_otros"]:
                        if st.session_state.get(f"{company}_selected"):
                            fig.add_trace(
                                go.Bar(
                                    x=[region],
                                    y=[df_region[company].mean()],
                                    name=f"{company} - {region}",
                                    marker_color=base_colors[company],
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
                    for region in st.session_state.region_selected:
                        df_region = df_metrica_1[df_metrica_1["Región"] == region]
                        for company in COMPANIES + ["AVG", "AVG_otros"]:
                            if st.session_state.get(f"{company}_selected"):
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
                                        line=dict(
                                            color=base_colors[company],
                                            dash=line_style_mapping[region],
                                        ),
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
                    for region in st.session_state.region_selected:
                        df_region = df_metrica_2[df_metrica_2["Región"] == region]
                        for company in COMPANIES + ["AVG", "AVG_otros"]:
                            if st.session_state.get(f"{company}_selected"):
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
                                        line=dict(
                                            color=base_colors[company],
                                            dash=line_style_mapping[region],
                                        ),
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

                for region in st.session_state.region_selected:
                    df_region = df_metrica_filtrada[
                        df_metrica_filtrada["Región"] == region
                    ]
                    for company in COMPANIES + ["AVG", "AVG_otros"]:

                        if st.session_state.get(f"{company}_selected", True):
                            df_company = (
                                df_region.groupby("Año")[company].mean().reset_index()
                            )
                            fig.add_trace(
                                go.Scatter(
                                    x=df_company["Año"],
                                    y=df_company[company],
                                    mode="lines",
                                    name=f"{company} - {region}",
                                    line=dict(
                                        color=base_colors[company],
                                        dash=line_style_mapping[region],
                                    ),
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

                for region in st.session_state.region_selected:
                    df_region = df_metrica_filtrada[
                        df_metrica_filtrada["Región"] == region
                    ]
                    for company in COMPANIES + ["AVG", "AVG_otros"]:
                        if st.session_state.get(f"{company}_selected", True):
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
