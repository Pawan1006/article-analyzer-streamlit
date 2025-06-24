import re
import string
import yake
from nltk.corpus import stopwords
from nltk import download


stop_words = set(stopwords.words("english"))

# 🧹 Custom stopword sets
domain_stopwords = {
    "client background", "introduction", "section", "conclusion",
    "data", "result", "analysis"
}
contractions = {"'ll", "'re", "'ve", "'d", "n't", "'s", "'m"}

# 🔧 Text normalization
def normalize_text(text):
    return (
        text.replace("’", "'")
            .replace("‘", "'")
            .replace("“", '"')
            .replace("”", '"')
            .strip()
            .lower()
    )

# 🧠 Main Keyword Extraction
def extract_keywords_from_text(text, max_keywords=5, language="en"):
    """
    Extracts top meaningful keywords from a given text using YAKE.
    Filters out stopwords, punctuation, numbers, and domain-specific noise.

    Args:
        text (str): Input article/content text.
        max_keywords (int): Number of top keywords to return.
        language (str): Language code (default: 'en').

    Returns:
        List[str]: Cleaned list of keywords.
    """
    if not text or not isinstance(text, str):
        return []

    kw_extractor = yake.KeywordExtractor(lan=language, n=3, top=max_keywords * 5)
    raw_keywords = kw_extractor.extract_keywords(text)

    cleaned_keywords = []
    seen = set()

    for kw, _ in raw_keywords:
        kw_clean = normalize_text(kw)

        if (
            len(kw_clean) < 3 or
            kw_clean in stop_words or
            kw_clean in domain_stopwords or
            kw_clean in contractions or
            kw_clean in seen or
            kw_clean in string.punctuation or
            re.fullmatch(r"[\W_]+", kw_clean) or
            re.fullmatch(r"\d+", kw_clean)
        ):
            continue

        cleaned_keywords.append(kw_clean)
        seen.add(kw_clean)

        if len(cleaned_keywords) >= max_keywords:
            break

    return cleaned_keywords