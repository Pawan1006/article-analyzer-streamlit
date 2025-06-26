import streamlit as st
import os
import uuid
from PIL import Image

from app.pdf_charts import (  # <-- Static matplotlib charts for PDF
    save_sentiment_distribution_matplotlib,
    save_word_count_vs_complexity_matplotlib,
    save_personal_pronouns_barchart_matplotlib
)
from app.pdf_generator import export_analysis_to_pdf


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

            # Generate a unique session ID
            if "session_id" not in st.session_state:
                st.session_state.session_id = str(uuid.uuid4())[:8]

            session_id = st.session_state.session_id
            os.makedirs("charts", exist_ok=True)

            # Generate and save matplotlib charts with unique filenames
            sentiment_path = save_sentiment_distribution_matplotlib(df_result, session_id)
            wc_path = save_word_count_vs_complexity_matplotlib(df_result, session_id)
            pronoun_path = save_personal_pronouns_barchart_matplotlib(df_result, session_id)

            # Dict of saved chart image paths
            charts = {
                "📊 Sentiment Distribution": sentiment_path,
                "🧠 Word Count vs Complexity": wc_path,
                "🗣️ Personal Pronouns Barchart": pronoun_path
            }

            # Generate PDF
            pdf_path = export_analysis_to_pdf(df_result, charts, input_path=sample_path, session_id=session_id)
            st.session_state.pdf_path = pdf_path

    else:
        pdf_path = st.session_state.pdf_path

    # ---------------- PDF Download Button ----------------
    try:
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name=os.path.basename(pdf_path),
                mime="application/pdf"
            )

        # Optional Cleanup: delete charts and PDF
        for path in list(st.session_state.get("pdf_cleanup_files", [])):
            if os.path.exists(path):
                os.remove(path)

    except Exception as e:
        st.error(f"❌ Failed to generate PDF report: {e}")