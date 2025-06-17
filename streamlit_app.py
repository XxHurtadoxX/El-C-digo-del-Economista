import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime, timedelta

# --------------------
# CONFIGURACIÓN GENERAL
# --------------------
st.set_page_config(
    page_title="Dashboard Financiero V2",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------
# FUNCIONES AUXILIARES
# --------------------
def generar_datos_falsos(meses=12, año=2024):
    """Genera un DataFrame con datos financieros ficticios"""
    fechas = pd.date_range(start=f"{año}-01-01", periods=meses, freq='M')
    
    # Añadir más categorías y variabilidad
    categorias = ['Ventas', 'Servicios', 'Consultoría', 'Productos']
    departamentos = ['Marketing', 'Operaciones', 'RRHH', 'IT', 'Administración']
    
    data = []
    for fecha in fechas:
        for categoria in categorias:
            ingreso = np.random.randint(2000, 8000)
            egreso = np.random.randint(1000, 6000)
            data.append({
                'Fecha': fecha,
                'Categoria': categoria,
                'Departamento': np.random.choice(departamentos),
                'Ingresos': ingreso,
                'Egresos': egreso,
                'Utilidad': ingreso - egreso,
                'Region': np.random.choice(['Norte', 'Sur', 'Centro', 'Oriente'])
            })
    
    return pd.DataFrame(data)

def procesar_archivo_csv(uploaded_file):
    """Procesa archivo CSV subido por el usuario"""
    try:
        # Leer el archivo
        df = pd.read_csv(uploaded_file)
        
        # Intentar detectar columnas de fecha
        date_columns = df.select_dtypes(include=['object']).columns
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col])
                break  # Usar la primera columna que se pueda convertir
            except:
                continue
        
        return df, None
    except Exception as e:
        return None, str(e)

