import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def ensure_charts_dir():
    os.makedirs("charts", exist_ok=True)


def plot_sentiment_distribution_matplotlib(df, path="charts/sentiment_distribution.png"):
    df = df.copy()
    df["SentimentGroup"] = df["POLARITY SCORE"].apply(
        lambda x: "Positive" if x > 0.1 else "Negative" if x < -0.1 else "Neutral"
    )

    plt.figure(figsize=(8, 5))
    for sentiment in df["SentimentGroup"].unique():
        subset = df[df["SentimentGroup"] == sentiment]
        plt.hist(subset["POLARITY SCORE"], bins=10, alpha=0.6, label=sentiment)

    plt.title("Sentiment Polarity Distribution")
    plt.xlabel("Polarity Score")
    plt.ylabel("Count")
    plt.legend(title="SentimentGroup", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    os.makedirs("charts", exist_ok=True)
    plt.savefig(path)
    plt.close()


def plot_wordcount_vs_complexity_matplotlib(df, path="charts/word_count_vs_complexity.png"):
    plt.figure(figsize=(8, 5))
    plt.scatter(df["WORD COUNT"], df["PERCENTAGE OF COMPLEX WORDS"], color='royalblue')

    for i, row in df.iterrows():
        plt.text(row["WORD COUNT"], row["PERCENTAGE OF COMPLEX WORDS"], str(row["URL_ID"]),
                 fontsize=7, ha='left', va='bottom')

    plt.title("Word Count vs Complex Word Usage")
    plt.xlabel("Word Count")
    plt.ylabel("% of Complex Words")
    plt.tight_layout()
    os.makedirs("charts", exist_ok=True)
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
    plt.title("Personal Pronoun Usage per Article")
    plt.xlabel("Article ID")
    plt.ylabel("Count of Personal Pronouns")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()