import streamlit as st
import pandas as pd
import os

@st.cache_data
def generate_sample_file():
    """Creates and caches a sample input Excel file."""
    df = pd.DataFrame({
        "URL_ID": ["101", "102", "103"],
        "URL": [
            "https://realpython.com/tutorials/web-dev/",
            "https://python.land/introduction-to-python",
            "https://en.wikipedia.org/wiki/Natural_language_processing"
        ]
    })
    os.makedirs("input", exist_ok=True)
    sample_path = "input/sample_input.xlsx"
    df.to_excel(sample_path, index=False)
    return sample_path


def handle_file_upload():
    """Handles user file upload and sample input toggle."""
    st.markdown("### 📂 Upload Your Data File")
    st.caption("Accepted formats: `.xlsx` or `.csv` with headers: `URL_ID`, `URL`")

    # 👉 Provide sample download option
    sample_path = generate_sample_file()
    with open(sample_path, "rb") as f:
        st.download_button(
            label="📄 Download Sample Input File",
            data=f,
            file_name="sample_input.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # 👉 Option to use sample file directly
    use_sample = st.checkbox("✅ Use sample input file", value=False)
    if use_sample:
        st.success("Using sample input file.")
        return sample_path

    # 👉 Upload user file
    uploaded_file = st.file_uploader("Upload your file", type=["xlsx", "csv"])
    if uploaded_file:
        upload_dir = "input"
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
        st.success(f"Uploaded: `{uploaded_file.name}`")
        return save_path

    return None