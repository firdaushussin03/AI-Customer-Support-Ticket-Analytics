import pandas as pd
import numpy as np

df = pd.read_csv("data/raw/customer_support_tickets.csv")

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Remove duplicate rows
df = df.drop_duplicates()

# Strip spaces from all text-like columns
text_like_columns = df.select_dtypes(include=["object", "string"]).columns

for col in text_like_columns:
    df[col] = df[col].astype("string").str.strip()

# Convert date columns
if "date_of_purchase" in df.columns:
    df["date_of_purchase"] = pd.to_datetime(df["date_of_purchase"], errors="coerce")

if "first_response_time" in df.columns:
    df["first_response_time"] = pd.to_datetime(df["first_response_time"], errors="coerce")

if "time_to_resolution" in df.columns:
    df["time_to_resolution"] = pd.to_datetime(df["time_to_resolution"], errors="coerce")

# Standardize text columns
text_columns = [
    "customer_gender",
    "product_purchased",
    "ticket_type",
    "ticket_status",
    "ticket_priority",
    "ticket_channel"
]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].astype("string").str.strip().str.title()

# Handle missing values
if "customer_age" in df.columns:
    df["customer_age"] = df["customer_age"].fillna(df["customer_age"].median())

if "customer_satisfaction_rating" in df.columns:
    df["customer_satisfaction_rating"] = df["customer_satisfaction_rating"].fillna(0)

if "resolution" in df.columns:
    df["resolution"] = df["resolution"].fillna("No resolution provided")

if "ticket_description" in df.columns:
    df["ticket_description"] = df["ticket_description"].fillna("No description provided")

# Create resolution time in hours
if "first_response_time" in df.columns and "time_to_resolution" in df.columns:
    df["resolution_hours"] = (
        df["time_to_resolution"] - df["first_response_time"]
    ).dt.total_seconds() / 3600

    # Remove impossible negative resolution time
    df = df[(df["resolution_hours"].isna()) | (df["resolution_hours"] >= 0)]

# Create age group
if "customer_age" in df.columns:
    df["age_group"] = pd.cut(
        df["customer_age"],
        bins=[0, 18, 25, 35, 45, 60, 100],
        labels=["Below 18", "18-25", "26-35", "36-45", "46-60", "60+"]
    )

# Save cleaned data
df.to_csv("data/processed/support_tickets_clean.csv", index=False)

print("Cleaning completed.")
print("Cleaned shape:", df.shape)