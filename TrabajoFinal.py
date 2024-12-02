import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título
st.title("Visualización de datos con Streamlit")

# Subir un archivo
uploaded_file = st.file_uploader("Carga tu archivo Excel o CSV", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Verificar tipo de archivo
    if uploaded_file.name.endswith(".csv"):
        # Leer archivo CSV
        data = pd.read_csv(uploaded_file)
        st.write("Vista previa de los datos:", data.head())
    elif uploaded_file.name.endswith(".xlsx"):
        # Leer archivo Excel
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names  # Obtener nombres de las hojas
        
        if len(sheet_names) == 1:
            # Si solo hay una hoja, cargarla directamente
            data = excel_file.parse(sheet_names[0])
            st.write(f"Vista previa de la única hoja '{sheet_names[0]}':", data.head())
        else:
            # Si hay varias hojas, permitir seleccionar
            selected_sheet = st.selectbox("Selecciona una hoja:", sheet_names)  # Seleccionar hoja
            data = excel_file.parse(selected_sheet)  # Cargar hoja seleccionada
            st.write(f"Vista previa de la hoja '{selected_sheet}':", data.head())
    
    # Seleccionar columna para graficar
    column = st.selectbox("Selecciona una columna para graficar", data.columns)

    # Graficar
    if column:
        # Ordenar y seleccionar los valores más importantes
        value_counts = data[column].value_counts().head(10)  # Los 10 más frecuentes
        fig, ax = plt.subplots(figsize=(10, 6))  # Tamaño ajustado del gráfico
        value_counts.sort_values(ascending=True).plot(kind="barh", ax=ax)  # Gráfico de barras horizontal
        ax.set_title(f"Top 10 valores más frecuentes en {column}")
        ax.set_xlabel("Frecuencia")
        ax.set_ylabel(column)
        st.pyplot(fig)
