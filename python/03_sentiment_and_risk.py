import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv("data/processed/support_tickets_clean.csv")

# Validate the fields used by the risk rules.
allowed_statuses = ["Open", "Pending Customer Response", "Closed"]
allowed_priorities = ["Critical", "High", "Medium", "Low"]

if not df["ticket_status"].isin(allowed_statuses).all():
    raise ValueError("Unknown or missing ticket status found.")

if not df["ticket_priority"].isin(allowed_priorities).all():
    raise ValueError("Unknown or missing ticket priority found.")

# Handle absent text columns and missing text values.
for column in ["ticket_subject", "ticket_description"]:
    if column not in df.columns:
        df[column] = ""
    df[column] = df[column].fillna("").astype(str)

df["ticket_text"] = (
    df["ticket_subject"] + " " + df["ticket_description"]
).str.strip()

# Calculate VADER sentiment scores.
analyzer = SentimentIntensityAnalyzer()


def get_sentiment_score(text):
    return analyzer.polarity_scores(text)["compound"]


def classify_sentiment(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


df["sentiment_score"] = df["ticket_text"].apply(get_sentiment_score)
df["sentiment_label"] = df["sentiment_score"].apply(classify_sentiment)


# Apply the risk rules.
def classify_risk(row):
    unresolved = row["ticket_status"] in [
        "Open",
        "Pending Customer Response",
    ]
    urgent = row["ticket_priority"] in ["High", "Critical"]
    negative = row["sentiment_label"] == "Negative"

    if unresolved and urgent and negative:
        return "High Risk"
    elif unresolved and (urgent or negative):
        return "Medium Risk"
    else:
        return "Low Risk"


df["risk_level"] = df.apply(classify_risk, axis=1)

df["needs_alert"] = df["risk_level"].apply(
    lambda risk: "Yes" if risk == "High Risk" else "No"
)

# Save the dataset used by MySQL and Power BI.
df.to_csv(
    "data/processed/support_tickets_ai_ready.csv",
    index=False,
)

print("Sentiment and risk analysis completed.")
print("Total tickets:", len(df))

print("\nSentiment:")
print(df["sentiment_label"].value_counts())

print("\nRisk levels:")
print(df["risk_level"].value_counts())

print("\nneeds_alert is a review flag. No notifications were sent.")