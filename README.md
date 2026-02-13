# Character Relationship Analysis in "Marmalade Boy"

This repository contains a detailed analysis of the relationships between characters in the anime series "Marmalade Boy". This project uses this anime as a case study to demonstrate how to analyze character conversations and interactions using text processing and data visualization techniques in Python.

## Features
- **Dialogue Count by Character**: Analyzes the number of dialogues per character.
- **Scene Breakdown**: Analyzes the number of scenes and spoken lines per character.
- **Character Interaction Graph**: Visualizes interactions between characters using network graphs.
- **Sentiment Analysis**: Tracks the emotional tone of dialogues and its evolution over episodes.
- **Interactive Dashboard**: A web-based dashboard built with Streamlit to explore all analyses interactively.

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
        > **Note:** If you encounter a security error like `running scripts is disabled on this system` in PowerShell, you can try running this command before activating the environment:
        > ```powershell
        > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
        > ```
        > Alternatively, you can use Command Prompt (`cmd`) instead of PowerShell.

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

### Option 1: Interactive Web Dashboard (Recommended)
The easiest way to explore the data is using the Streamlit dashboard.
```bash
streamlit run app.py
```
This will automatically open the dashboard in your web browser.

### Option 2: Command Line Interface
You can also run the analysis scripts directly from the terminal.
1.  **Prepare the data file**
    Ensure your dialogue file is located at `data/script.csv`. It must have the following columns, without a header: `index`, `episode`, `scene`, `character`, `dialogue`.

2.  **Run the script**
    ```bash
    python main.py
    ```
    Follow the on-screen menu to select the analysis you want to perform.

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
├── app.py              # Streamlit dashboard
├── main.py             # CLI entry point
├── requirements.txt
└── README.md
```

## Technologies
- Python
- Pandas
- Matplotlib & Seaborn
- NLTK
- NetworkX
- Streamlit
- Pyvis

## Contributions
Contributions are welcome. Please open an *issue* or a *pull request* to discuss any changes.

## License
This project is licensed under the MIT License.
