# -*- coding: utf-8 -*-
"""App00.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1df7yn5bXtv4U5UQhmw5oDA-3VjCi1VH2
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from geopy.distance import geodesic

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("analisis_clientes.csv")

df = cargar_datos()

# Verificar columnas numéricas
df_numeric = df.select_dtypes(include=['number'])

# Sidebar con opciones
opciones = [
    "Visión General",
    "Análisis de Correlación",
    "Mapas de Ubicación",
    "Mapas Personalizados",
    "Análisis de Clúster",
    "Gráficos de Barras",
    "Mapa de Calor",
    "Cálculo de Distancias"
]
opcion = st.sidebar.radio("Selecciona un análisis", opciones)

# Diccionario de funciones
def vision_general():
    st.title("📊 Análisis de Datos de Clientes")
    st.write("Datos cargados con éxito. Vista previa:")
    st.dataframe(df.head())

def analisis_correlacion():
    st.title("🔗 Análisis de Correlación")

    # Matriz de correlación global
    st.subheader("Matriz de Correlación Global")
    matriz_corr = df_numeric.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(matriz_corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    # Correlación segmentada
    st.subheader("Correlación por Género")
    genero = st.selectbox("Selecciona el género", df["Género"].unique())
    df_genero = df[df["Género"] == genero].select_dtypes(include=['number'])
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df_genero.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

def mapas_ubicacion():
    st.title("📍 Mapas de Ubicación de Clientes")
    mapa_global = px.scatter_mapbox(
        df, lat="Latitud", lon="Longitud", hover_data=["Edad", "Ingreso_Anual_USD"],
        color="Género", zoom=3, mapbox_style="open-street-map"
    )
    st.plotly_chart(mapa_global)

    # Mapa segmentado
    genero = st.selectbox("Selecciona género para el mapa", df["Género"].unique())
    df_genero = df[df["Género"] == genero]
    mapa_genero = px.scatter_mapbox(
        df_genero, lat="Latitud", lon="Longitud", hover_data=["Edad", "Ingreso_Anual_USD"],
        zoom=3, mapbox_style="open-street-map"
    )
    st.plotly_chart(mapa_genero)

def mapas_personalizados():
    st.title("🗺️ Mapas Personalizados")
    
    # Selección de variables
    var1 = st.selectbox("Variable 1", df.columns)
    var2 = st.selectbox("Variable 2", df.columns)
    
    # Rango de valores
    min1, max1 = st.slider(f"Rango para {var1}", float(df[var1].min()), float(df[var1].max()), (float(df[var1].min()), float(df[var1].max())))
    min2, max2 = st.slider(f"Rango para {var2}", float(df[var2].min()), float(df[var2].max()), (float(df[var2].min()), float(df[var2].max())))

    # Filtrar datos
    df_filtrado = df[(df[var1] >= min1) & (df[var1] <= max1) & (df[var2] >= min2) & (df[var2] <= max2)]
    
    # Mostrar mapa
    mapa_custom = px.scatter_mapbox(df_filtrado, lat="Latitud", lon="Longitud", color=var1, zoom=3, mapbox_style="open-street-map")
    st.plotly_chart(mapa_custom)

def analisis_cluster():
    st.title("📈 Análisis de Clúster")
    df["Frecuencia_Compra"] = pd.cut(df["Frecuencia_Compra"], bins=3, labels=["Baja", "Media", "Alta"])
    cluster_plot = px.scatter(df, x="Edad", y="Ingreso_Anual_USD", color="Frecuencia_Compra")
    st.plotly_chart(cluster_plot)

def graficos_barras():
    st.title("📊 Gráfico de Barras por Género y Frecuencia de Compra")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(x="Genero", hue="Frecuencia_Compra", data=df, ax=ax)
    st.pyplot(fig)

def mapa_calor():
    st.title("🔥 Mapa de Calor de Ingresos")

    # Filtrar solo columnas numéricas
    df_numeric = df.select_dtypes(include=['number'])

    # Crear una matriz de correlación sin verificar la cantidad de columnas
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df_numeric.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)


def calculo_distancias():
    st.title("📏 Cálculo de Distancias entre Compradores de Mayores Ingresos")

    # Filtrar compradores con los mayores ingresos
    df_top = df.nlargest(10, "Ingreso")

    # Calcular distancias
    distancias = [
        (df_top.iloc[i]["ID"], df_top.iloc[j]["ID"], geodesic((df_top.iloc[i]["Latitud"], df_top.iloc[i]["Longitud"]), 
                                                               (df_top.iloc[j]["Latitud"], df_top.iloc[j]["Longitud"])).km)
        for i in range(len(df_top)) for j in range(i + 1, len(df_top))
    ]

    # Mostrar resultados
    distancias_df = pd.DataFrame(distancias, columns=["Cliente 1", "Cliente 2", "Distancia (km)"])
    st.dataframe(distancias_df)

# Ejecutar la función seleccionada
funciones = [
    vision_general, 
    analisis_correlacion, 
    mapas_ubicacion, 
    mapas_personalizados, 
    analisis_cluster, 
    graficos_barras, 
    mapa_calor, 
    calculo_distancias
]
funciones[opciones.index(opcion)]()
