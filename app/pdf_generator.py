import os
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Image, PageBreak, KeepTogether
)
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape, letter
from app.pipeline.summary import compute_summary_insights


@st.cache_data
def export_analysis_to_pdf(df, chart_paths_dict, input_path, session_id=None, output_dir="output"):
    """
    Generate a PDF report summarizing article analysis with pre-saved chart images.

    Args:
        df (pd.DataFrame): Final result dataframe.
        chart_paths_dict (dict): Dict with {title: image_path} for pre-saved chart PNGs.
        input_path (str): Path of uploaded input file (used for naming output).
        session_id (str): Unique ID to prevent file collisions (optional).
        output_dir (str): Directory to store the generated PDF.
        
    Returns:
        str: Full path to the generated PDF.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs("charts", exist_ok=True)

    filename_base = os.path.splitext(os.path.basename(input_path))[0]  # sample_input
    if session_id:
        filename_base = f"{filename_base}_{session_id}"

    # Clean up previous PDFs for same session or file (optional but good hygiene)
    for file in os.listdir(output_dir):
        if filename_base in file and file.endswith("_analysis_summary.pdf"):
            try:
                os.remove(os.path.join(output_dir, file))
            except Exception as e:
                print(f"⚠️ Could not delete {file}: {e}")

    output_path = os.path.join(output_dir, f"{filename_base}_analysis_summary.pdf")

    # Begin PDF content
    doc = SimpleDocTemplate(output_path, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    elements = []

    # Page 1: Summary
    summary = compute_summary_insights(df)
    elements.append(Paragraph("--Article Analysis Summary--", styles["Title"]))
    elements.append(Spacer(1, 12))

    highlights = [
        f"Total Articles Analyzed: {summary['total_articles']}",
        f"Average Polarity Score: {summary['avg_polarity']}",
        f"Positive Articles: {summary['positive_articles']}",
        f"Negative Articles: {summary['negative_articles']}",
        f"Neutral Articles: {summary['neutral_articles']}"
    ]

    elements.append(Paragraph("Highlights -", styles["Heading3"]))
    for item in highlights:
        elements.append(Paragraph(item, styles["Normal"]))
    elements.append(Spacer(1, 12))

    if summary.get("top_keywords"):
        elements.append(Paragraph("Top 10 Common Keywords -", styles["Heading3"]))
        for kw, freq in summary["top_keywords"]:
            elements.append(Paragraph(f"• {kw} ({freq} times)", styles["Normal"]))
    elements.append(PageBreak())

    # Page 2: Metrics Table
    df_metric = df.drop(columns=["URL"]).set_index("URL_ID").T.reset_index()
    df_metric.columns = ["Metric"] + [f"URL_ID-{col}" for col in df_metric.columns[1:]]

    table_data = [df_metric.columns.tolist()] + df_metric.values.tolist()
    table = Table(table_data, repeatRows=1, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))

    elements.append(Paragraph("Article Metrics Table -", styles["Heading2"]))
    elements.append(Spacer(1, 6))
    elements.append(table)
    elements.append(PageBreak())

    # Pages 3+: Charts
    for title, img_path in chart_paths_dict.items():
        if os.path.exists(img_path):
            elements.append(KeepTogether([
                Paragraph(title, styles["Heading2"]),
                Spacer(1, 6),
                Image(img_path, width=500, height=300),
                Spacer(1, 18)
            ]))
        else:
            elements.append(Paragraph(f"⚠️ Could not load chart for '{title}'", styles["Normal"]))
            elements.append(Spacer(1, 12))

    doc.build(elements)
    return output_path