def aplicar_estilo_css(tema):
    """Inyecta CSS personalizado según el tema seleccionado con colores elegantes para todos los widgets"""
    if tema == "Oscuro":
        css = """
        <style>
            /* === CONFIGURACIÓN BASE === */
            body {background-color: #000000; color: white;}
            .stApp {background-color: #000000; color: white;}
            .main .block-container {color: #ffffff;}
            
            /* === MÉTRICAS PERSONALIZADAS === */
            .metric-container {
                background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 50%, #1f1f1f 100%);
                border: 1px solid #404040;
                border-radius: 12px;
                padding: 24px;
                margin: 10px 0;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(255, 255, 255, 0.05);
                transition: all 0.3s ease;
            }
            .metric-container:hover {
                box-shadow: 0 12px 24px rgba(0, 0, 0, 0.5), 0 4px 8px rgba(255, 255, 255, 0.08);
                transform: translateY(-2px);
            }
            .metric-title {
                color: #e0e0e0;
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 8px;
                letter-spacing: 0.5px;
            }
            .metric-value {
                color: #ffffff;
                font-size: 28px;
                font-weight: 700;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            }
            
            /* === CONTENEDOR DE UPLOAD === */
            .upload-container {
                background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 50%, #1f1f1f 100%);
                border: 2px dashed #505050;
                border-radius: 12px;
                padding: 32px;
                text-align: center;
                margin: 20px 0;
                transition: border-color 0.3s ease;
            }
            .upload-container:hover {
                border-color: #707070;
            }
            
            /* === PESTAÑAS (TABS) === */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: transparent;
            }
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                background-color: #2a2a2a;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 0 16px;
                color: #ffffff !important;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #3a3a3a;
                color: #ffffff !important;
                border-color: #606060;
            }
            .stTabs [aria-selected="true"] {
                background-color: #ff4b4b !important;
                color: #ffffff !important;
                border-color: #ff4b4b !important;
            }
            
            /* === TEXT INPUT === */
            .stTextInput > div > div > input {
                color: #ffffff !important;
                background-color: #2a2a2a !important;
                border: 1px solid #404040 !important;
                border-radius: 8px;
            }
            .stTextInput > div > div > input:focus {
                border-color: #ff4b4b !important;
                box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2) !important;
            }
            .stTextInput > div > div > input::placeholder {
                color: #888888 !important;
                opacity: 1;
            }
            
            /* === TEXT AREA === */
            .stTextArea > div > div > textarea {
                color: #ffffff !important;
                background-color: #2a2a2a !important;
                border: 1px solid #404040 !important;
                border-radius: 8px;
            }
            .stTextArea > div > div > textarea:focus {
                border-color: #ff4b4b !important;
                box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2) !important;
            }
            .stTextArea > div > div > textarea::placeholder {
                color: #888888 !important;
                opacity: 1;
            }
            
            /* === SELECTBOX === */
            .stSelectbox > div > div > div {
                background-color: #2a2a2a !important;
                border: 1px solid #404040 !important;
                color: #ffffff !important;
            }
            .stSelectbox > div > div > div:focus-within {
                border-color: #ff4b4b !important;
                box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2) !important;
            }
            
            /* === MULTISELECT === */
            .stMultiSelect > div > div > div {
                background-color: #2a2a2a !important;
                border: 1px solid #404040 !important;
            }
            .stMultiSelect > div > div > div > div {
                color: #ffffff !important;
            }
            
            /* === SLIDERS === */
            .stSlider > div > div > div > div {
                background-color: #404040;
            }
            .stSlider > div > div > div > div > div {
                background-color: #ff4b4b;
            }
            .stSlider > div > div > div > div > div > div {
                background-color: #ff4b4b;
                border: 2px solid #ffffff;
            }
            
            /* === SELECT SLIDER === */
            .stSelectSlider > div > div > div {
                color: #ffffff !important;
                background-color: #2a2a2a;
                border: 1px solid #404040;
            }
            .stSelectSlider > div > div > div > div {
                background-color: #ff4b4b !important;
                color: #ffffff !important;
            }
            
            /* === BOTONES === */
            .stButton > button {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                background-color: #3a3a3a;
                border-color: #606060;
                transform: translateY(-1px);
            }
            .stButton > button[kind="primary"] {
                background-color: #ff4b4b;
                border-color: #ff4b4b;
            }
            .stButton > button[kind="primary"]:hover {
                background-color: #ff3333;
                border-color: #ff3333;
            }
            
            /* === CHECKBOX === */
            .stCheckbox > label {
                color: #ffffff !important;
            }
            .stCheckbox > label > div {
                background-color: #2a2a2a;
                border: 1px solid #404040;
            }
            
            /* === RADIO === */
            .stRadio > label {
                color: #ffffff !important;
            }
            .stRadio > div > label {
                color: #ffffff !important;
            }
            
            /* === TOGGLE === */
            .stToggle > label {
                color: #ffffff !important;
            }
            
            /* === DATE INPUT === */
            .stDateInput > div > div > input {
                background-color: #2a2a2a !important;
                color: #ffffff !important;
                border: 1px solid #404040 !important;
            }
            
            /* === TIME INPUT === */
            .stTimeInput > div > div > input {
                background-color: #2a2a2a !important;
                color: #ffffff !important;
                border: 1px solid #404040 !important;
            }
            
            /* === NUMBER INPUT === */
            .stNumberInput > div > div > input {
                background-color: #2a2a2a !important;
                color: #ffffff !important;
                border: 1px solid #404040 !important;
            }
            
            /* === COLOR PICKER === */
            .stColorPicker > div > div > input {
                background-color: #2a2a2a !important;
                border: 1px solid #404040 !important;
            }
            
            /* === LABELS GENERALES === */
            .stTextInput > label,
            .stTextArea > label,
            .stSelectbox > label,
            .stMultiSelect > label,
            .stSlider > label,
            .stSelectSlider > label,
            .stDateInput > label,
            .stTimeInput > label,
            .stNumberInput > label,
            .stColorPicker > label {
                color: #ffffff !important;
                font-weight: 500 !important;
            }
            
            /* === SIDEBAR === */
            .css-1d391kg {
                background-color: #1a1a1a;
            }
            .sidebar .sidebar-content {
                background-color: #1a1a1a;
            }
            
            /* === DATAFRAME === */
            .stDataFrame {
                background-color: #2a2a2a;
            }
            
            /* === MÉTRICAS DE STREAMLIT === */
            .metric-container .metric-value {
                color: #ffffff;
            }
            .metric-container .metric-delta {
                color: #00ff00;
            }
            
            /* === ALERTAS === */
            .stAlert {
                background-color: #2a2a2a;
                border: 1px solid #404040;
                color: #ffffff;
            }
            
            /* === EXPANDER === */
            .streamlit-expanderHeader {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            .streamlit-expanderContent {
                background-color: #1a1a1a;
                border: 1px solid #404040;
            }
        </style>
        """
    else:
        css = """
        <style>
            /* === CONFIGURACIÓN BASE === */
            body {background-color: #ffffff; color: black;}
            .stApp {background-color: #ffffff; color: black;}
            .main .block-container {color: #262730;}
            
            /* === MÉTRICAS PERSONALIZADAS === */
            .metric-container {
                background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 50%, #f5f5f5 100%);
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                padding: 24px;
                margin: 10px 0;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(0, 0, 0, 0.04);
                transition: all 0.3s ease;
            }
            .metric-container:hover {
                box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12), 0 4px 8px rgba(0, 0, 0, 0.06);
                transform: translateY(-2px);
            }
            .metric-title {
                color: #4a4a4a;
                font-size: 14px;
                font-weight: 500;
                margin-bottom: 8px;
                letter-spacing: 0.5px;
            }
            .metric-value {
                color: #1a1a1a;
                font-size: 28px;
                font-weight: 700;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            }
            
            /* === CONTENEDOR DE UPLOAD === */
            .upload-container {
                background: linear-gradient(135deg, #ffffff 0%, #f8f8f8 50%, #f5f5f5 100%);
                border: 2px dashed #c0c0c0;
                border-radius: 12px;
                padding: 32px;
                text-align: center;
                margin: 20px 0;
                transition: border-color 0.3s ease;
            }
            .upload-container:hover {
                border-color: #a0a0a0;
            }
            
            /* === PESTAÑAS (TABS) === */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: transparent;
            }
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                background-color: #f0f2f6;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 16px;
                color: #262730 !important;
                font-weight: 500;
                transition: all 0.3s ease;
            }
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #e6e9ef;
                color: #000000 !important;
                border-color: #9ca3af;
            }
            .stTabs [aria-selected="true"] {
                background-color: #ff4b4b !important;
                color: #ffffff !important;
                border-color: #ff4b4b !important;
            }
            
            /* === TEXT INPUT === */
            .stTextInput > div > div > input {
                color: #262730 !important;
                background-color: #ffffff !important;
                border: 1px solid #d1d5db !important;
                border-radius: 8px;
            }
            .stTextInput > div > div > input:focus {
                border-color: #ff4b4b !important;
                box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2) !important;
            }
            .stTextInput > div > div > input::placeholder {
                color: #6b7280 !important;
                opacity: 1;
            }
            
            /* === TEXT AREA === */
            .stTextArea > div > div > textarea {
                color: #262730 !important;
                background-color: #ffffff !important;
                border: 1px solid #d1d5db !important;
                border-radius: 8px;
            }
            .stTextArea > div > div > textarea:focus {
                border-color: #ff4b4b !important;
                box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2) !important;
            }
            .stTextArea > div > div > textarea::placeholder {
                color: #6b7280 !important;
                opacity: 1;
            }
            
            /* === SELECTBOX === */
            .stSelectbox > div > div > div {
                background-color: #ffffff !important;
                border: 1px solid #d1d5db !important;
                color: #262730 !important;
            }
            .stSelectbox > div > div > div:focus-within {
                border-color: #ff4b4b !important;
                box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2) !important;
            }
            
            /* === MULTISELECT === */
            .stMultiSelect > div > div > div {
                background-color: #ffffff !important;
                border: 1px solid #d1d5db !important;
            }
            .stMultiSelect > div > div > div > div {
                color: #262730 !important;
            }
            
            /* === SLIDERS === */
            .stSlider > div > div > div > div {
                background-color: #d1d5db;
            }
            .stSlider > div > div > div > div > div {
                background-color: #ff4b4b;
            }
            .stSlider > div > div > div > div > div > div {
                background-color: #ff4b4b;
                border: 2px solid #ffffff;
            }
            
            /* === SELECT SLIDER === */
            .stSelectSlider > div > div > div {
                color: #262730 !important;
                background-color: #f9fafb;
                border: 1px solid #d1d5db;
            }
            .stSelectSlider > div > div > div > div {
                background-color: #ff4b4b !important;
                color: #ffffff !important;
            }
            
            /* === BOTONES === */
            .stButton > button {
                background-color: #ffffff;
                color: #262730;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                background-color: #f9fafb;
                border-color: #9ca3af;
                transform: translateY(-1px);
            }
            .stButton > button[kind="primary"] {
                background-color: #ff4b4b;
                border-color: #ff4b4b;
                color: #ffffff;
            }
            .stButton > button[kind="primary"]:hover {
                background-color: #ff3333;
                border-color: #ff3333;
            }
            
            /* === CHECKBOX === */
            .stCheckbox > label {
                color: #262730 !important;
            }
            .stCheckbox > label > div {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
            }
            
            /* === RADIO === */
            .stRadio > label {
                color: #262730 !important;
            }
            .stRadio > div > label {
                color: #262730 !important;
            }
            
            /* === TOGGLE === */
            .stToggle > label {
                color: #262730 !important;
            }
            
            /* === DATE INPUT === */
            .stDateInput > div > div > input {
                background-color: #ffffff !important;
                color: #262730 !important;
                border: 1px solid #d1d5db !important;
            }
            
            /* === TIME INPUT === */
            .stTimeInput > div > div > input {
                background-color: #ffffff !important;
                color: #262730 !important;
                border: 1px solid #d1d5db !important;
            }
            
            /* === NUMBER INPUT === */
            .stNumberInput > div > div > input {
                background-color: #ffffff !important;
                color: #262730 !important;
                border: 1px solid #d1d5db !important;
            }
            
            /* === COLOR PICKER === */
            .stColorPicker > div > div > input {
                background-color: #ffffff !important;
                border: 1px solid #d1d5db !important;
            }
            
            /* === LABELS GENERALES === */
            .stTextInput > label,
            .stTextArea > label,
            .stSelectbox > label,
            .stMultiSelect > label,
            .stSlider > label,
            .stSelectSlider > label,
            .stDateInput > label,
            .stTimeInput > label,
            .stNumberInput > label,
            .stColorPicker > label {
                color: #262730 !important;
                font-weight: 500 !important;
            }
            
            /* === SIDEBAR === */
            .css-1d391kg {
                background-color: #f8f9fa;
            }
            .sidebar .sidebar-content {
                background-color: #f8f9fa;
            }
            
            /* === DATAFRAME === */
            .stDataFrame {
                background-color: #ffffff;
            }
            
            /* === MÉTRICAS DE STREAMLIT === */
            .metric-container .metric-value {
                color: #262730;
            }
            .metric-container .metric-delta {
                color: #059669;
            }
            
            /* === ALERTAS === */
            .stAlert {
                background-color: #f8f9fa;
                border: 1px solid #d1d5db;
                color: #262730;
            }
            
            /* === EXPANDER === */
            .streamlit-expanderHeader {
                background-color: #f8f9fa;
                color: #262730;
            }
            .streamlit-expanderContent {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
            }
        </style>
        """
    
    st.markdown(css, unsafe_allow_html=True)

