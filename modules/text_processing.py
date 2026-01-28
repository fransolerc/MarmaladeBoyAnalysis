import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from pysentimiento import create_analyzer

# Note: Ensure NLTK data is downloaded before running.
# You can download it by running the following in a Python interpreter:
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

class TextProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words("spanish"))
        self.lemma = WordNetLemmatizer()
        # Initialize the sentiment analyzer
        self.sentiment_analyzer = create_analyzer(task="sentiment", lang="es")

    def _clean_text(self, text):
        text = re.sub(r"[^A-Za-z_ÑñÁáÉéÍíÓóÚú]+", " ", text).lower()
        tokens = text.split()
        tokens = [word for word in tokens if word not in self.stop_words]
        tokens = [self.lemma.lemmatize(word) for word in tokens]
        return " ".join(tokens)

    def analyze_sentiment(self, df):
        """
        Analyzes the sentiment of each dialogue.
        """
        # The analyzer returns a prediction object. We are interested in the output attribute.
        df["sentiment"] = df["dialogue"].apply(lambda text: self.sentiment_analyzer.predict(text).output)
        return df

    def process_text(self, df):
        # Use .apply for vectorized text processing
        df["new_script"] = df["dialogue"].apply(self._clean_text)
        # Add sentiment analysis to the pipeline
        df = self.analyze_sentiment(df)
        return df

    @staticmethod
    def analyze_frequencies(description_list):
        dist = FreqDist(description_list)
        return dist.most_common(50)

    @staticmethod
    def vectorize_text(texts, max_features=50):
        try:
            count_vectorizer = CountVectorizer(max_features=max_features, stop_words="spanish")
            count_vectorizer.fit_transform(texts).toarray()
            return count_vectorizer.get_feature_names_out()
        except Exception as e:
            print(f"Text vectorization error: {e}")
            return []
