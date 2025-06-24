import os
import tempfile
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    Image, PageBreak, KeepTogether
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape, letter

from app.pipeline.summary import compute_summary_insights


def export_analysis_to_pdf(df, visual_funcs, output_path="output/analysis_summary.pdf"):
    """
    Exports a full PDF report containing:
    1. Summary insights
    2. Vertical metrics table
    3. Charts from visual functions

    Args:
        df (pd.DataFrame): Resultant DataFrame after analysis.
        visual_funcs (list): List of (title, function) tuples to generate charts.
        output_path (str): Output path to save the generated PDF.

    Returns:
        str: Final PDF path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc = SimpleDocTemplate(output_path, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    elements = []

    # ======================= 📄 PAGE 1: Summary ==========================
    summary = compute_summary_insights(df)

    elements.append(Paragraph("📊 Article Analysis Summary", styles["Title"]))
    elements.append(Spacer(1, 12))

    insights = [
        f"Total Articles Analyzed: {summary['total_articles']}",
        f"Average Polarity Score: {summary['avg_polarity']}",
        f"Positive Articles: {summary['positive_articles']}",
        f"Negative Articles: {summary['negative_articles']}",
        f"Neutral Articles: {summary['neutral_articles']}"
    ]

    elements.append(Paragraph("🔹 Highlights", styles["Heading3"]))
    for item in insights:
        elements.append(Paragraph(item, styles["Normal"]))
    elements.append(Spacer(1, 12))

    if summary["top_keywords"]:
        elements.append(Paragraph("🔑 Top 10 Common Keywords", styles["Heading3"]))
        for kw, freq in summary["top_keywords"]:
            elements.append(Paragraph(f"• {kw} ({freq} times)", styles["Normal"]))

    elements.append(PageBreak())

    # ======================= 📄 PAGE 2: Metrics Table (Vertical) ==========================
    df_metric = df.drop(columns=["URL"]).set_index("URL_ID").T.reset_index()
    df_metric.columns = ["Metric"] + df_metric.columns[1:].tolist()

    table_data = [df_metric.columns.tolist()] + df_metric.values.tolist()
    table = Table(table_data, repeatRows=1, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))

    elements.append(Paragraph("📋 Article Metrics Table", styles["Heading2"]))
    elements.append(Spacer(1, 6))
    elements.append(table)
    elements.append(PageBreak())

    # ======================= 📄 PAGE 3+: Charts ==========================
    for title, fig_func in visual_funcs:
        try:
            print(f"🎯 Generating visual: {title}")
            fig = fig_func(df)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
                # Save plot to image
                if hasattr(fig, "savefig"):
                    fig.savefig(tmp_img.name, format='png', bbox_inches='tight')
                    plt.close(fig)
                elif hasattr(fig, "write_image"):
                    fig.write_image(tmp_img.name)
                else:
                    raise ValueError("Unsupported figure type")

                block = [
                    Paragraph(title, styles["Heading2"]),
                    Spacer(1, 6),
                    Image(tmp_img.name, width=500, height=300),
                    Spacer(1, 18)
                ]
                elements.append(KeepTogether(block))
                print(f"✅ Chart added: {title}")

        except Exception as e:
            print(f"⚠️ Failed to generate '{title}': {e}")
            elements.append(Paragraph(f"⚠️ Could not generate '{title}': {e}", styles["Normal"]))
            elements.append(Spacer(1, 12))

    # 🧾 Build final document
    doc.build(elements)
    print(f"✅ PDF saved to: {output_path}")
    return output_path