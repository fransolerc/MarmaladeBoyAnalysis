from modules.data_processing import DataProcessor
from modules.text_processing import TextProcessor
from modules.visualizations import Visualizer
import pandas as pd

def run_dialogue_count(df):
    """Calculates and plots character dialogue counts."""
    print("\n--- Running Dialogue Count Analysis ---")
    df_dialogue_counts = DataProcessor.create_character_counts(df)
    Visualizer.plot_character_dialogues(df_dialogue_counts)
    print("Dialogue count plot generated.")

def run_scene_line_count(df):
    """Calculates and plots scene and line counts per character."""
    print("\n--- Running Scene and Line Count Analysis ---")
    speaker_scene_count = DataProcessor.calculate_scene_counts(df)
    scene_count = dict(sorted(speaker_scene_count.items(), key=lambda item: item[1], reverse=True))
    df_scenes_lines = pd.DataFrame(scene_count).T
    df_scenes_lines.columns = ['# of Scenes', '# of lines spoken']
    df_scenes_lines['# of lines per scene'] = df_scenes_lines['# of lines spoken'] / df_scenes_lines['# of Scenes']
    Visualizer.plot_scenes_lines(df_scenes_lines)
    print("Scene and line count plot generated.")

def run_interaction_graph(df):
    """Calculates and generates the interactive character interaction graph."""
    print("\n--- Generating Interactive Character Interaction Graph ---")
    print("Calculating character interactions...")
    interaction_dict = DataProcessor.calculate_character_interactions(df)
    print("Generating interactive network graph...")
    Visualizer.plot_interactive_interactions(df, interaction_dict)
    print("Interactive graph 'interactive_network.html' saved.")

def run_sentiment_analysis(df, text_processor):
    """Processes text for sentiment and plots the distribution."""
    print("\n--- Running Sentiment Analysis ---")
    print("Processing text and analyzing sentiment... (This may take a moment)")
    # Use a copy to avoid modifying the original DataFrame
    processed_df = text_processor.process_text(df.copy())
    print("Processing complete.")
    print("Generating sentiment distribution plot...")
    Visualizer.plot_sentiment_distribution(processed_df)
    print("Sentiment distribution plot generated.")
    return processed_df # Return processed df for further use

def run_sentiment_evolution(df, text_processor):
    """Calculates and plots sentiment evolution over episodes."""
    print("\n--- Running Sentiment Evolution Analysis ---")

    # Check if sentiment has been calculated, if not, do it
    if 'sentiment' not in df.columns:
        print("Sentiment data not found. Processing text first...")
        df = text_processor.process_text(df.copy())

    print("Calculating sentiment evolution...")
    df_evolution = DataProcessor.calculate_sentiment_evolution(df)

    if not df_evolution.empty:
        print("\n--- Sentiment Evolution Stats ---")
        print(df_evolution.describe())
        print("\nFirst 5 rows:")
        print(df_evolution.head())
        print("---------------------------------")

        print("Generating sentiment evolution plot...")
        Visualizer.plot_sentiment_evolution(df_evolution)
        print("Sentiment evolution plot generated.")
    else:
        print("Could not generate evolution data.")

def display_menu():
    """Displays the main menu and gets user choice."""
    print("\n" + "="*30)
    print("  Marmalade Boy Analysis Menu")
    print("="*30)
    print("1. Plot Character Dialogue Counts")
    print("2. Plot Scene and Line Counts")
    print("3. Generate Interactive Interaction Graph")
    print("4. Plot Sentiment Distribution")
    print("5. Plot Sentiment Evolution (Time Series)")
    print("6. Run All Analyses")
    print("0. Exit")
    try:
        return input("Enter your choice [1-6, 0]: ")
    except (EOFError, KeyboardInterrupt):
        return '0'

def get_sentiment_data(df, text_processor, df_with_sentiment):
    """Helper to ensure sentiment data is available."""
    if df_with_sentiment is None:
        print("Processing text for sentiment first...")
        return text_processor.process_text(df.copy())
    return df_with_sentiment

def handle_menu_choice(choice, df, text_processor, df_with_sentiment):
    """Handles the user's menu choice and executes the corresponding analysis."""

    if choice == '1':
        run_dialogue_count(df)
    elif choice == '2':
        run_scene_line_count(df)
    elif choice == '3':
        run_interaction_graph(df)
    elif choice == '4':
        if df_with_sentiment is None:
            df_with_sentiment = run_sentiment_analysis(df, text_processor)
        else:
            Visualizer.plot_sentiment_distribution(df_with_sentiment)
    elif choice == '5':
        df_with_sentiment = get_sentiment_data(df, text_processor, df_with_sentiment)
        run_sentiment_evolution(df_with_sentiment, text_processor)
    elif choice == '6':
        print("\n--- Running All Analyses ---")
        run_dialogue_count(df)
        run_scene_line_count(df)
        run_interaction_graph(df)

        if df_with_sentiment is None:
            df_with_sentiment = run_sentiment_analysis(df, text_processor)
        else:
            Visualizer.plot_sentiment_distribution(df_with_sentiment)

        run_sentiment_evolution(df_with_sentiment, text_processor)
        print("\nAll analyses complete.")
    elif choice == '0':
        print("Exiting program.")
        return df_with_sentiment, False # Signal to exit loop
    else:
        print("Invalid choice. Please enter a number between 0 and 6.")

    return df_with_sentiment, True # Signal to continue loop

def main():
    try:
        print("Loading data...")
        df = DataProcessor.load_data('data/script.csv')
        if df.empty:
            print("Failed to load data. Please check the file and try again.")
            return
        print("Data loaded successfully.")

        # Initialize the text processor once
        text_processor = TextProcessor()

        # Keep a version of df with sentiment if calculated to avoid re-processing
        df_with_sentiment = None
        running = True

        while running:
            choice = display_menu()
            df_with_sentiment, running = handle_menu_choice(choice, df, text_processor, df_with_sentiment)

    except Exception as e:
        print(f"\nA critical error occurred: {e}")

if __name__ == "__main__":
    main()
