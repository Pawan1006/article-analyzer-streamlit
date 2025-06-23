import os
import requests
from newspaper import Article
from readability import Document
from bs4 import BeautifulSoup


def extract_articles(url_id, url, save_dir="extracted_articles"):
    """
    Extracts main text content from a given URL using Newspaper3k or Readability fallback.
    
    Args:
        url_id (str): Unique identifier for the article.
        url (str): The article URL.
        save_dir (str): Directory to save extracted articles.

    Returns:
        tuple: (True/False, status message)
    """
    def save_to_file(text):
        try:
            os.makedirs(save_dir, exist_ok=True)
            file_path = os.path.join(save_dir, f"{url_id}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text.strip())
            return True, "✅ Article saved successfully"
        except Exception as e:
            return False, f"❌ Failed to save file: {e}"

    # --------- Method 1: Try Newspaper3k ---------
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text.strip()

        if len(text) >= 300:
            saved, msg = save_to_file(text)
            return saved, f"✅ Extracted with Newspaper3k | {msg}"
    except Exception:
        pass  # Fall back to next method

    # --------- Method 2: Try Readability + BeautifulSoup fallback ---------
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        doc = Document(response.text)
        soup = BeautifulSoup(doc.summary(), "html.parser")
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        text = "\n".join(paragraphs)

        if len(text) >= 100:
            saved, msg = save_to_file(text)
            return saved, f"✅ Extracted with Readability | {msg}"
        else:
            return False, "⚠️ Readability fallback content too short"
    except Exception as e:
        return False, f"❌ Failed to extract content: {e}"