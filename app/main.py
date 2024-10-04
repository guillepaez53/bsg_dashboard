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

# Agregar pestañas
tabs = st.tabs(["Inteligencia Competitiva", "IC - Temporal"])

# --- PESTAÑA 1: ANÁLISIS TRANSVERSAL ---
with tabs[0]:
    st.title("BSG Dashboard: Inteligencia Competitiva")

    # Filtros para el análisis transversal
    years = sorted(df_accumulated["Año"].unique(), reverse=True)
    selected_year = st.selectbox("Año", years, index=0, key="year_transversal")
    df_filtrado = df_accumulated[df_accumulated["Año"] == selected_year]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_region = st.selectbox(
            "Región",
            ["Todas"] + list(df_filtrado["Región"].unique()),
            key="region_transversal",
        )

    with col2:
        selected_canal = st.selectbox(
            "Canal",
            ["Todas"] + list(df_filtrado["Canal"].unique()),
            key="canal_transversal",
        )

    with col3:
        if selected_canal == "Todas":
            tipos_disponibles = df_filtrado["Tipo"].unique()
        else:
            tipos_disponibles = df_filtrado[df_filtrado["Canal"] == selected_canal][
                "Tipo"
            ].unique()
        selected_tipo = st.selectbox(
            "Tipo", ["Todas"] + list(tipos_disponibles), key="tipo_transversal"
        )

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
            "Métricas",
            metricas_disponibles,
            default=metricas_disponibles[0],
            key="metricas_transversal",
        )

    # Nuevo dropdown para elegir el tipo de comparación
    tipo_comparacion = st.selectbox(
        "Tipo de Comparación",
        [
            f"Comparar {COMPANY} contra el promedio de la competencia (AVG_otros)",
            "Comparar las 5 empresas",
            f"Comparar {COMPANY} contra el promedio general (AVG)",
        ],
        index=0,
    )

    # Aplicar los filtros según la selección
    if selected_region == "Todas":
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
        ].drop_duplicates(subset=["Métrica", "Región"])
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

            # Ajustar las proporciones de las columnas (2:1 para gráfico:KPI)
            col_graph, col_kpi = st.columns([1.5, 1])

            with col_graph:
                fig = go.Figure()

                if tipo_comparacion == "Comparar las 5 empresas":
                    for _, row in df_metrica.iterrows():
                        y = [row[company] for company in COMPANIES]
                        fig.add_trace(go.Bar(x=COMPANIES, y=y, name=row["Región"]))

                elif (
                    tipo_comparacion
                    == f"Comparar {COMPANY} contra el promedio general (AVG)"
                ):
                    for _, row in df_metrica.iterrows():
                        y = [row[COMPANY], row["AVG"]]
                        fig.add_trace(
                            go.Bar(x=[COMPANY, "AVG"], y=y, name=row["Región"])
                        )

                elif (
                    tipo_comparacion
                    == f"Comparar {COMPANY} contra el promedio de la competencia (AVG_otros)"
                ):
                    for _, row in df_metrica.iterrows():
                        y = [row[COMPANY], row["AVG_otros"]]
                        fig.add_trace(
                            go.Bar(x=[COMPANY, "AVG_otros"], y=y, name=row["Región"])
                        )

                fig.update_layout(
                    barmode="group",
                    title=f"{metrica}",
                    xaxis_title="Empresas",
                    yaxis_title="Valor de la Métrica",
                    template="plotly_white",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_kpi:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"###### Empresa D vs AVG_otros")
                st.markdown("<br>", unsafe_allow_html=True)
                kpi_data = {"Región": [], "Diferencia": [], "Dif. %": []}
                if selected_region == "Todas":
                    for _, row in df_metrica.iterrows():
                        kpi_data["Región"].append(row["Región"])
                        kpi_data["Diferencia"].append(row["diferencia"])
                        kpi_data["Dif. %"].append(f"{row['diferencia_porcentaje']:.2%}")
                else:
                    row = df_metrica.iloc[0]
                    kpi_data["Región"].append(row["Región"])
                    kpi_data["Diferencia"].append(row["diferencia"])
                    kpi_data["Dif. %"].append(f"{row['diferencia_porcentaje']:.2%}")

                kpi_df = pd.DataFrame(kpi_data).reset_index(drop=True)
                st.dataframe(kpi_df.style.hide(axis="index"), use_container_width=True)


