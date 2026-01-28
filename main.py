from modules.data_processing import DataProcessor
from modules.text_processing import TextProcessor
from modules.visualizations import Visualizer
import pandas as pd


def process_and_plot(df):
    try:
        # --- Static Visualizations ---

        # Create character counts for dialogue plot
        df_dialogue_counts = DataProcessor.create_character_counts(df)
        Visualizer.plot_character_dialogues(df_dialogue_counts)

        # Initialize text processor and process text (including sentiment analysis)
        print("Processing text and analyzing sentiment... (This may take a moment)")
        text_processor = TextProcessor()
        df = text_processor.process_text(df)
        print("Processing complete.")

        # Calculate and plot scene and line counts
        speaker_scene_count = DataProcessor.calculate_scene_counts(df)
        scene_count = dict(sorted(speaker_scene_count.items(), key=lambda item: item[1], reverse=True))
        df_scenes_lines = pd.DataFrame(scene_count).T
        df_scenes_lines.columns = ['# of Scenes', '# of lines spoken']
        df_scenes_lines['# of lines per scene'] = df_scenes_lines['# of lines spoken'] / df_scenes_lines['# of Scenes']
        Visualizer.plot_scenes_lines(df_scenes_lines)

        # --- Interactive Network Visualization ---
        print("Calculating character interactions for the interactive graph...")
        interaction_dict = DataProcessor.calculate_character_interactions(df)

        print("Generating interactive network graph...")
        Visualizer.plot_interactive_interactions(df, interaction_dict)

        # --- Sentiment Visualization (now last) ---
        print("Generating sentiment distribution plot...")
        Visualizer.plot_sentiment_distribution(df)

        print("\nAnalysis complete. Check the generated plots and the 'interactive_network.html' file.")

    except Exception as e:
        print(f"An error occurred during processing: {e}")


def main():
    try:
        print("Loading data...")
        df = DataProcessor.load_data('data/script.csv')

        if not df.empty:
            print("Data loaded successfully.")
            process_and_plot(df)
        else:
            print("Failed to load data. Please check the file and try again.")

    except Exception as e:
        print(f"A critical error occurred: {e}")


if __name__ == "__main__":
    main()
