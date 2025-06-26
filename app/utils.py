import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import time


def clean_old_pdfs(folder="output", max_age_minutes=30):

    """Deletes PDF files older than a specified number of minutes in the given folder."""
    
    now = time.time()
    cutoff = now - (max_age_minutes * 60)

    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))
    deleted_count = 0

    for file_path in pdf_files:
        if os.path.isfile(file_path):
            file_mtime = os.path.getmtime(file_path)
            if file_mtime < cutoff:
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
    
    print(f"🧹 Cleaned {deleted_count} old PDF(s) from '{folder}'")



def clear_old_charts(chart_dir="charts"):
    """
    Deletes all PNG files in the given chart directory.
    """
    if os.path.exists(chart_dir):
        for file in glob.glob(os.path.join(chart_dir, "*.png")):
            try:
                os.remove(file)
            except Exception as e:
                print(f"⚠️ Could not delete {file}: {e}")


def count_syllables(word):
    """
    Approximate syllable count for a given word.
    Used to estimate complexity in readability metrics.
    """
    vowels = "aeiouy"
    word = word.lower()
    count = 0
    prev_vowel = False

    for c in word:
        if c in vowels:
            if not prev_vowel:
                count += 1
            prev_vowel = True
        else:
            prev_vowel = False

    # Adjust for common suffixes
    if word.endswith(("es", "ed")):
        count = max(1, count - 1)

    return max(1, count)


def load_input_excel(path):
    """
    Loads an Excel file and ensures correct column names.
    Falls back to default headers if missing.
    """
    df = pd.read_excel(path)

    # Handle files without headers
    if "URL_ID" not in df.columns or "URL" not in df.columns:
        df = pd.read_excel(path, header=None, names=["URL_ID", "URL"])

    return df


def save_plot_image(fig, filename):
    """
    Saves matplotlib or plotly figure to a PNG file.
    """
    try:
        if hasattr(fig, "savefig"):
            fig.savefig(filename, format="png", bbox_inches="tight")
            plt.close(fig)
        elif hasattr(fig, "write_image"):
            fig.write_image(filename)
        else:
            raise TypeError("Unsupported figure type. Must be matplotlib or plotly.")
    except Exception as e:
        print(f"[❌ Error saving plot]: {e}")