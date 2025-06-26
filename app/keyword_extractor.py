import re
import string
import yake
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

from .nltk_setup import ensure_nltk_resources
ensure_nltk_resources()

# Initialize resources
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# 🧹 Custom stopword extensions
domain_stopwords = {
    "client background", "introduction", "section", "conclusion",
    "data", "result", "analysis"
}
contractions = {"'ll", "'re", "'ve", "'d", "n't", "'s", "'m"}


# 🔧 Utility: Normalize individual keyword
def normalize_keyword(phrase):
    phrase = phrase.lower().strip()
    phrase = phrase.translate(str.maketrans('', '', string.punctuation))
    phrase = re.sub(r'\s+', ' ', phrase)  # Normalize extra spaces
    return phrase


# 🔁 Utility: Lemmatize and remove stopwords from phrase
def clean_and_filter_phrase(phrase):
    tokens = nltk.word_tokenize(phrase)
    lemmatized = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in stop_words and word not in contractions and word.isalpha()
    ]
    return " ".join(lemmatized)


# 🧠 Main: Robust Keyword Extractor
def extract_keywords_from_text(text, max_keywords=10, language="en", min_char_length=3, min_word_count=1, return_with_freq=False):
    """
    Extracts top keywords using YAKE, with cleaning, de-duplication, and lemmatization.

    Args:
        text (str): Input text.
        max_keywords (int): Maximum number of keywords to return.
        language (str): Language code.
        min_char_length (int): Minimum character length for keyword.
        min_word_count (int): Minimum number of words in phrase.
        return_with_freq (bool): Return (keyword, freq) pairs if True.

    Returns:
        List[str] or List[Tuple[str, int]]: Cleaned keywords.
    """
    if not text or not isinstance(text, str):
        return []

    text = normalize_keyword(text)

    kw_extractor = yake.KeywordExtractor(lan=language, n=2, top=max_keywords * 4)
    raw_keywords = kw_extractor.extract_keywords(text)

    seen = set()
    keyword_freq = defaultdict(int)

    for kw, score in raw_keywords:
        kw_norm = normalize_keyword(kw)

        if (
            len(kw_norm) < min_char_length or
            kw_norm in stop_words or
            kw_norm in domain_stopwords or
            kw_norm in contractions or
            re.fullmatch(r"[\W_]+", kw_norm) or
            re.fullmatch(r"\d+", kw_norm)
        ):
            continue

        # Lemmatize and tokenize
        cleaned_phrase = clean_and_filter_phrase(kw_norm)

        if not cleaned_phrase or cleaned_phrase in seen:
            continue

        # Apply phrase-level filters
        if len(cleaned_phrase.split()) < min_word_count:
            continue

        seen.add(cleaned_phrase)
        keyword_freq[cleaned_phrase] += 1

        if len(keyword_freq) >= max_keywords:
            break

    return (
        sorted(keyword_freq.items(), key=lambda x: -x[1]) if return_with_freq
        else list(keyword_freq.keys())
    )