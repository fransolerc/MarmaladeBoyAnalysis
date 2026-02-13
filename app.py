import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from modules.data_processing import DataProcessor
from modules.text_processing import TextProcessor
from modules.visualizations import Visualizer

# Constants for Analysis Options
OPTION_DIALOGUE_COUNT = "Dialogue Count"
OPTION_SCENE_LINE_ANALYSIS = "Scene & Line Analysis"
OPTION_SENTIMENT_DISTRIBUTION = "Sentiment Distribution"
OPTION_SENTIMENT_EVOLUTION = "Sentiment Evolution (Time Series)"
OPTION_INTERACTION_GRAPH = "Interaction Network Graph"

# Constants for UI Labels
LABEL_NUM_CHARACTERS = "Number of characters to show"

# Page configuration
st.set_page_config(
    page_title="Marmalade Boy Analysis",
    page_icon="🍊",
    layout="wide"
)

# Title and Description
st.title("🍊 Marmalade Boy Character Analysis")
st.markdown("""
This dashboard provides an interactive analysis of character relationships and dialogues in the anime **Marmalade Boy**.
Explore dialogue counts, scene breakdowns, sentiment evolution, and character interactions.
""")

# Load Data
@st.cache_data
def load_data():
    return DataProcessor.load_data('data/script.csv')

df = load_data()

if df.empty:
    st.error("Failed to load data. Please check 'data/script.csv'.")
    st.stop()

# Sidebar Menu
st.sidebar.header("Analysis Options")
analysis_type = st.sidebar.radio(
    "Choose an analysis:",
    [
        OPTION_DIALOGUE_COUNT,
        OPTION_SCENE_LINE_ANALYSIS,
        OPTION_SENTIMENT_DISTRIBUTION,
        OPTION_SENTIMENT_EVOLUTION,
        OPTION_INTERACTION_GRAPH
    ]
)

# --- Analysis Logic ---

if analysis_type == OPTION_DIALOGUE_COUNT:
    st.header("Character Dialogue Counts")
    st.markdown("Who talks the most? This chart shows the number of dialogues per character.")

    top_n = st.slider(LABEL_NUM_CHARACTERS, 5, 50, 20)
    df_counts = DataProcessor.create_character_counts(df)

    # Generate plot without showing it immediately
    fig = Visualizer.plot_character_dialogues(df_counts, top_n=top_n, show=False)
    st.pyplot(fig)

elif analysis_type == OPTION_SCENE_LINE_ANALYSIS:
    st.header(OPTION_SCENE_LINE_ANALYSIS)
    st.markdown("Comparison of how many scenes characters appear in vs. how many lines they speak.")

    top_n = st.slider(LABEL_NUM_CHARACTERS, 5, 30, 12)

    speaker_scene_count = DataProcessor.calculate_scene_counts(df)
    scene_count = dict(sorted(speaker_scene_count.items(), key=lambda item: item[1], reverse=True))
    df_scenes_lines = pd.DataFrame(scene_count).T
    df_scenes_lines.columns = ['# of Scenes', '# of lines spoken']
    df_scenes_lines['# of lines per scene'] = df_scenes_lines['# of lines spoken'] / df_scenes_lines['# of Scenes']

    fig = Visualizer.plot_scenes_lines(df_scenes_lines, top_n=top_n, show=False)
    st.pyplot(fig)

elif analysis_type == OPTION_SENTIMENT_DISTRIBUTION:
    st.header(OPTION_SENTIMENT_DISTRIBUTION)
    st.markdown("What is the general mood of each character? (Positive, Neutral, Negative)")

    # Cache the text processing as it's expensive
    @st.cache_data
    def get_processed_data(df):
        tp = TextProcessor()
        return tp.process_text(df.copy())

    with st.spinner("Processing text and analyzing sentiment..."):
        processed_df = get_processed_data(df)

    top_n = st.slider(LABEL_NUM_CHARACTERS, 5, 30, 15)
    fig = Visualizer.plot_sentiment_distribution(processed_df, top_n=top_n, show=False)
    st.pyplot(fig)

elif analysis_type == OPTION_SENTIMENT_EVOLUTION:
    st.header("Sentiment Evolution Over Episodes")
    st.markdown("How does the emotional tone of the series change episode by episode?")

    @st.cache_data
    def get_processed_data(df):
        tp = TextProcessor()
        return tp.process_text(df.copy())

    with st.spinner("Processing text and analyzing sentiment..."):
        processed_df = get_processed_data(df)

    df_evolution = DataProcessor.calculate_sentiment_evolution(processed_df)

    if not df_evolution.empty:
        fig = Visualizer.plot_sentiment_evolution(df_evolution, show=False)
        st.pyplot(fig)
    else:
        st.warning("Could not calculate sentiment evolution.")

elif analysis_type == OPTION_INTERACTION_GRAPH:
    st.header("Character Interaction Network")
    st.markdown("Interactive graph showing who interacts with whom. Drag nodes to explore!")

    interaction_dict = DataProcessor.calculate_character_interactions(df)

    # Generate the HTML file but don't open browser
    html_file = Visualizer.plot_interactive_interactions(df, interaction_dict, show=False)

    # Read and display the HTML file in Streamlit
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        components.html(html_content, height=800, scrolling=True)
    except FileNotFoundError:
        st.error("Network graph file not found.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Created by Fran Soler")
