import os
import streamlit as st
from app.visualizer import (
    sentiment_distribution,
    word_count_vs_complexity,
    personal_pronouns_barchart,
    generate_wordcloud,
    plot_sentiment_comparison,
    plot_readability_comparison
)
from app.keyword_extractor import extract_keywords_from_text
from app.benchmark import benchmark_sentiments, benchmark_readability


def show_visual_tabs(df_result):
    """Displays all visualization tabs for article analysis."""
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Table", "📈 Visuals", "🔑 Keywords", "🧪 Benchmarks"
    ])

    # --- 📋 Data Table Tab ---
    with tab1:
        st.dataframe(df_result)

    # --- 📈 Visual Charts Tab ---
    with tab2:
        st.subheader("📊 Sentiment Distribution")
        st.plotly_chart(sentiment_distribution(df_result), use_container_width=True)

        st.subheader("🧠 Word Count vs. Complexity")
        st.plotly_chart(word_count_vs_complexity(df_result), use_container_width=True)

        st.subheader("🗣️ Personal Pronouns Heatmap")
        st.plotly_chart(personal_pronouns_barchart(df_result), use_container_width=True)

    # --- 🔑 Keywords Tab ---
    with tab3:
        st.subheader("🔎 Top 5 Keywords per Article")

        all_keywords = []
        for _, row in df_result.iterrows():
            file_path = f"extracted_articles/{row['URL_ID']}.txt"
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read()
                    keywords = extract_keywords_from_text(text)
                    all_keywords.extend(keywords)

                    # Display keywords as styled chips
                    with st.expander(f"📰 Article ID: {row['URL_ID']}"):
                        styled = " ".join([
                            f'<span style="background-color:#e0f3ff; color:#333; '
                            f'padding:5px 10px; border-radius:12px; margin:4px; '
                            f'display:inline-block;">{kw}</span>'
                            for kw in keywords
                        ])
                        st.markdown(styled, unsafe_allow_html=True)
                except Exception:
                    continue

        st.subheader("☁️ Common Keyword WordCloud")
        st.pyplot(generate_wordcloud(all_keywords))

    # --- 🧪 Benchmark Tab ---
    with tab4:
        st.subheader("📊 Benchmarking Tools (TextBlob vs VADER, FOG vs Flesch)")

        top_n = st.slider("Select number of articles to benchmark:", 3, 20, 5)

        sentiment_data = benchmark_sentiments(df_result, top_n=top_n)
        readability_data = benchmark_readability(df_result, top_n=top_n)

        # Optional insights
        with st.expander("ℹ️ Why Benchmarks?"):
            st.markdown("""
            - Benchmarking shows how different tools interpret text.
            - TextBlob vs VADER contrast rule-based and ML-based sentiment engines.
            - FOG vs Flesch Grade assess readability from different lenses.
            - Helps in validating your NLP pipeline with confidence.
            """)

        if sentiment_data:
            st.plotly_chart(plot_sentiment_comparison(sentiment_data), use_container_width=True)
        else:
            st.warning("⚠️ No sentiment data to visualize.")

        if readability_data:
            st.plotly_chart(plot_readability_comparison(readability_data), use_container_width=True)
        else:
            st.warning("⚠️ No readability data to visualize.")