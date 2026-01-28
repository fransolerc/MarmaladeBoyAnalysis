# Análisis de Relaciones de Personajes en "Marmalade Boy"

Este repositorio contiene un análisis detallado de las relaciones entre los personajes de "Marmalade Boy" utilizando técnicas de procesamiento de texto y visualización de datos en Python.

## Características
- **Conteo de Diálogos por Personaje**: Analiza el número de diálogos por personaje.
- **Desglose de Escenas**: Analiza el número de escenas y líneas habladas por personaje.
- **Gráfico de Interacciones entre Personajes**: Visualiza las interacciones entre personajes usando grafos de red.

## Instalación

### Requisitos Previos
- [Python 3.8+](https://www.python.org/downloads/) (Se recomienda marcar "Add Python to PATH" durante la instalación en Windows).
- [Git](https://git-scm.com/downloads)

### Pasos para la Instalación

1.  **Clona el repositorio**
    Abre una terminal (o `cmd` / `PowerShell` en Windows) y ejecuta:
    ```bash
    git clone https://github.com/fransolerc/MarmaladeBoyAnalysis.git
    cd MarmaladeBoyAnalysis
    ```

2.  **Crea y activa un entorno virtual**
    Es una buena práctica aislar las dependencias del proyecto.

    *   **En Windows:**
        ```bash
        python -m venv env
        .\env\Scripts\activate
        ```
    *   **En macOS / Linux:**
        ```bash
        python3 -m venv env
        source env/bin/activate
        ```
    Después de activarlo, deberías ver `(env)` al inicio de la línea de tu terminal.

3.  **Instala las dependencias**
    Con el entorno virtual activado, instala las librerías necesarias:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Descarga los datos de NLTK**
    El proyecto necesita algunos paquetes de la librería NLTK. Ejecuta el siguiente comando para descargarlos de forma automática:
    ```bash
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
    ```

## Uso

1.  **Prepara el archivo de datos**
    Asegúrate de que tu archivo con los diálogos se encuentre en `data/script.csv`. Debe tener las siguientes columnas, sin cabecera: `index`, `episode`, `scene`, `character`, `dialogue`.

2.  **Ejecuta el análisis**
    Para correr el script principal, simplemente ejecuta:
    ```bash
    python main.py
    ```
    El programa procesará los datos y mostrará varias ventanas con los gráficos generados.

## Estructura del Proyecto
```
marmalade-boy-analysis/
│
├── data/
│   └── script.csv
├── modules/
│   ├── data_processing.py
│   ├── text_processing.py
│   └── visualizations.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Tecnologías
- Python
- Pandas
- Matplotlib & Seaborn
- NLTK
- NetworkX

## Contribuciones
Las contribuciones son bienvenidas. Por favor, abre un *issue* o un *pull request* para discutir cualquier cambio.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT.
