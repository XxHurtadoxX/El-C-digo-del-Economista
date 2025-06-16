import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --------------------
# CONFIGURACIÓN GENERAL
# --------------------
st.set_page_config(
    page_title="Dashboard Financiero",
    layout="wide",
    initial_sidebar_state="collapsed"  # Cambiado de "expanded" a "collapsed"
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
            body {background-color: #000000; color: white;}
            .stApp {background-color: #000000; color: white;}
            .css-18e3th9 {background-color: #000000; color: white;}
            .css-1d391kg {background-color: #000000; color: white;}
            .css-1v3fvcr {color: white;}
            .stButton>button {
                background-color: #333333;
                color: white;
                border-radius: 8px;
            }
            /* Estilos para métricas */
            .metric-container {
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                border: 1px solid #444444;
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
            }
            .metric-title {
                color: #ffffff;
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 5px;
            }
            .metric-value {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
        """
    else:
        css = """
        <style>
            body {background-color: #ffffff; color: black;}
            .stApp {background-color: #ffffff; color: black;}
            .css-18e3th9 {background-color: #ffffff; color: black;}
            .css-1d391kg {background-color: #ffffff; color: black;}
            .css-1v3fvcr {color: black;}
            .stButton>button {
                background-color: #f0f0f0;
                color: black;
                border-radius: 8px;
            }
            /* Estilos para métricas */
            .metric-container {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .metric-title {
                color: #000000;
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 5px;
            }
            .metric-value {
                color: #000000;
                font-size: 24px;
                font-weight: bold;
            }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

def crear_grafico_lineas(df, tema):
    """Crea un gráfico de líneas con estilos diferenciados"""
    fig = go.Figure()
    
    # Colores según el tema - solo blanco y negro con degradados
    if tema == "Oscuro":
        color_ingresos = "#ffffff"  # Blanco
        color_egresos = "#888888"   # Gris medio
        bg_color = "#000000"
        text_color = "#ffffff"
        grid_color = "#333333"
    else:
        color_ingresos = "#000000"  # Negro
        color_egresos = "#666666"   # Gris oscuro
        bg_color = "#ffffff"
        text_color = "#000000"
        grid_color = "#cccccc"
    
    # Línea sólida para Ingresos
    fig.add_trace(go.Scatter(
        x=df["Fecha"],
        y=df["Ingresos"],
        mode='lines+markers',
        name='Ingresos',
        line=dict(color=color_ingresos, width=3),
        marker=dict(size=8)
    ))
    
    # Línea punteada para Egresos
    fig.add_trace(go.Scatter(
        x=df["Fecha"],
        y=df["Egresos"],
        mode='lines+markers',
        name='Egresos',
        line=dict(color=color_egresos, width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="Ingresos y Egresos Mensuales",
        title_font_color=text_color,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font_color=text_color,
        xaxis=dict(gridcolor=grid_color, title="Fecha"),
        yaxis=dict(gridcolor=grid_color, title="Monto")
    )
    
    return fig

def crear_grafico_barras(df, tema):
    """Crea un gráfico de barras con colores según el tema"""
    if tema == "Oscuro":
        color_positivo = "#ffffff"
        color_negativo = "#666666"
        bg_color = "#000000"
        text_color = "#ffffff"
        grid_color = "#333333"
    else:
        color_positivo = "#000000"
        color_negativo = "#888888"
        bg_color = "#ffffff"
        text_color = "#000000"
        grid_color = "#cccccc"
    
    # Crear colores condicionalmente
    colors = [color_positivo if x >= 0 else color_negativo for x in df["Utilidad"]]
    
    fig = go.Figure(data=[
        go.Bar(
            x=df["Fecha"],
            y=df["Utilidad"],
            marker_color=colors,
            name="Utilidad"
        )
    ])
    
    fig.update_layout(
        title="Utilidad Mensual",
        title_font_color=text_color,
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font_color=text_color,
        xaxis=dict(gridcolor=grid_color, title="Fecha"),
        yaxis=dict(gridcolor=grid_color, title="Utilidad")
    )
    
    return fig

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

# Mostrar métricas principales en tres columnas con cajitas y emojis
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">💰 Ingresos totales</div>
        <div class="metric-value">${df['Ingresos'].sum():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">💸 Egresos totales</div>
        <div class="metric-value">${df['Egresos'].sum():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    utilidad_total = df['Utilidad'].sum()
    emoji_utilidad = "📈" if utilidad_total >= 0 else "📉"
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">{emoji_utilidad} Utilidad neta</div>
        <div class="metric-value">${utilidad_total:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --------------------
# GRÁFICOS
# --------------------

# Gráfico de ingresos vs egresos con líneas diferenciadas
fig = crear_grafico_lineas(df, tema)
st.plotly_chart(fig, use_container_width=True)

# Gráfico de utilidad con colores según el tema
fig2 = crear_grafico_barras(df, tema)
st.plotly_chart(fig2, use_container_width=True)

# Mostrar tabla completa de datos con formato japonés para fechas
st.markdown("### 📋 Detalle de datos")

# Formatear el DataFrame para mostrar
df_display = df.copy()
df_display["Fecha"] = df_display["Fecha"].dt.strftime("%Y/%m/%d")  # Formato japonés

# Aplicar formato solo a las columnas numéricas
df_styled = df_display.style.format({
    "Ingresos": "${:,.0f}",
    "Egresos": "${:,.0f}", 
    "Utilidad": "${:,.0f}"
})

st.dataframe(df_styled)