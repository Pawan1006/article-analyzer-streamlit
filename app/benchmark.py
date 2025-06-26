import os
import streamlit as st
import pandas as pd
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import textstat

from app.nltk_setup import ensure_nltk_resources
ensure_nltk_resources()

from app.visualizer import (
    plot_sentiment_comparison,
    plot_sentiment_difference,
    plot_sentiment_agreement_pie,   # ✅ Moved pie here
    plot_readability_comparison
)

# ---------------- Utility ----------------
def classify_sentiment(score):
    if score > 0.1:
        return "Positive"
    elif score < -0.1:
        return "Negative"
    else:
        return "Neutral"

# ---------------- Sentiment Benchmark ----------------
def benchmark_sentiments(df, folder="extracted_articles", top_n=5):
    results = []
    sia = SentimentIntensityAnalyzer()

    for _, row in df.head(top_n).iterrows():
        url_id = row['URL_ID']
        file_path = os.path.join(folder, f"{url_id}.txt")
        if not os.path.exists(file_path):
            st.warning(f"⚠️ Missing file for article {url_id}")
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            blob_score = round(TextBlob(text).sentiment.polarity, 3)
            vader_score = round(sia.polarity_scores(text)['compound'], 3)
            diff = round(vader_score - blob_score, 3)

            blob_label = classify_sentiment(blob_score)
            vader_label = classify_sentiment(vader_score)
            agreement = "Agree" if blob_label == vader_label else "Disagree"

            results.append({
                "URL_ID": url_id,
                "TextBlob": blob_score,
                "VADER": vader_score,
                "Difference": diff,
                "Agreement": agreement
            })

        except Exception as e:
            st.error(f"⚠️ Error processing {url_id}: {e}")

    return results

# ---------------- Readability Benchmark ----------------
def benchmark_readability(df, folder="extracted_articles", top_n=5):
    results = []

    for _, row in df.head(top_n).iterrows():
        url_id = row['URL_ID']
        file_path = os.path.join(folder, f"{url_id}.txt")
        if not os.path.exists(file_path):
            st.warning(f"⚠️ Missing file for article {url_id}")
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            fog_score = round(textstat.gunning_fog(text), 2)
            flesch_score = round(textstat.flesch_reading_ease(text), 2)

            results.append({
                "URL_ID": url_id,
                "FOG": fog_score,
                "Flesch": flesch_score
            })

        except Exception as e:
            st.error(f"⚠️ Error processing {url_id}: {e}")

    return results

# ---------------- Streamlit Benchmark Page ----------------
def benchmarking_tools_page(df_result):
    with st.expander("ℹ️ Why Benchmarks?"):
        st.markdown("""
        - Benchmarking helps validate your NLP pipeline.
        - TextBlob vs VADER → compare ML vs rule-based sentiment.
        - FOG vs Flesch → test readability from complexity and ease perspectives.
        """)

    top_n = st.slider("📌 Select number of articles to benchmark:", min_value=2, max_value=20, value=5)

    sentiment_results = benchmark_sentiments(df_result, top_n=top_n)
    readability_results = benchmark_readability(df_result, top_n=top_n)

    # -------- Sentiment Section --------
    if sentiment_results:
        st.subheader("🧪 Sentiment Comparison")
        sentiment_df = pd.DataFrame(sentiment_results)

        st.plotly_chart(plot_sentiment_comparison(sentiment_results), use_container_width=True)
        st.plotly_chart(plot_sentiment_difference(sentiment_results), use_container_width=True)
        st.plotly_chart(plot_sentiment_agreement_pie(sentiment_df), use_container_width=True)

        with st.expander("📋 Detailed Sentiment Table"):
            st.dataframe(sentiment_df, use_container_width=True)
            csv = sentiment_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Sentiment CSV", csv, "sentiment_benchmark.csv", "text/csv")
    else:
        st.warning("⚠️ No sentiment data available.")

    st.markdown("---")

    # -------- Readability Section --------
    if readability_results:
        st.subheader("📚 Readability Comparison")
        readability_df = pd.DataFrame(readability_results)

        st.plotly_chart(plot_readability_comparison(readability_results), use_container_width=True)

        with st.expander("📋 Detailed Readability Table"):
            st.dataframe(readability_df, use_container_width=True)
            csv_readability = readability_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Readability CSV", csv_readability, "readability_benchmark.csv", "text/csv")
    else:
        st.warning("⚠️ No readability data available.")