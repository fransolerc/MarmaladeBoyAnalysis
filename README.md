# Character Relationship Analysis in "Marmalade Boy"

This repository contains a detailed analysis of the relationships between characters in "Marmalade Boy" using text processing and data visualization techniques in Python.

## Features
- **Dialogue Count by Character**: Analyzes the number of dialogues per character.
- **Scene Breakdown**: Analyzes the number of scenes and spoken lines per character.
- **Character Interaction Graph**: Visualizes interactions between characters using network graphs.

## Installation

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/) (It is recommended to check "Add Python to PATH" during installation on Windows).
- [Git](https://git-scm.com/downloads)

### Installation Steps

1.  **Clone the repository**
    Open a terminal (or `cmd` / `PowerShell` on Windows) and run:
    ```bash
    git clone https://github.com/fransolerc/MarmaladeBoyAnalysis.git
    cd MarmaladeBoyAnalysis
    ```

2.  **Create and activate a virtual environment**
    It is good practice to isolate project dependencies.

    *   **On Windows:**
        ```bash
        python -m venv env
        .\env\Scripts\activate
        ```
    *   **On macOS / Linux:**
        ```bash
        python3 -m venv env
        source env/bin/activate
        ```
    After activating it, you should see `(env)` at the beginning of your terminal line.

3.  **Install dependencies**
    With the virtual environment activated, install the necessary libraries:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download NLTK data**
    The project needs some packages from the NLTK library. Run the following command to download them automatically:
    ```bash
    python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
    ```

## Usage

1.  **Prepare the data file**
    Ensure your dialogue file is located at `data/script.csv`. It must have the following columns, without a header: `index`, `episode`, `scene`, `character`, `dialogue`.

2.  **Run the analysis**
    To run the main script, simply execute:
    ```bash
    python main.py
    ```
    The program will process the data and display several windows with the generated charts.

## Project Structure
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

## Technologies
- Python
- Pandas
- Matplotlib & Seaborn
- NLTK
- NetworkX

## Contributions
Contributions are welcome. Please open an *issue* or a *pull request* to discuss any changes.

## License
This project is licensed under the MIT License.
