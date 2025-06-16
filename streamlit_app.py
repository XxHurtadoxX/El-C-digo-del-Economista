import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --------------------
# CONFIGURACIÓN GENERAL
# --------------------
st.set_page_config(
    page_title="Dashboard Financiero",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------
# FUNCIONES AUXILIARES
# --------------------
def generar_datos_falsos():
    """Genera un DataFrame con datos financieros ficticios"""
    fechas = pd.date_range(start="2024-01-01", periods=12, freq='M')
    ingresos = np.random.randint(5000, 15000, size=12)
    egresos = np.random.randint(3000, 12000, size=12)
    df = pd.DataFrame({
        "Fecha": fechas,
        "Ingresos": ingresos,
        "Egresos": egresos,
    })
    df["Utilidad"] = df["Ingresos"] - df["Egresos"]
    return df


def aplicar_estilo_css(tema):
    """Inyecta CSS personalizado según el tema seleccionado"""
    if tema == "Oscuro":
        css = """
        <style>
            body {background-color: #111111; color: white;}
            .stApp {background-color: #111111; color: white;}
            .css-18e3th9 {background-color: #111111; color: white;}
            .css-1d391kg {background-color: #111111; color: white;}
            .css-1v3fvcr {color: white;}
            .stButton>button {
                background-color: #222222;
                color: white;
                border-radius: 8px;
            }
        </style>
        """
    else:
        css = """
        <style>
            body {background-color: white; color: black;}
            .stApp {background-color: white; color: black;}
            .css-18e3th9 {background-color: white; color: black;}
            .css-1d391kg {background-color: white; color: black;}
            .css-1v3fvcr {color: black;}
            .stButton>button {
                background-color: #eeeeee;
                color: black;
                border-radius: 8px;
            }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# --------------------
# SIDEBAR - CONTROL DE TEMA Y FILTROS
# --------------------
st.sidebar.title("⚙️ Configuración")
tema = st.sidebar.radio("Tema visual", ["Claro", "Oscuro"])
aplicar_estilo_css(tema)

# --------------------
# MAIN - TÍTULO Y DATOS
# --------------------
st.title("📊 Dashboard Financiero Básico")

# Obtener datos simulados
df = generar_datos_falsos()

# Mostrar métricas principales en tres columnas
col1, col2, col3 = st.columns(3)
col1.metric("Ingresos totales", f"${df['Ingresos'].sum():,.0f}")
col2.metric("Egresos totales", f"${df['Egresos'].sum():,.0f}")
col3.metric("Utilidad neta", f"${df['Utilidad'].sum():,.0f}")

st.markdown("---")

# --------------------
# GRÁFICOS
# --------------------

# Gráfico de ingresos vs egresos
fig = px.line(df, x="Fecha", y=["Ingresos", "Egresos"],
              title="Ingresos y Egresos Mensuales",
              markers=True)
fig.update_layout(template="plotly_dark" if tema == "Oscuro" else "plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Gráfico de utilidad
fig2 = px.bar(df, x="Fecha", y="Utilidad", color="Utilidad",
              title="Utilidad Mensual",
              color_continuous_scale="Greys")
fig2.update_layout(template="plotly_dark" if tema == "Oscuro" else "plotly_white")
st.plotly_chart(fig2, use_container_width=True)

# Mostrar tabla completa de datos
st.markdown("### 📋 Detalle de datos")
st.dataframe(df.style.format("${:,.0f}"))

