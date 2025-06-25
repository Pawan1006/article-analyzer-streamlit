import streamlit as st
import os
from app.visualizer import (
    sentiment_distribution,
    word_count_vs_complexity,
    personal_pronouns_barchart
)
from app.pdf_generator import export_analysis_to_pdf
from app.visualizer import save_plotly_as_png

def show_download_section(excel_path, df_result, sample_path):
    """
    Renders the download section for Excel and PDF output files in the Streamlit app.
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
    if "pdf_path" not in st.session_state:
        with st.spinner("📄 Generating PDF Report..."):
            # Only generate charts once per session
            charts = {
                "📊 Sentiment Distribution": save_plotly_as_png(sentiment_distribution(df_result), "sentiment_distribution"),
                "🧠 Word Count vs Complexity": save_plotly_as_png(word_count_vs_complexity(df_result), "word_count_vs_complexity"),
                "🗣️ Personal Pronouns Barchart": save_plotly_as_png(personal_pronouns_barchart(df_result), "personal_pronouns_barchart")
            }
            # Export to PDF and store path in session
            pdf_path = export_analysis_to_pdf(df_result, charts, input_path=sample_path)
            st.session_state.pdf_path = pdf_path
    else:
        pdf_path = st.session_state.pdf_path

    try:
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"❌ Failed to generate PDF report: {e}")