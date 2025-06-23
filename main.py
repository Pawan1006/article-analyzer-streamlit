import streamlit as st
from app.ui.upload import handle_file_upload
from app.pipeline.extract import extract_articles_from_file
from app.pipeline.analyze import analyze_and_cache_results
from app.pipeline.summary import display_summary
from app.pipeline.visuals import show_visual_tabs
from app.pipeline.download import show_download_section

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
    df_result = extract_articles_from_file(sample_path)

    if df_result is not None:
        # ---------------- Step 3: Analyze Articles ----------------
        df_result = analyze_and_cache_results(sample_path, df_result)
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