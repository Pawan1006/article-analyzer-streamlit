import os
import pandas as pd
import streamlit as st
from app.visualizer import (
    sentiment_distribution,
    word_count_vs_complexity,
    personal_pronouns_barchart,
    generate_wordcloud,
    plot_sentiment_comparison,
    plot_readability_comparison,
    plot_sentiment_difference,
    plot_sentiment_agreement_pie
)
from app.keyword_extractor import extract_keywords_from_text
from app.benchmark import benchmark_sentiments, benchmark_readability, benchmarking_tools_page


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

        st.subheader("🗣️ Personal Pronouns BarChart")
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
                    keywords = extract_keywords_from_text(text, max_keywords=5)
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

        with st.expander("ℹ️ Why Benchmarks?"):
            st.markdown("""
            - Benchmarking helps validate your NLP pipeline.
            - TextBlob vs VADER → compare ML vs rule-based sentiment.
            - FOG vs Flesch → test readability from complexity and ease perspectives.
            """)

        # Run benchmarking directly with sliders
        top_n = st.slider("📌 Select number of articles to benchmark:", min_value=2, max_value=20, value=5)

        sentiment_results = benchmark_sentiments(df_result, top_n=top_n)
        readability_results = benchmark_readability(df_result, top_n=top_n)

        if sentiment_results:
            st.subheader("🧪 Sentiment Comparison")
            st.plotly_chart(plot_sentiment_comparison(sentiment_results), use_container_width=True)
            st.plotly_chart(plot_sentiment_difference(sentiment_results), use_container_width=True)

            sentiment_df = pd.DataFrame(sentiment_results)

            correlation = sentiment_df[["TextBlob", "VADER"]].corr().iloc[0, 1]
            st.plotly_chart(plot_sentiment_agreement_pie(sentiment_df), use_container_width=True)

            
            with st.expander("📋 Detailed Sentiment Table"):
                st.dataframe(sentiment_df, use_container_width=True)
                csv = sentiment_df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download Sentiment CSV", csv, "sentiment_benchmark.csv", "text/csv")
        else:
            st.warning("⚠️ No sentiment data available.")

        st.markdown("---")

        if readability_results:
            st.subheader("📚 Readability Comparison")
            st.plotly_chart(plot_readability_comparison(readability_results), use_container_width=True)

            readability_df = pd.DataFrame(readability_results)
            with st.expander("📋 Detailed Readability Table"):
                st.dataframe(readability_df, use_container_width=True)
                csv_readability = readability_df.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download Readability CSV", csv_readability, "readability_benchmark.csv", "text/csv")
        else:
            st.warning("⚠️ No readability data available.")