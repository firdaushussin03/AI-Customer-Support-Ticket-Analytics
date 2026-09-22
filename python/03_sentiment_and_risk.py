import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv("data/processed/support_tickets_clean.csv")

analyzer = SentimentIntensityAnalyzer()

# Combine subject and description for better sentiment analysis
df["ticket_text"] = (
    df.get("ticket_subject", "").astype(str) + " " +
    df.get("ticket_description", "").astype(str)
)

def get_sentiment_score(text):
    score = analyzer.polarity_scores(text)
    return score["compound"]

def classify_sentiment(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

df["sentiment_score"] = df["ticket_text"].apply(get_sentiment_score)
df["sentiment_label"] = df["sentiment_score"].apply(classify_sentiment)

# Create risk flag
def classify_risk(row):
    priority = str(row.get("ticket_priority", "")).lower()
    status = str(row.get("ticket_status", "")).lower()
    sentiment = str(row.get("sentiment_label", "")).lower()

    if priority in ["critical", "high"] and status != "closed" and sentiment == "negative":
        return "High Risk"
    elif priority in ["critical", "high"] and status != "closed":
        return "Medium Risk"
    elif sentiment == "negative" and status != "closed":
        return "Medium Risk"
    else:
        return "Low Risk"

df["risk_level"] = df.apply(classify_risk, axis=1)

# Create automation flag
df["needs_alert"] = df["risk_level"].apply(lambda x: "Yes" if x == "High Risk" else "No")

df.to_csv("data/processed/support_tickets_ai_ready.csv", index=False)

print("AI sentiment and risk classification completed.")
print(df[["ticket_text", "sentiment_label", "risk_level", "needs_alert"]].head())