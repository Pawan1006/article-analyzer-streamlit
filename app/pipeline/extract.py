import streamlit as st
import pandas as pd
from app.scraper import extract_articles  # function should accept (url_id, url)


def extract_articles_from_file(path):
    """
    Extracts articles from the URLs listed in the uploaded Excel file.

    Args:
        path (str): Path to the uploaded Excel file.

    Returns:
        DataFrame: The original dataframe with URL_IDs and URLs, or None on failure.
    """
    try:
        # Load and sanitize data
        df = pd.read_excel(path)
        df["URL_ID"] = df["URL_ID"].astype(str)
        df.to_excel(path, index=False)

        st.markdown("### 🧪 Step 1: Extracting Articles")
        status_list = []
        extracted_count = 0

        # Spinner while processing
        with st.spinner("⏳ Extracting all articles..."):
            for _, row in df.iterrows():
                url_id, url = row["URL_ID"], row["URL"]
                success, msg = extract_articles(url_id, url)
                if success:
                    extracted_count += 1
                status_list.append((url_id, msg))

        st.success(f"✅ Extraction complete: {extracted_count}/{len(df)} articles extracted.")

        # Show extraction results
        with st.expander("🗂️ Extraction Summary"):
            result_df = pd.DataFrame(status_list, columns=["URL_ID", "Status"])
            st.dataframe(result_df)

        return df

    except Exception as e:
        st.error(f"❌ Failed to extract articles: {e}")
        return None