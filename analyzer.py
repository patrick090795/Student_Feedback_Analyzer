"""Analyzer module for Student Feedback Analyzer

Provides:
- clean_text(text): basic text cleaning
- sentiment_scores(comments): returns list of polarity scores and summary
- compute_correlations(df, sentiment_col, rating_cols): safe correlation computation
- generate_wordcloud(text, output_path=None): create and optionally save a wordcloud image
- interpret_results(sentiments, ratings): simple human-readable interpretations

This is a lightweight refactor of the original notebook script into reusable functions.
"""

import re
import string
from typing import List, Tuple, Dict, Optional

import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from wordcloud import WordCloud


# Ensure required NLTK resources are available. If not, download them at runtime.
def _ensure_nltk_resources():
    resources = {
        'punkt': 'tokenizers/punkt',
        'punkt_tab': 'tokenizers/punkt_tab',
        'wordnet': 'corpora/wordnet',
        'stopwords': 'corpora/stopwords',
    }
    for name, path in resources.items():
        try:
            nltk.data.find(path)
        except LookupError:
            try:
                nltk.download(name)
            except Exception:
                # If download fails, continue and let callers handle missing resources
                pass


# Call once on import
_ensure_nltk_resources()

# NOTE: Ensure NLTK resources are downloaded by the consumer script if needed.

_lemmatizer = WordNetLemmatizer()
try:
    _stop_words = set(stopwords.words('english'))
except Exception:
    _stop_words = set()


def clean_text(text: str) -> str:
    """Clean a single text string: lowercase, remove punctuation, tokenize, remove stopwords, lemmatize.

    Args:
        text: raw input string
    Returns:
        cleaned single-line string
    """
    if not isinstance(text, str):
        text = str(text)
    text = text.lower()
    text = text.strip()
    # remove URLs and emails
    text = re.sub(r"https?://\S+|www\.\S+|\S+@\S+", "", text)
    # remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
    tokens = [t for t in tokens if t.isalpha() and t not in _stop_words]
    try:
        tokens = [_lemmatizer.lemmatize(t) for t in tokens]
    except Exception:
        pass
    return " ".join(tokens)


def sentiment_scores(comments: List[str]) -> Tuple[List[float], Dict[str, float]]:
    """Compute polarity for a list of comments and return basic summary.

    Returns (polarity_list, summary) where summary contains mean, median, pos/neg/neu proportions.
    """
    polarities = []
    for c in comments:
        if pd.isna(c):
            polarities.append(0.0)
            continue
        blob = TextBlob(str(c))
        polarities.append(blob.sentiment.polarity)
    arr = np.array(polarities)
    summary = {
        'mean': float(np.nanmean(arr)),
        'median': float(np.nanmedian(arr)),
        'count': int(len(arr)),
        'positive_pct': float((arr > 0).sum() / len(arr)) if len(arr) else 0.0,
        'negative_pct': float((arr < 0).sum() / len(arr)) if len(arr) else 0.0,
        'neutral_pct': float((arr == 0).sum() / len(arr)) if len(arr) else 0.0,
    }
    return polarities, summary


def compute_correlations(df: pd.DataFrame, sentiment_col: str, rating_cols: List[str]) -> Dict[str, Optional[float]]:
    """Compute Pearson correlations between sentiment_col and each column in rating_cols.

    Returns a dict column_name -> correlation (None if cannot compute).
    """
    results = {}
    for col in rating_cols:
        try:
            series_a = pd.to_numeric(df[sentiment_col], errors='coerce')
            series_b = pd.to_numeric(df[col], errors='coerce')
            valid = series_a.notna() & series_b.notna()
            if valid.sum() < 2:
                results[col] = None
                continue
            corr = np.corrcoef(series_a[valid], series_b[valid])[0, 1]
            results[col] = float(corr)
        except Exception:
            results[col] = None
    return results


def generate_wordcloud(text: str, output_path: Optional[str] = None, max_words: int = 100) -> WordCloud:
    """Generate a wordcloud object for the provided text. Optionally save to output_path.

    Returns the WordCloud instance.
    """
    wc = WordCloud(max_words=max_words, background_color='white')
    wc.generate(text)
    if output_path:
        wc.to_file(output_path)
    return wc


def interpret_results(polarities: List[float], ratings: Optional[List[float]] = None) -> List[str]:
    """Provide simple textual interpretations based on polarities (and optional ratings).

    Example outputs:
      - "Overall sentiment is positive with mean polarity X"
      - "Items with very negative sentiment (below -0.5): N"
    """
    texts = []
    if not polarities:
        return ["No comments provided."]
    arr = np.array(polarities)
    mean = float(np.nanmean(arr))
    texts.append(f"Overall mean polarity: {mean:.3f}")
    pos = (arr > 0).sum()
    neg = (arr < 0).sum()
    neu = (arr == 0).sum()
    texts.append(f"Positive: {pos}, Negative: {neg}, Neutral: {neu} (out of {len(arr)})")
    very_neg = (arr <= -0.5).sum()
    very_pos = (arr >= 0.5).sum()
    if very_neg:
        texts.append(f"There are {very_neg} strongly negative comments (<= -0.5). Consider investigating common themes.")
    if very_pos:
        texts.append(f"There are {very_pos} strongly positive comments (>= 0.5). These can be highlighted.")

    # If ratings provided, compare trend
    if ratings is not None:
        try:
            r = np.array([float(x) for x in ratings])
            if len(r) == len(arr):
                corr = np.corrcoef(arr, r)[0, 1]
                texts.append(f"Correlation between sentiment and provided ratings: {corr:.3f}")
        except Exception:
            pass

    return texts
