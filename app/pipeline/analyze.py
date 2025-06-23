import streamlit as st
from app.analyzer import analyze_articles

@st.cache_data(show_spinner=False)
def analyze_and_cache_results(path, df):
    """
    Analyze extracted articles and cache the result.

    Args:
        path (str): Path to the uploaded Excel file.
        df (DataFrame): DataFrame containing extracted URL_IDs.

    Returns:
        DataFrame: Analyzed article metrics.
    """
    st.markdown("### 📊 Step 2: Analyzing Articles")

    with st.spinner("🔍 Analyzing article content..."):
        result_df = analyze_articles(path)

        # Ensure URL_ID is treated as string (critical for joining/tracking)
        result_df["URL_ID"] = result_df["URL_ID"].astype(str)

    return result_df