def crear_grafico_lineas(df, tema, categorias_seleccionadas):
    """Crea un gráfico de líneas con colores elegantes en escala de grises"""
    # Filtrar por categorías seleccionadas
    df_filtrado = df[df['Categoria'].isin(categorias_seleccionadas)]
    
    # Agrupar por fecha
    df_agrupado = df_filtrado.groupby('Fecha').agg({
        'Ingresos': 'sum',
        'Egresos': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    # Colores elegantes según el tema
    if tema == "Oscuro":
        color_ingresos = "#ffffff"  # Blanco puro para ingresos
        color_egresos = "#808080"   # Gris medio para egresos
        bg_color = "#0a0a0a"
        text_color = "#e0e0e0"
        grid_color = "#2a2a2a"
    else:
        color_ingresos = "#1a1a1a"  # Negro para ingresos
        color_egresos = "#666666"   # Gris oscuro para egresos
        bg_color = "#fafafa"
        text_color = "#2a2a2a"
        grid_color = "#e0e0e0"
    
    # Línea sólida para Ingresos con gradiente
    fig.add_trace(go.Scatter(
        x=df_agrupado["Fecha"],
        y=df_agrupado["Ingresos"],
        mode='lines+markers',
        name='Ingresos',
        line=dict(color=color_ingresos, width=4),
        marker=dict(size=10, color=color_ingresos, line=dict(width=2, color=bg_color)),
        fill='tonexty' if tema == "Oscuro" else None,
        fillcolor='rgba(255, 255, 255, 0.1)' if tema == "Oscuro" else 'rgba(26, 26, 26, 0.1)'
    ))
    
    # Línea para Egresos
    fig.add_trace(go.Scatter(
        x=df_agrupado["Fecha"],
        y=df_agrupado["Egresos"],
        mode='lines+markers',
        name='Egresos',
        line=dict(color=color_egresos, width=4, dash='dot'),
        marker=dict(size=10, color=color_egresos, line=dict(width=2, color=bg_color))
    ))
    
    fig.update_layout(
        title=dict(
            text="Ingresos y Egresos por Período",
            font=dict(color=text_color, size=20, family="Arial Black")
        ),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=text_color, family="Arial"),
        height=450,
        xaxis=dict(
            gridcolor=grid_color, 
            title="Fecha", 
            tickcolor=text_color, 
            linecolor=text_color,
            title_font_color=text_color,
            tickfont_color=text_color
        ),
        yaxis=dict(
            gridcolor=grid_color, 
            title="Monto", 
            tickcolor=text_color, 
            linecolor=text_color,
            title_font_color=text_color,
            tickfont_color=text_color
        ),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor=grid_color,
            borderwidth=1,
            font=dict(color=text_color)
        )
    )
    
    return fig

