from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Variable global para almacenar los datos cargados
uploaded_data = {}

@app.route("/")
def index():
    return render_template("index.html")  # Página principal para subir archivos

@app.route("/upload", methods=["POST"])
def upload_file():
    global uploaded_data
    file = request.files["file"]
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Cargar datos en un DataFrame y almacenarlos globalmente
        data = pd.read_csv(file_path)
        uploaded_data["data"] = data
        return redirect(url_for("select_column"))
    return "No se cargó ningún archivo", 400

@app.route("/select_column")
def select_column():
    global uploaded_data
    data = uploaded_data.get("data")
    if data is not None:
        columns = data.columns.tolist()
        return render_template("select_column.html", columns=columns)
    return redirect(url_for("index"))

@app.route("/process", methods=["POST"])
def process_data():
    global uploaded_data
    column = request.form.get("column")
    data = uploaded_data.get("data")
    
    if data is not None and column in data.columns:
        # Generar gráfico
        value_counts = data[column].value_counts().head(10)
        fig, ax = plt.subplots(figsize=(10, 6))
        value_counts.sort_values(ascending=True).plot(kind="barh", ax=ax)
        ax.set_title(f"Top 10 valores más frecuentes en {column}")
        ax.set_xlabel("Frecuencia")
        ax.set_ylabel(column)
        
        # Guardar gráfico
        output_path = os.path.join(OUTPUT_FOLDER, "chart.png")
        plt.savefig(output_path)
        plt.close()
        return render_template("chart.html", column=column, chart_url=output_path)
    
    return "Columna seleccionada no válida", 400

if __name__ == "__main__":
    app.run(debug=True)
