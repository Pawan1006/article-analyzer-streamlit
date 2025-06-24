import os
from collections import Counter
import streamlit as st
from app.keyword_extractor import extract_keywords_from_text


def compute_summary_insights(df_result):
    """
    Computes summary metrics and top keywords from the analyzed articles.

    Args:
        df_result (pd.DataFrame): DataFrame with article metrics.

    Returns:
        dict: Dictionary containing total count, polarity stats, and top keywords.
    """
    summary = {
        "total_articles": len(df_result),
        "avg_polarity": round(df_result["POLARITY SCORE"].mean(), 3),
        "positive_articles": (df_result["POLARITY SCORE"] > 0.1).sum(),
        "negative_articles": (df_result["POLARITY SCORE"] < -0.1).sum(),
        "neutral_articles": df_result[
            (df_result["POLARITY SCORE"] >= -0.1) & (df_result["POLARITY SCORE"] <= 0.1)
        ].shape[0],
    }

    # Collect keywords from each article file
    all_keywords = []
    for _, row in df_result.iterrows():
        file_path = f"extracted_articles/{row['URL_ID']}.txt"
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                keywords = extract_keywords_from_text(text)
                all_keywords.extend(keywords)
            except Exception:
                continue  # Skip corrupt files silently

    summary["top_keywords"] = Counter(all_keywords).most_common(10)
    return summary


def display_summary(df_result):
    """
    Displays high-level summary insights in the Streamlit interface.

    Args:
        df_result (pd.DataFrame): DataFrame containing the analysis results.
    """
    st.markdown("### 📌 Summary Insights")

    with st.expander("📊 High-Level Dataset Insights"):
        try:
            summary = compute_summary_insights(df_result)

            # Display core statistics
            st.markdown(f"- **Total Articles Analyzed**: `{summary['total_articles']}`")
            st.markdown(f"- **Average Polarity Score**: `{summary['avg_polarity']}`")
            st.markdown(f"- **Positive Articles**: `{summary['positive_articles']}`")
            st.markdown(f"- **Negative Articles**: `{summary['negative_articles']}`")
            st.markdown(f"- **Neutral Articles**: `{summary['neutral_articles']}`")

            # Display top keywords
            if summary["top_keywords"]:
                st.markdown("#### 🔑 Top 10 Common Keywords:")
                for kw, freq in summary["top_keywords"]:
                    st.markdown(f"- {kw} ({freq} times)")

        except Exception as e:
            st.error(f"❌ Could not compute summary: {e}")