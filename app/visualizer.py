import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def wrap_plotly(fig):
    """
    Tags Plotly figure so it can be detected in the PDF exporter.
    """
    fig.__class__.__name__ = "WrappedPlotlyFigure"
    return fig


def sentiment_distribution(df):
    """
    Displays histogram of polarity scores grouped by sentiment.
    """
    df = df.copy()
    df["SentimentGroup"] = df["POLARITY SCORE"].apply(
        lambda x: "Positive" if x > 0.1 else "Negative" if x < -0.1 else "Neutral"
    )

    fig = px.histogram(
        df,
        x="POLARITY SCORE",
        color="SentimentGroup",
        nbins=30,
        title="📊 Sentiment Polarity Distribution by Category",
        labels={"POLARITY SCORE": "Polarity Score", "SentimentGroup": "Sentiment"},
        template="plotly_white",
        color_discrete_map={
            "Positive": "#2ca02c",
            "Negative": "#d62728",
            "Neutral": "#1f77b4"
        }
    )
    fig.update_layout(
        bargap=0.1,
        xaxis_title="Polarity Score",
        yaxis_title="Count",
        font=dict(color="#000000")
    )
    return wrap_plotly(fig)


def word_count_vs_complexity(df):
    """
    Scatter plot showing word count vs % of complex words.
    """
    fig = px.scatter(
        df,
        x="WORD COUNT",
        y="PERCENTAGE OF COMPLEX WORDS",
        hover_data=["URL_ID"],
        title="🧠 Word Count vs Complex Word Usage",
        labels={
            "WORD COUNT": "Word Count",
            "PERCENTAGE OF COMPLEX WORDS": "% Complex Words"
        },
        template="plotly_white",
        color_discrete_sequence=["#636EFA"]
    )
    fig.update_layout(
        xaxis_title="Word Count",
        yaxis_title="% of Complex Words",
        font=dict(color="#000000")
    )
    return wrap_plotly(fig)


def personal_pronouns_barchart(df):
    """
    Bar chart showing usage of personal pronouns per article.
    """
    df_clean = df[["URL_ID", "PERSONAL PRONOUNS"]].dropna()
    df_clean["PERSONAL PRONOUNS"] = pd.to_numeric(df_clean["PERSONAL PRONOUNS"], errors="coerce").fillna(0)

    fig = px.bar(
        df_clean,
        x="URL_ID",
        y="PERSONAL PRONOUNS",
        text="PERSONAL PRONOUNS",
        title="🗣 Personal Pronoun Usage per Article",
        labels={
            "URL_ID": "Article ID",
            "PERSONAL PRONOUNS": "Count of Personal Pronouns"
        },
        color_discrete_sequence=["#3f8efc"]
    )
    fig.update_traces(
        textposition='outside',
        marker=dict(line=dict(width=1, color='black'))
    )
    fig.update_layout(
        template="plotly_white",
        xaxis_title="Article ID",
        yaxis_title="Count of Personal Pronouns",
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        bargap=0.3
    )
    return wrap_plotly(fig)


def generate_wordcloud(keywords):
    """
    Generates a WordCloud from a list of keywords.
    """
    if not keywords:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No keywords available", ha="center", va="center")
        ax.axis("off")
        return fig

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(keywords))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    return fig


def plot_sentiment_comparison(sentiment_data):
    """
    Bar chart comparing TextBlob and VADER sentiment scores.
    """
    df = pd.DataFrame(sentiment_data)
    df_melted = df.melt(id_vars='URL_ID', var_name='Method', value_name='Score')

    fig = px.bar(
        df_melted,
        x="URL_ID",
        y="Score",
        color="Method",
        barmode="group",
        title="🧪 Sentiment Comparison: TextBlob vs VADER",
        labels={"Score": "Polarity Score", "URL_ID": "Article ID"}
    )
    return wrap_plotly(fig)


def plot_readability_comparison(readability_data):
    """
    Bar chart comparing FOG index and Flesch reading ease.
    """
    df = pd.DataFrame(readability_data)
    df_melted = df.melt(id_vars='URL_ID', var_name='Metric', value_name='Score')

    fig = px.bar(
        df_melted,
        x="URL_ID",
        y="Score",
        color="Metric",
        barmode="group",
        title="📚 Readability Comparison: FOG vs Flesch",
        labels={"Score": "Readability Score", "URL_ID": "Article ID"}
    )
    return wrap_plotly(fig)