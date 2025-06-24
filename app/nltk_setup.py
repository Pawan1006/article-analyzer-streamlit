import nltk

def ensure_nltk_resources():
    for resource in ["punkt", "stopwords", "vader_lexicon", "wordnet", "omw-1.4", "punkt_tab"]:
        try:
            nltk.data.find(resource)
        except LookupError:
            nltk.download(resource, quiet=True)