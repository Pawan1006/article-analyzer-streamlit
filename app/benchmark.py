import os
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from rake_nltk import Rake
import yake
import textstat
import nltk

# 📦 Ensure VADER lexicon is available
try:
    nltk.data.find('sentiment/vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

# 🔍 Sentiment Benchmark: TextBlob vs VADER
def benchmark_sentiments(df, folder="extracted_articles", top_n=5):
    results = []

    for _, row in df.head(top_n).iterrows():
        url_id = row['URL_ID']
        file_path = os.path.join(folder, f"{url_id}.txt")

        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            blob_score = TextBlob(text).sentiment.polarity
            vader_score = SentimentIntensityAnalyzer().polarity_scores(text)['compound']

            results.append({
                "URL_ID": url_id,
                "TextBlob": round(blob_score, 3),
                "VADER": round(vader_score, 3)
            })

        except Exception as e:
            print(f"Error in sentiment benchmark for {url_id}: {e}")

    return results


# 📚 Readability Benchmark: FOG vs Flesch Reading Ease
def benchmark_readability(df, folder="extracted_articles", top_n=5):
    results = []

    for _, row in df.head(top_n).iterrows():
        url_id = row['URL_ID']
        file_path = os.path.join(folder, f"{url_id}.txt")

        if not os.path.exists(file_path):
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            fog_score = textstat.gunning_fog(text)
            flesch_score = textstat.flesch_reading_ease(text)

            results.append({
                "URL_ID": url_id,
                "FOG": round(fog_score, 2),
                "Flesch": round(flesch_score, 2)
            })

        except Exception as e:
            print(f"Error in readability benchmark for {url_id}: {e}")

    return results