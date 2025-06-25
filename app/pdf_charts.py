import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def ensure_charts_dir():
    os.makedirs("charts", exist_ok=True)


def save_sentiment_distribution_matplotlib(df, path="charts/sentiment_distribution.png"):
    ensure_charts_dir()
    df = df.copy()
    df["SentimentGroup"] = df["POLARITY SCORE"].apply(
        lambda x: "Positive" if x > 0.1 else "Negative" if x < -0.1 else "Neutral"
    )

    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="POLARITY SCORE", hue="SentimentGroup", bins=30, palette="Set2", kde=False)
    plt.title("📊 Sentiment Polarity Distribution")
    plt.xlabel("Polarity Score")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def save_word_count_vs_complexity_matplotlib(df, path="charts/word_count_vs_complexity.png"):
    ensure_charts_dir()
    plt.figure(figsize=(8, 5))
    sns.scatterplot(
        data=df,
        x="WORD COUNT",
        y="PERCENTAGE OF COMPLEX WORDS",
        hue="URL_ID",
        palette="husl",
        legend=False,
        s=50
    )
    plt.title("🧠 Word Count vs Complex Word Usage")
    plt.xlabel("Word Count")
    plt.ylabel("% of Complex Words")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def save_personal_pronouns_barchart_matplotlib(df, path="charts/personal_pronouns_barchart.png"):
    ensure_charts_dir()
    df_clean = df[["URL_ID", "PERSONAL PRONOUNS"]].dropna()
    df_clean["PERSONAL PRONOUNS"] = pd.to_numeric(df_clean["PERSONAL PRONOUNS"], errors="coerce").fillna(0)

    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=df_clean,
        x="URL_ID",
        y="PERSONAL PRONOUNS",
        palette="Blues_d"
    )
    plt.title("🗣️ Personal Pronoun Usage per Article")
    plt.xlabel("Article ID")
    plt.ylabel("Count of Personal Pronouns")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()