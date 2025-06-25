import streamlit as st
from app.ui.upload import handle_file_upload
from app.pipeline.extract import extract_articles_from_file
from app.pipeline.analyze import analyze_and_cache_results
from app.pipeline.summary import display_summary
from app.pipeline.visuals import show_visual_tabs
from app.pipeline.download import show_download_section
from app.utils import clear_old_charts 

# ---------------------- App Configuration ----------------------
st.set_page_config(
    page_title="Article Analyzer with Visual Insights",
    layout="wide"
)
st.title("📰 Advanced Article Analyzer with Visual Insights")

# ---------------------- Step 1: Upload Input ----------------------
sample_path = handle_file_upload()

# ---------------------- Step 2: Article Extraction ----------------------
if sample_path:
    # Check if new file uploaded or no previous result
    if (
        "df_result" not in st.session_state or
        st.session_state.get("last_file_path") != sample_path
    ):
        clear_old_charts() # clean old charts
        df_result = extract_articles_from_file(sample_path)
        if df_result is not None:
            df_result = analyze_and_cache_results(sample_path, df_result)
            st.session_state.df_result = df_result
            st.session_state.last_file_path = sample_path
    else:
        df_result = st.session_state.df_result

    if df_result is not None:
        st.success("✅ Article analysis complete")
        st.markdown("---")

        # ---------------- Step 4: Display Summary ----------------
        display_summary(df_result)
        st.markdown("---")

        # ---------------- Step 5: Show Visualizations ----------------
        show_visual_tabs(df_result)
        st.markdown("---")

        # ---------------- Step 6: Download Processed File ----------------
        show_download_section("output/Output Data Structure.xlsx", df_result)

        st.caption("📍 Built with ❤️ by Pawan | Powered by Streamlit")