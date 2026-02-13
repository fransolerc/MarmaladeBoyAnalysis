import pandas as pd
from itertools import combinations
import re


class DataProcessor:
    @staticmethod
    def load_data(file_path):
        """
        Load data from a CSV file into a DataFrame.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: DataFrame containing the data from the file.
        """
        try:
            df = pd.read_csv(file_path, names=["index", "episode", "scene", "character", "dialogue"], header=None)
            return df
        except FileNotFoundError:
            print(f"Error: The file at '{file_path}' was not found.")
            return pd.DataFrame()  # Return an empty DataFrame
        except pd.errors.EmptyDataError:
            print(f"Error: The file at '{file_path}' is empty.")
            return pd.DataFrame()  # Return an empty DataFrame
        except pd.errors.ParserError:
            print(f"Error: There was a problem parsing the file at '{file_path}'.")
            return pd.DataFrame()  # Return an empty DataFrame
        except Exception as e:
            print(f"Unexpected error loading the file: {e}")
            return pd.DataFrame()  # Return an empty DataFrame

    @staticmethod
    def create_character_counts(df):
        """
        Create a DataFrame containing the count of dialogues for each character.

        Args:
            df (pd.DataFrame): DataFrame containing the dialogue data.

        Returns:
            pd.DataFrame: DataFrame with character counts.
        """
        try:
            df2 = df['character'].value_counts().reset_index()
            df2.columns = ['character', 'count']
            df2 = df2.head(20)
            return df2
        except KeyError:
            print("Error: The DataFrame does not contain a 'character' column.")
            return pd.DataFrame()  # Return an empty DataFrame
        except Exception as e:
            print(f"Unexpected error creating character counts: {e}")
            return pd.DataFrame()  # Return an empty DataFrame

    @staticmethod
    def calculate_scene_counts(df):
        speaker_scene_count = {}
        for name, df_group in df.groupby(['episode', 'scene']):
            for speaker_name in df_group.character.unique().tolist():
                if speaker_name in speaker_scene_count:
                    speaker_scene_count[speaker_name][0] += 1
                    speaker_scene_count[speaker_name][1] += df_group.character.tolist().count(speaker_name)
                else:
                    speaker_scene_count[speaker_name] = [1, df_group.character.tolist().count(speaker_name)]

        return speaker_scene_count

    @staticmethod
    def calculate_character_interactions(df):
        char_dict = {}
        for _, scene_df in df.groupby(['episode', 'scene']):
            characters_in_scene = sorted(scene_df['character'].unique())

            # Generate combinations of 2 and 3 characters
            for i in range(2, 4):
                for combo in combinations(characters_in_scene, i):
                    key = ", ".join(combo)
                    char_dict[key] = char_dict.get(key, 0) + 1

        # Sort the dictionary by value in descending order
        sorted_interactions = dict(sorted(char_dict.items(), key=lambda item: item[1], reverse=True))

        return sorted_interactions

    @staticmethod
    def calculate_sentiment_evolution(df):
        """
        Calculates the average sentiment per episode.
        Assumes 'sentiment' column exists with values 'POS', 'NEU', 'NEG'.
        """
        if 'sentiment' not in df.columns:
            print("Error: 'sentiment' column missing. Run text processing first.")
            return pd.DataFrame()

        # Map sentiment labels to numerical values
        sentiment_map = {'POS': 1, 'NEU': 0, 'NEG': -1}

        # Create a copy to avoid SettingWithCopyWarning on the original df
        df_calc = df.copy()
        df_calc['sentiment_score'] = df_calc['sentiment'].map(sentiment_map)

        # Group by episode and calculate mean
        sentiment_evolution = df_calc.groupby('episode')['sentiment_score'].mean().reset_index()

        # Sort by episode numerically
        try:
            # Extract numbers from the episode string if it contains text (e.g., "Episode 1")
            # If it's already numeric or string of digits, this will handle it
            sentiment_evolution['episode_num'] = sentiment_evolution['episode'].astype(str).str.extract(r'(\d+)').astype(float)

            # Sort by the extracted number
            sentiment_evolution = sentiment_evolution.sort_values('episode_num')

            # Drop the helper column
            sentiment_evolution = sentiment_evolution.drop('episode_num', axis=1)

        except Exception as e:
            print(f"Warning: Could not sort episodes numerically ({e}). Falling back to default sort.")
            sentiment_evolution = sentiment_evolution.sort_values('episode')

        return sentiment_evolution