# --- PESTAÑA 2: ANÁLISIS TEMPORAL ---
with tabs[1]:
    st.title("BSG Dashboard: Inteligencia Competitiva - Análisis Temporal")

    if df_accumulated["Año"].max() > df_accumulated["Año"].min():
        # Slider para seleccionar el rango de años (Inicio y Fin)
        start_year, end_year = st.slider(
            "Seleccionar el inicio y fin de la evolución a analizar",
            min_value=int(df_accumulated["Año"].min()),
            max_value=int(df_accumulated["Año"].max()),
            value=(int(df_accumulated["Año"].min()), int(df_accumulated["Año"].max())),
            step=1,
        )
    else:
        start_year = df_accumulated["Año"].min()
        end_year = df_accumulated["Año"].max()

    # Filtros de Región, Canal, Tipo
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

    with col1:
        selected_region_temporal = st.selectbox(
            "Región",
            ["Todas"] + list(df_accumulated["Región"].unique()),
            key="region_temporal",
        )

    with col2:
        selected_canal_temporal = st.selectbox(
            "Canal",
            ["Todas"] + list(df_accumulated["Canal"].unique()),
            key="canal_temporal",
        )

    with col3:
        if selected_canal_temporal == "Todas":
            tipos_disponibles_temporal = df_accumulated["Tipo"].unique()
        else:
            tipos_disponibles_temporal = df_accumulated[
                df_accumulated["Canal"] == selected_canal_temporal
            ]["Tipo"].unique()
        selected_tipo_temporal = st.selectbox(
            "Tipo", ["Todas"] + list(tipos_disponibles_temporal), key="tipo_temporal"
        )

    with col4:
        if selected_canal_temporal == "Todas" and selected_tipo_temporal == "Todas":
            metricas_disponibles_temporal = df_accumulated["Métrica"].unique()
        elif selected_canal_temporal == "Todas":
            metricas_disponibles_temporal = df_accumulated[
                df_accumulated["Tipo"] == selected_tipo_temporal
            ]["Métrica"].unique()
        elif selected_tipo_temporal == "Todas":
            metricas_disponibles_temporal = df_accumulated[
                df_accumulated["Canal"] == selected_canal_temporal
            ]["Métrica"].unique()
        else:
            metricas_disponibles_temporal = df_accumulated[
                (df_accumulated["Canal"] == selected_canal_temporal)
                & (df_accumulated["Tipo"] == selected_tipo_temporal)
            ]["Métrica"].unique()

        selected_metricas_temporal = st.multiselect(
            "Métricas",
            metricas_disponibles_temporal,
            default=metricas_disponibles_temporal[:1],
            key="metricas_temporal",
        )

    # Subtítulo para las empresas
    # st.markdown("### Empresas")

    # Checkbox para seleccionar empresas y agregados
    with st.container():
        st.markdown("###### Empresas")
        cols = st.columns(7)
        A_selected = cols[0].checkbox("A", value=False)
        B_selected = cols[1].checkbox("B", value=False)
        C_selected = cols[2].checkbox("C", value=False)
        D_selected = cols[3].checkbox("D", value=True)  # Por defecto seleccionado
        E_selected = cols[4].checkbox("E", value=False)
        AVG_selected = cols[5].checkbox("AVG", value=False)
        AVG_otros_selected = cols[6].checkbox(
            "AVG_otros", value=True
        )  # Por defecto seleccionado

    # Filtrar el dataframe por los años seleccionados y por las métricas
    df_metrica_filtrada_temporal = df_accumulated[
        (df_accumulated["Año"] >= start_year)
        & (df_accumulated["Año"] <= end_year)
        & (df_accumulated["Métrica"].isin(selected_metricas_temporal))
    ]

    # Calcular la variación porcentual
    def calcular_variacion(df, col):
        inicio = df[df["Año"] == start_year][col].mean()
        fin = df[df["Año"] == end_year][col].mean()
        variacion_relativa = (fin - inicio) / inicio
        return f"{variacion_relativa:.2%}" if inicio != 0 else None

    # Crear DataFrame con la variación porcentual para cada métrica y empresa
    for metrica in selected_metricas_temporal:
        # st.markdown(f"### Métrica: {metrica}")
        df_metrica_filtrada = df_metrica_filtrada_temporal[
            df_metrica_filtrada_temporal["Métrica"] == metrica
        ]

        variacion_data = {
            "Empresa": [],
            "Variación %": [],
        }

        if A_selected:
            variacion_data["Empresa"].append("A")
            variacion_data["Variación %"].append(
                calcular_variacion(df_metrica_filtrada, "A")
            )
        if B_selected:
            variacion_data["Empresa"].append("B")
            variacion_data["Variación %"].append(
                calcular_variacion(df_metrica_filtrada, "B")
            )
        if C_selected:
            variacion_data["Empresa"].append("C")
            variacion_data["Variación %"].append(
                calcular_variacion(df_metrica_filtrada, "C")
            )
        if D_selected:
            variacion_data["Empresa"].append("D")
            variacion_data["Variación %"].append(
                calcular_variacion(df_metrica_filtrada, "D")
            )
        if E_selected:
            variacion_data["Empresa"].append("E")
            variacion_data["Variación %"].append(
                calcular_variacion(df_metrica_filtrada, "E")
            )
        if AVG_selected:
            variacion_data["Empresa"].append("AVG")
            variacion_data["Variación %"].append(
                calcular_variacion(df_metrica_filtrada, "AVG")
            )
        if AVG_otros_selected:
            variacion_data["Empresa"].append("AVG_otros")
            variacion_data["Variación %"].append(
                calcular_variacion(df_metrica_filtrada, "AVG_otros")
            )

        variacion_df = pd.DataFrame(variacion_data)

        col_graph, col_table = st.columns([2, 1])

        with col_table:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"###### Variación porcentual")
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(variacion_df, use_container_width=True)

        # Crear gráfico de líneas para las empresas seleccionadas
        fig = go.Figure()

        if A_selected:
            df_A = df_metrica_filtrada.groupby("Año")["A"].mean().reset_index()
            fig.add_trace(
                go.Scatter(x=df_A["Año"], y=df_A["A"], mode="lines", name="A")
            )

        if B_selected:
            df_B = df_metrica_filtrada.groupby("Año")["B"].mean().reset_index()
            fig.add_trace(
                go.Scatter(x=df_B["Año"], y=df_B["B"], mode="lines", name="B")
            )

        if C_selected:
            df_C = df_metrica_filtrada.groupby("Año")["C"].mean().reset_index()
            fig.add_trace(
                go.Scatter(x=df_C["Año"], y=df_C["C"], mode="lines", name="C")
            )

        if D_selected:
            df_D = df_metrica_filtrada.groupby("Año")["D"].mean().reset_index()
            fig.add_trace(
                go.Scatter(x=df_D["Año"], y=df_D["D"], mode="lines", name="D")
            )

        if E_selected:
            df_E = df_metrica_filtrada.groupby("Año")["E"].mean().reset_index()
            fig.add_trace(
                go.Scatter(x=df_E["Año"], y=df_E["E"], mode="lines", name="E")
            )

        if AVG_selected:
            df_AVG = df_metrica_filtrada.groupby("Año")["AVG"].mean().reset_index()
            fig.add_trace(
                go.Scatter(x=df_AVG["Año"], y=df_AVG["AVG"], mode="lines", name="AVG")
            )

        if AVG_otros_selected:
            df_AVG_otros = (
                df_metrica_filtrada.groupby("Año")["AVG_otros"].mean().reset_index()
            )
            fig.add_trace(
                go.Scatter(
                    x=df_AVG_otros["Año"],
                    y=df_AVG_otros["AVG_otros"],
                    mode="lines",
                    name="AVG_otros",
                )
            )

        fig.update_layout(
            title=f"Evolución temporal de{metrica}",
            xaxis_title="Año",
            yaxis_title="Valor de la Métrica",
            template="plotly_white",
        )

        with col_graph:
            st.plotly_chart(fig, use_container_width=True)
