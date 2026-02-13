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
    def plot_character_dialogues(df, top_n=20, show=True):
        sns.set(style="whitegrid")
        fig = plt.figure(figsize=(14, 10))

        # Ensure we are working with the top N characters
        top_characters = df.nlargest(top_n, 'count')

        # Create bar plot
        bars = plt.barh(top_characters['character'], top_characters['count'], color=sns.color_palette(Visualizer.PALETTE, n_colors=len(top_characters)), edgecolor='black')

        # Add value labels
        for bar in bars:
            plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width())}',
                     va='center', ha='left', fontsize=10, color='black')

        plt.xlabel('Number of Dialogues', fontsize=12)
        plt.ylabel('Character', fontsize=12)
        plt.title(f'Top {top_n} Characters by Dialogue Count', fontsize=14)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()

        if show:
            plt.show()
        return fig

    @staticmethod
    def plot_scenes_lines(df_scenes_lines, top_n=12, show=True):
        sns.set(style="whitegrid")
        fig, axes = plt.subplots(1, 2, figsize=(18, 10))

        # Plot Scene Count
        scenes = df_scenes_lines['# of Scenes'].nlargest(top_n)
        sns.barplot(x=scenes.values, y=scenes.index, ax=axes[0], palette=Visualizer.PALETTE)
        axes[0].set_title(f'Top {top_n} Characters by Scene Count', fontsize=14)
        axes[0].set_xlabel('Number of Scenes', fontsize=12)
        axes[0].set_ylabel('Character', fontsize=12)

        # Plot Lines Spoken
        lines_spoken = df_scenes_lines['# of lines spoken'].nlargest(top_n)
        sns.barplot(x=lines_spoken.values, y=lines_spoken.index, ax=axes[1], palette=Visualizer.PALETTE)
        axes[1].set_title(f'Top {top_n} Characters by Lines Spoken', fontsize=14)
        axes[1].set_xlabel('Number of Lines Spoken', fontsize=12)
        axes[1].set_ylabel('')

        plt.tight_layout()

        if show:
            plt.show()
        return fig

    @staticmethod
    def plot_sentiment_distribution(df, top_n=15, show=True):
        # Filter for top characters
        top_characters = df['character'].value_counts().nlargest(top_n).index
        df_top = df[df['character'].isin(top_characters)]

        # Calculate sentiment proportions
        sentiment_counts = pd.crosstab(df_top['character'], df_top['sentiment'])
        sentiment_dist = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0)

        # Plot
        fig, ax = plt.subplots(figsize=(14, 10))
        sentiment_dist.plot(kind='barh', stacked=True, color=[Visualizer.SENTIMENT_COLORS.get(x, 'blue') for x in sentiment_dist.columns], ax=ax, edgecolor='black')

        plt.title(f'Sentiment Distribution for Top {top_n} Characters', fontsize=14)
        plt.xlabel('Proportion of Dialogues', fontsize=12)
        plt.ylabel('Character', fontsize=12)
        plt.legend(title='Sentiment')
        plt.tight_layout()

        if show:
            plt.show()
        return fig

    @staticmethod
    def plot_interactive_interactions(df, interaction_dict, show=True):
        """
        Plots an interactive network graph of character interactions.

        Args:
            df (pd.DataFrame): The main DataFrame with all data.
            interaction_dict (dict): Dictionary with co-occurrence counts.
            show (bool): If True, opens the browser.
        """
        # Get total dialogue counts for node sizing
        dialogue_counts = df['character'].value_counts()
        top_characters = dialogue_counts.nlargest(15).index.tolist()

        # Create a Pyvis network
        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=False)
        # net.force_atlas_2based() # Optional layout algorithm

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

        # Generate the interactive HTML file
        filepath = "interactive_network.html"
        net.save_graph(filepath)
        print(f"Interactive network graph saved to {filepath}")

        if show:
            webbrowser.open(f"file://{os.path.realpath(filepath)}")

        return filepath

    @staticmethod
    def plot_sentiment_evolution(df_evolution, show=True):
        """
        Plots the evolution of sentiment proportions over episodes using a stacked area chart.

        Args:
            df_evolution (pd.DataFrame): DataFrame with 'episode' and columns 'POS', 'NEU', 'NEG'.
        """
        sns.set(style="whitegrid")
        fig = plt.figure(figsize=(16, 8))

        # Ensure columns are in a logical order for stacking: NEG (bottom), NEU (middle), POS (top)
        cols_to_plot = ['NEG', 'NEU', 'POS']
        colors = [Visualizer.SENTIMENT_COLORS[col] for col in cols_to_plot]

        # Plot stacked area chart
        plt.stackplot(df_evolution['episode'],
                      df_evolution['NEG'],
                      df_evolution['NEU'],
                      df_evolution['POS'],
                      labels=cols_to_plot,
                      colors=colors,
                      alpha=0.8)

        plt.title('Evolution of Sentiment Proportions Over Episodes', fontsize=16)
        plt.xlabel('Episode', fontsize=12)
        plt.ylabel('Proportion of Dialogues', fontsize=12)
        plt.legend(loc='upper left', title='Sentiment')
        plt.margins(0, 0) # Remove white space on edges
        plt.xticks(rotation=45)
        plt.tight_layout()

        if show:
            plt.show()
        return fig
