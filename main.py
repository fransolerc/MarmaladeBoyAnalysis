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

def display_menu():
    """Displays the main menu and gets user choice."""
    print("\n" + "="*30)
    print("  Marmalade Boy Analysis Menu")
    print("="*30)
    print("1. Plot Character Dialogue Counts")
    print("2. Plot Scene and Line Counts")
    print("3. Generate Interactive Interaction Graph")
    print("4. Plot Sentiment Distribution")
    print("5. Run All Analyses")
    print("0. Exit")
    return input("Enter your choice [1-5, 0]: ")

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

        while True:
            choice = display_menu()

            if choice == '1':
                run_dialogue_count(df)
            elif choice == '2':
                run_scene_line_count(df)
            elif choice == '3':
                run_interaction_graph(df)
            elif choice == '4':
                run_sentiment_analysis(df, text_processor)
            elif choice == '5':
                print("\n--- Running All Analyses ---")
                run_dialogue_count(df)
                run_scene_line_count(df)
                run_interaction_graph(df)
                run_sentiment_analysis(df, text_processor)
                print("\nAll analyses complete.")
            elif choice == '0':
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 5.")

    except Exception as e:
        print(f"\nA critical error occurred: {e}")

if __name__ == "__main__":
    main()