def crear_grafico_barras_categorias(df, tema, categorias_seleccionadas):
    """Crea un gráfico de barras por categorías con degradados elegantes"""
    # Filtrar y agrupar por categoría
    df_filtrado = df[df['Categoria'].isin(categorias_seleccionadas)]
    df_agrupado = df_filtrado.groupby('Categoria').agg({
        'Utilidad': 'sum'
    }).reset_index()
    
    if tema == "Oscuro":
        # Degradados de gris claro a blanco para positivos, gris medio a oscuro para negativos
        color_positivo = "#e0e0e0"
        color_negativo = "#606060"
        bg_color = "#0a0a0a"
        text_color = "#e0e0e0"
        grid_color = "#2a2a2a"
    else:
        # Negro a gris oscuro para positivos, gris medio para negativos
        color_positivo = "#2a2a2a"
        color_negativo = "#888888"
        bg_color = "#fafafa"
        text_color = "#2a2a2a"
        grid_color = "#e0e0e0"
    
    colors = [color_positivo if x >= 0 else color_negativo for x in df_agrupado["Utilidad"]]
    
    fig = go.Figure(data=[
        go.Bar(
            x=df_agrupado["Categoria"],
            y=df_agrupado["Utilidad"],
            marker=dict(
                color=colors,
                line=dict(width=2, color=bg_color),
                opacity=0.9
            ),
            name="Utilidad por Categoría"
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Utilidad por Categoría",
            font=dict(color=text_color, size=20, family="Arial Black")
        ),
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(color=text_color, family="Arial"),
        height=450,
        xaxis=dict(
            title="Categoría",
            title_font=dict(size=14, color=text_color),
            tickfont=dict(color=text_color)
        ),
        yaxis=dict(
            title="Utilidad",
            title_font=dict(size=14, color=text_color),
            gridcolor=grid_color,
            showgrid=True,
            gridwidth=1,
            tickfont=dict(color=text_color)
        ),
        showlegend=False
    )
    
    return fig

# --------------------
# SIDEBAR - WIDGETS COMPLETOS
# --------------------
st.sidebar.title("⚙️ Configuración y Filtros")

# 1. WIDGET: Radio Button para tema
tema = st.sidebar.radio(
    "🎨 Tema visual", 
    ["Claro", "Oscuro"],
    help="Selecciona el tema de la interfaz"
)
aplicar_estilo_css(tema)

st.sidebar.markdown("---")

# 2. WIDGET: Checkbox para usar datos simulados
usar_datos_simulados = st.sidebar.checkbox(
    "📊 Usar datos simulados", 
    value=True,
    help="Desactiva para subir tu propio archivo"
)

# 3. WIDGETS para datos simulados
if usar_datos_simulados:
    st.sidebar.subheader("🎲 Configuración de datos simulados")
    
    # WIDGET: Slider para número de meses
    num_meses = st.sidebar.slider(
        "Número de meses", 
        min_value=3, 
        max_value=24, 
        value=12,
        help="Cantidad de meses de datos a generar"
    )
    
    # WIDGET: Select box para año
    año_seleccionado = st.sidebar.selectbox(
        "Año de datos",
        options=[2022, 2023, 2024, 2025],
        index=2,
        help="Año base para generar los datos"
    )

st.sidebar.markdown("---")

# 4. WIDGETS de filtros (siempre visibles)
st.sidebar.subheader("🔍 Filtros de análisis")

# Generar o cargar datos primero para obtener las opciones
if usar_datos_simulados:
    df_principal = generar_datos_falsos(num_meses, año_seleccionado)
else:
    df_principal = pd.DataFrame()  # Se llenará con upload

# WIDGET: Multiselect para categorías (solo si hay datos)
if not df_principal.empty:
    categorias_disponibles = df_principal['Categoria'].unique()
    categorias_seleccionadas = st.sidebar.multiselect(
        "Categorías a mostrar",
        options=categorias_disponibles,
        default=categorias_disponibles,
        help="Selecciona las categorías a incluir en los análisis"
    )
    
    # WIDGET: Date input para rango de fechas
    fecha_min = df_principal['Fecha'].min().date()
    fecha_max = df_principal['Fecha'].max().date()
    
    rango_fechas = st.sidebar.date_input(
        "Rango de fechas",
        value=(fecha_min, fecha_max),
        min_value=fecha_min,
        max_value=fecha_max,
        help="Selecciona el período a analizar"
    )
    
    # WIDGET: Number input para monto mínimo
    monto_minimo = st.sidebar.number_input(
        "Monto mínimo a mostrar",
        min_value=0,
        max_value=50000,
        value=0,
        step=500,
        help="Filtrar registros por monto mínimo"
    )
    
    # WIDGET: Select slider para regiones
    regiones_disponibles = df_principal['Region'].unique()
    regiones_seleccionadas = st.sidebar.select_slider(
        "Regiones",
        options=regiones_disponibles,
        value=regiones_disponibles[0],
        help="Desliza para seleccionar región"
    )
else:
    categorias_seleccionadas = []
    rango_fechas = None
    monto_minimo = 0
    regiones_seleccionadas = None

# --------------------
# MAIN - UPLOAD DE ARCHIVOS
# --------------------
st.title("📊 Dashboard Financiero V2")

# SECCIÓN DE UPLOAD (solo si no se usan datos simulados)
if not usar_datos_simulados:
    st.markdown("### 📁 Subir Archivo de Datos")
    
    col_upload1, col_upload2 = st.columns([2, 1])
    
    with col_upload1:
        # WIDGET: File uploader con múltiples tipos
        uploaded_file = st.file_uploader(
            "Sube tu archivo de datos financieros",
            type=['csv', 'xlsx', 'xls'],
            help="Formatos soportados: CSV, Excel (.xlsx, .xls)",
            accept_multiple_files=False
        )
        
        if uploaded_file is not None:
            # Mostrar información del archivo
            st.success(f"✅ Archivo cargado: {uploaded_file.name}")
            st.info(f"📏 Tamaño: {uploaded_file.size} bytes")
            
            # Procesar el archivo
            if uploaded_file.name.endswith('.csv'):
                df_cargado, error = procesar_archivo_csv(uploaded_file)
            else:
                try:
                    df_cargado = pd.read_excel(uploaded_file)
                    error = None
                except Exception as e:
                    df_cargado = None
                    error = str(e)
            
            if error:
                st.error(f"❌ Error al procesar archivo: {error}")
                df_principal = pd.DataFrame()
            else:
                df_principal = df_cargado
                st.success(f"✅ Datos cargados correctamente: {len(df_principal)} registros")
                
                # Mostrar vista previa
                with st.expander("👀 Vista previa de los datos"):
                    st.dataframe(df_principal.head())
    
    with col_upload2:
        # Ejemplo de formato esperado
        st.markdown("#### 📋 Formato esperado:")
        ejemplo_df = pd.DataFrame({
            'Fecha': ['2024-01-01', '2024-02-01'],
            'Categoria': ['Ventas', 'Servicios'],
            'Ingresos': [10000, 8000],
            'Egresos': [7000, 6000]
        })
        st.dataframe(ejemplo_df)
        
        # WIDGET: Botón para descargar plantilla
        csv_template = ejemplo_df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar plantilla CSV",
            data=csv_template,
            file_name="plantilla_datos_financieros.csv",
            mime="text/csv",
            help="Descarga una plantilla para estructurar tus datos"
        )

