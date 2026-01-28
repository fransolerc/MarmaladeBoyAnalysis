import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import pandas as pd
from pyvis.network import Network
import webbrowser
import os

class Visualizer:
    """A class for visualizing character data and interactions."""

    PALETTE = "viridis"
    SENTIMENT_COLORS = {"POS": "green", "NEU": "gray", "NEG": "red"}

    @staticmethod
    def plot_character_dialogues(df, top_n=20):
        # (No changes to this method)
        sns.set(style="whitegrid")
        plt.figure(figsize=(14, 10))
        top_characters = df.nlargest(top_n, 'count')
        colors = sns.color_palette(Visualizer.PALETTE, n_colors=len(top_characters))
        bars = plt.barh(top_characters['character'], top_characters['count'], color=colors, edgecolor='black')
        for bar in bars:
            plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}',
                     va='center', ha='left', fontsize=10, color='black')
        plt.xlabel('Number of Dialogues', fontsize=12)
        plt.ylabel('Character', fontsize=12)
        plt.title(f'Top {top_n} Characters by Dialogue Count', fontsize=14)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_scenes_lines(df_scenes_lines, top_n=12):
        # (No changes to this method)
        sns.set(style="whitegrid")
        _, axes = plt.subplots(1, 2, figsize=(18, 10))
        scenes = df_scenes_lines['# of Scenes'].nlargest(top_n)
        sns.barplot(x=scenes.values, y=scenes.index, ax=axes[0], palette=Visualizer.PALETTE)
        axes[0].set_title(f'Top {top_n} Characters by Scene Count', fontsize=14)
        axes[0].set_xlabel('Number of Scenes', fontsize=12)
        axes[0].set_ylabel('Character', fontsize=12)
        lines_spoken = df_scenes_lines['# of lines spoken'].nlargest(top_n)
        sns.barplot(x=lines_spoken.values, y=lines_spoken.index, ax=axes[1], palette=Visualizer.PALETTE)
        axes[1].set_title(f'Top {top_n} Characters by Lines Spoken', fontsize=14)
        axes[1].set_xlabel('Number of Lines Spoken', fontsize=12)
        axes[1].set_ylabel('')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_sentiment_distribution(df, top_n=15):
        # (No changes to this method)
        top_characters = df['character'].value_counts().nlargest(top_n).index
        df_top = df[df['character'].isin(top_characters)]
        sentiment_counts = pd.crosstab(df_top['character'], df_top['sentiment'])
        sentiment_dist = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0)
        sentiment_dist.plot(kind='barh', stacked=True, color=Visualizer.SENTIMENT_COLORS, figsize=(14, 10), edgecolor='black')
        plt.title(f'Sentiment Distribution for Top {top_n} Characters', fontsize=14)
        plt.xlabel('Proportion of Dialogues', fontsize=12)
        plt.ylabel('Character', fontsize=12)
        plt.legend(title='Sentiment')
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_interactive_interactions(df, interaction_dict, top_n_chars=15):
        """
        Plots an interactive network graph of character interactions.

        Args:
            df (pd.DataFrame): The main DataFrame with all data.
            interaction_dict (dict): Dictionary with co-occurrence counts.
            top_n_chars (int): Number of top characters to include in the graph.
        """
        # Get total dialogue counts for node sizing
        dialogue_counts = df['character'].value_counts()
        top_characters = dialogue_counts.nlargest(top_n_chars).index

        # Create a Pyvis network
        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=True)
        net.force_atlas_2based()

        # Add nodes (characters)
        for char in top_characters:
            node_size = int(dialogue_counts.get(char, 0))
            net.add_node(char, label=char, value=node_size, title=f"{char}: {node_size} dialogues")

        # Add edges (interactions)
        for key, weight in interaction_dict.items():
            nodes = key.split(', ')
            if len(nodes) == 2:
                char1, char2 = nodes
                # Only add edges between top characters
                if char1 in top_characters and char2 in top_characters:
                    net.add_edge(char1, char2, value=weight, title=f"Interactions: {weight}")

        # Generate and open the interactive HTML file
        filepath = "interactive_network.html"
        net.show(filepath)

        # Open the file in the default web browser
        webbrowser.open(f"file://{os.path.realpath(filepath)}")
        print(f"Interactive network graph saved to {filepath}")
