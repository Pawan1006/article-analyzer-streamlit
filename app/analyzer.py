import os
import re
import pandas as pd
import streamlit as st
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk

from .utils import load_input_excel, count_syllables

# 🛡 Ensure required NLTK resources
from .nltk_setup import ensure_nltk_resources

ensure_nltk_resources()
stop_words = set(stopwords.words("english"))

# 🔍 Personal pronoun counter
def count_personal_pronouns(text):
    words = re.findall(r'\b\w+\b', text)
    count = 0
    for word in words:
        if word == 'I':
            count += 1
        elif word.lower() in ['we', 'my', 'ours', 'us'] and word != 'US':
            count += 1
    return count

# 🔬 Main analysis pipeline
@st.cache_data
def analyze_articles(path):
    df = load_input_excel(path)
    output_data = []
    invalid_rows = []

    for _, row in df.iterrows():
        url_id = row.get("URL_ID")
        url = row.get("URL")

        if pd.isna(url_id) or pd.isna(url):
            invalid_rows.append(row)
            continue

        file_path = f"extracted_articles/{url_id}.txt"
        if not os.path.exists(file_path):
            st.warning(f"⚠️ File not found for URL_ID {url_id}. Skipping.")
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Preprocessing
            blob = TextBlob(text)
            words = word_tokenize(text)
            sentences = sent_tokenize(text)

            clean_words = [w.lower() for w in words if w.isalpha() and w.lower() not in stop_words]
            word_count = len(clean_words)
            complex_words = [w for w in clean_words if count_syllables(w) > 2]
            complex_word_count = len(complex_words)

            # Metrics
            polarity = round(blob.sentiment.polarity, 3)
            subjectivity = round(blob.sentiment.subjectivity, 3)
            avg_sentence_len = round(word_count / max(len(sentences), 1), 3)
            percent_complex = round(complex_word_count / max(word_count, 1), 3)
            fog_index = round(0.4 * (avg_sentence_len + percent_complex), 3)
            syll_per_word = round(sum(count_syllables(w) for w in clean_words) / max(word_count, 1), 3)
            avg_word_len = round(sum(len(w) for w in clean_words) / max(word_count, 1), 3)
            pronouns = count_personal_pronouns(text)

            output_data.append([
                url_id, url, polarity, subjectivity, avg_sentence_len,
                percent_complex, fog_index,
                complex_word_count, word_count, syll_per_word,
                pronouns, avg_word_len
            ])

        except Exception as e:
            st.error(f"❌ Failed to analyze article {url_id}: {e}")

    # Save output
    df_out = pd.DataFrame(output_data, columns=[
        "URL_ID", "URL", "POLARITY SCORE", "SUBJECTIVITY SCORE", "AVG SENTENCE LENGTH",
        "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX",
        "COMPLEX WORD COUNT", "WORD COUNT", "SYLLABLE PER WORD",
        "PERSONAL PRONOUNS", "AVG WORD LENGTH"
    ])

    os.makedirs("output", exist_ok=True)
    df_out.to_excel("output/Output Data Structure.xlsx", index=False)

    if invalid_rows:
        st.warning(f"⚠️ Skipped {len(invalid_rows)} row(s) due to missing URL_ID or URL.")

    return df_out