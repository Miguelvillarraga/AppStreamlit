# -*- coding: utf-8 -*-
"""App00.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1df7yn5bXtv4U5UQhmw5oDA-3VjCi1VH2
"""

import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.cluster import KMeans
from scipy.spatial.distance import pdist, squareform

# Cargar datos desde URL o archivo
def cargar_datos(url=None):
    if url:
        return pd.read_csv(url)
    else:
        archivo_subido = files.upload()
        nombre_archivo = list(archivo_subido.keys())[0]
        return pd.read_csv(nombre_archivo)

# Preprocesar datos
def preprocesar_datos(df):
    return df.interpolate()  # Interpolación de valores faltantes

# Análisis de correlación
def analizar_correlacion(df):
    corr_global = df[['Edad', 'Ingreso_Anual']].corr()
    return corr_global

# Mapa de ubicación
def generar_mapa(df, filtro=None):
    df_filtrado = df if filtro is None else df.query(filtro)
    return px.scatter_mapbox(df_filtrado, lat='Latitud', lon='Longitud', color='Genero', zoom=3, mapbox_style='carto-positron')

# Análisis de clúster
def analizar_cluster(df):
    modelo = KMeans(n_clusters=3, random_state=42, n_init=10).fit(df[['Frecuencia_Compra']])
    df['Cluster'] = modelo.labels_
    return df

# Gráficos de barra
def grafico_barras(df):
    return sns.countplot(data=df, x='Genero', hue='Frecuencia_Compra')

# Mapa de calor
def mapa_calor(df):
    matriz_corr = df.corr()
    plt.figure(figsize=(8, 6))
    return sns.heatmap(matriz_corr, annot=True, cmap='coolwarm')

# Cálculo de distancias
def calcular_distancias(df):
    compradores_altos = df.nlargest(5, 'Ingreso_Anual')
    distancias = squareform(pdist(compradores_altos[['Latitud', 'Longitud']]))
    return distancias

# Código principal
data_url = "https://raw.githubusercontent.com/gabrielawad/programacion-para-ingenieria/refs/heads/main/archivos-datos/aplicaciones/analisis_clientes.csv"
df = cargar_datos(data_url)
df = preprocesar_datos(df)  # Interpolación antes de su uso

# Streamlit App
st.title("Análisis de Clientes")
st.write("Este dashboard interactivo permite analizar los datos de clientes y su comportamiento de compra.")

# Mostrar análisis
st.subheader("Correlación entre Edad e Ingreso Anual")
st.write(analizar_correlacion(df))

st.subheader("Gráfico de Barras por Género y Frecuencia de Compra")
fig_bar, ax = plt.subplots()
grafico_barras(df)
st.pyplot(fig_bar)

st.subheader("Mapa de Calor de Ingresos")
fig_heat, ax = plt.subplots()
mapa_calor(df)
st.pyplot(fig_heat)

st.subheader("Mapa de Ubicación de Clientes")
fig_mapa = generar_mapa(df)
st.plotly_chart(fig_mapa)

st.subheader("Cálculo de Distancias entre Compradores de Mayores Ingresos")
st.write(calcular_distancias(df))