# Solo continuar si hay datos disponibles
if df_principal.empty:
    st.warning("⚠️ No hay datos disponibles. Activa 'Usar datos simulados' o sube un archivo.")
    st.stop()

# Aplicar filtros a los datos
df_filtrado = df_principal.copy()

# Filtrar por rango de fechas si está disponible
if rango_fechas and len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas
    df_filtrado = df_filtrado[
        (df_filtrado['Fecha'].dt.date >= fecha_inicio) & 
        (df_filtrado['Fecha'].dt.date <= fecha_fin)
    ]

# Filtrar por monto mínimo
if 'Ingresos' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Ingresos'] >= monto_minimo]

# Filtrar por región si está disponible
if regiones_seleccionadas and 'Region' in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado['Region'] == regiones_seleccionadas]

# --------------------
# MÉTRICAS PRINCIPALES
# --------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_ingresos = df_filtrado['Ingresos'].sum() if 'Ingresos' in df_filtrado.columns else 0
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">💰 Ingresos totales</div>
        <div class="metric-value">${total_ingresos:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    total_egresos = df_filtrado['Egresos'].sum() if 'Egresos' in df_filtrado.columns else 0
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">💸 Egresos totales</div>
        <div class="metric-value">${total_egresos:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    utilidad_total = total_ingresos - total_egresos
    emoji_utilidad = "📈" if utilidad_total >= 0 else "📉"
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">{emoji_utilidad} Utilidad neta</div>
        <div class="metric-value">${utilidad_total:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    num_registros = len(df_filtrado)
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-title">📊 Registros</div>
        <div class="metric-value">{num_registros:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --------------------
# GRÁFICOS
# --------------------
    
fig1 = crear_grafico_lineas(df_filtrado, tema, categorias_seleccionadas)
st.plotly_chart(fig1, use_container_width=True)

fig2 = crear_grafico_barras_categorias(df_filtrado, tema, categorias_seleccionadas)
st.plotly_chart(fig2, use_container_width=True)

# --------------------
# TABLA DE DATOS Y WIDGETS ADICIONALES
# --------------------
st.markdown("### 📋 Análisis Detallado")

# WIDGET: Tabs para diferentes vistas
tab1, tab2, tab3 = st.tabs(["📊 Datos Completos", "📈 Resumen por Categoría", "🎛️ Widgets Demo"])

with tab1:
    # WIDGET: Checkbox para mostrar solo utilidades positivas
    solo_positivas = st.checkbox("Mostrar solo utilidades positivas")
    
    df_tabla = df_filtrado.copy()
    if solo_positivas and 'Utilidad' in df_tabla.columns:
        df_tabla = df_tabla[df_tabla['Utilidad'] > 0]
    
    # Formatear DataFrame para mostrar
    if not df_tabla.empty:
        df_display = df_tabla.copy()
        if 'Fecha' in df_display.columns:
            df_display["Fecha"] = df_display["Fecha"].dt.strftime("%Y/%m/%d")
        
        # Aplicar formato a columnas numéricas
        numeric_columns = df_display.select_dtypes(include=[np.number]).columns
        format_dict = {col: "${:,.0f}" if col in ['Ingresos', 'Egresos', 'Utilidad'] else "{:,.0f}" 
                      for col in numeric_columns}
        
        if format_dict:
            df_styled = df_display.style.format(format_dict)
            st.dataframe(df_styled, use_container_width=True)
        else:
            st.dataframe(df_display, use_container_width=True)
    else:
        st.info("No hay datos que mostrar con los filtros actuales.")

with tab2:
    if not df_filtrado.empty and 'Categoria' in df_filtrado.columns:
        resumen_categoria = df_filtrado.groupby('Categoria').agg({
            'Ingresos': ['sum', 'mean', 'count'],
            'Egresos': ['sum', 'mean'],
            'Utilidad': ['sum', 'mean']
        }).round(2)
        
        st.dataframe(resumen_categoria, use_container_width=True)
    else:
        st.info("No hay datos de categorías disponibles.")

with tab3:
    st.markdown("#### 🎛️ Demostración de Widgets Adicionales")
    
    col_widget1, col_widget2 = st.columns(2)
    
    with col_widget1:
        # WIDGET: Text input
        nombre_reporte = st.text_input("Nombre del reporte", value="Reporte Mensual")
        
        # WIDGET: Text area
        comentarios = st.text_area("Comentarios del análisis", 
                                  placeholder="Escribe tus observaciones aquí...")
        
        # WIDGET: Time input
        hora_reporte = st.time_input("Hora de generación del reporte")
        
        # WIDGET: Color picker (limitado a escala de grises)
        color_personalizado = st.color_picker("Tono de gris personalizado", "#808080")
    
    with col_widget2:
        # WIDGET: Select slider con ratings
        rating = st.select_slider(
            "Califica el desempeño",
            options=['Muy Malo', 'Malo', 'Regular', 'Bueno', 'Excelente'],
            value='Bueno'
        )
        
        # WIDGET: Range slider
        rango_utilidad = st.slider(
            "Rango de utilidad esperada",
            min_value=-10000,
            max_value=50000,
            value=(-5000, 25000),
            step=1000
        )
        
        # WIDGET: Toggle
        notificaciones = st.toggle("Activar notificaciones")
        
        # WIDGET: Botones
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Actualizar datos", type="primary"):
                st.success("Datos actualizados!")
                st.rerun()
        
        with col_btn2:
            # WIDGET: Download button para datos filtrados
            if not df_filtrado.empty:
                csv_data = df_filtrado.to_csv(index=False)
                st.download_button(
                    label="📥 Descargar datos",
                    data=csv_data,
                    file_name=f"datos_filtrados_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )

# --------------------
# INFORMACIÓN ADICIONAL
# --------------------
with st.expander("ℹ️ Información sobre widgets utilizados"):
    st.markdown("""
    **Widgets implementados en este dashboard:**
    
    **Entrada de datos:**
    - `st.file_uploader()` - Subir archivos CSV/Excel
    - `st.text_input()` - Entrada de texto
    - `st.text_area()` - Entrada de texto largo
    - `st.number_input()` - Entrada numérica
    - `st.date_input()` - Selector de fechas
    - `st.time_input()` - Selector de hora
    - `st.color_picker()` - Selector de color (limitado a escala de grises)
    
    **Selección:**
    - `st.radio()` - Botones de radio
    - `st.selectbox()` - Lista desplegable
    - `st.multiselect()` - Selección múltiple
    - `st.select_slider()` - Slider de selección
    
    **Controles:**
    - `st.slider()` - Slider numérico/rango
    - `st.checkbox()` - Casilla de verificación
    - `st.toggle()` - Interruptor
    - `st.button()` - Botón
    - `st.download_button()` - Botón de descarga
    
    **Organización:**
    - `st.tabs()` - Pestañas
    - `st.columns()` - Columnas
    - `st.expander()` - Secciones expandibles
    - `st.sidebar` - Barra lateral
    
    **Paleta de colores elegante:**
    - Tema claro: Negro (#1a1a1a), gris oscuro (#2a2a2a), gris medio (#666666)
    - Tema oscuro: Blanco (#ffffff), gris claro (#e0e0e0), gris medio (#808080)
    - Todos los degradados utilizan transiciones suaves entre tonos de la escala de grises
    - Efectos hover y sombras para mayor sofisticación visual
    - Tipografía mejorada con pesos y espaciados elegantes
    """)