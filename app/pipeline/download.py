import streamlit as st
from app.visualizer import (
    sentiment_distribution,
    word_count_vs_complexity,
    personal_pronouns_barchart
)
from app.pdf_generator import export_analysis_to_pdf


def show_download_section(excel_path, df_result):
    """
    Renders the download section for Excel and PDF output files in the Streamlit app.

    Args:
        excel_path (str): File path to the Excel output file.
        df_result (DataFrame): Final processed DataFrame with analysis results.
    """
    st.markdown("### 📥 Download Output Files")

    # ---------------- Excel Download ----------------
    if excel_path and df_result is not None:
        try:
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="📥 Download Excel Output",
                    data=f,
                    file_name="Output_Data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        except FileNotFoundError:
            st.error("❌ Excel file not found.")
    else:
        st.warning("⚠️ Excel path or data not provided.")

    # ---------------- PDF Generation ----------------
    visuals = [
        ("📊 Sentiment Distribution", lambda df: sentiment_distribution(df)),
        ("🧠 Word Count vs Complexity", lambda df: word_count_vs_complexity(df)),
        ("🗣️ Personal Pronouns Barchart", lambda df: personal_pronouns_barchart(df)),
    ]


    try:
        with st.spinner("📄 Generating PDF Report..."):
            pdf_path = export_analysis_to_pdf(df_result, visuals)

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name="Article_Analysis_Report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"❌ Failed to generate PDF report: {e}")