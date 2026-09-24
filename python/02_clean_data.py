from pathlib import Path

import pandas as pd

# Load the raw dataset.
df = pd.read_csv("data/raw/customer_support_tickets.csv")

# Standardize column names.
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)

# Remove whitespace from text columns.
for column in df.select_dtypes(include=["object", "string"]).columns:
    df[column] = df[column].astype("string").str.strip()

# Remove identical duplicate rows.
df = df.drop_duplicates().copy()

# Check ticket IDs.
df["ticket_id"] = pd.to_numeric(df["ticket_id"], errors="raise")

if (
    df["ticket_id"].isna().any()
    or df["ticket_id"].duplicated().any()
    or (df["ticket_id"] <= 0).any()
    or (df["ticket_id"] % 1 != 0).any()
):
    raise ValueError("Ticket IDs must be unique, positive whole numbers.")

df["ticket_id"] = df["ticket_id"].astype("int64")

# Standardize categorical values.
category_columns = [
    "customer_gender",
    "product_purchased",
    "ticket_type",
    "ticket_status",
    "ticket_priority",
    "ticket_channel",
]

for column in category_columns:
    df[column] = df[column].astype("string").str.title()

# Validate status and priority before risk classification.
allowed_statuses = ["Open", "Pending Customer Response", "Closed"]
allowed_priorities = ["Critical", "High", "Medium", "Low"]

if not df["ticket_status"].isin(allowed_statuses).all():
    raise ValueError("Unknown or missing ticket status found.")

if not df["ticket_priority"].isin(allowed_priorities).all():
    raise ValueError("Unknown or missing ticket priority found.")

# Convert date columns.
for column in [
    "date_of_purchase",
    "first_response_time",
    "time_to_resolution",
]:
    df[column] = pd.to_datetime(df[column], errors="coerce")

# Clean customer age.
age = pd.to_numeric(df["customer_age"], errors="coerce")
age = age.where(age.between(0, 100))
df["customer_age"] = age.fillna(age.median())

# Keep only valid satisfaction ratings. Missing ratings remain missing.
ratings = pd.to_numeric(
    df["customer_satisfaction_rating"],
    errors="coerce",
)
df["customer_satisfaction_rating"] = ratings.where(ratings.between(1, 5))

# Prepare text fields.
df["resolution"] = df["resolution"].fillna("No resolution provided")

for column in ["ticket_subject", "ticket_description"]:
    if column not in df.columns:
        df[column] = ""
    df[column] = df[column].fillna("")

# Calculate hours from first response to resolution.
df["resolution_hours"] = (
    df["time_to_resolution"] - df["first_response_time"]
).dt.total_seconds() / 3600

# Keep the ticket, flag the invalid duration, and blank only the duration.
df["invalid_resolution_time"] = df["resolution_hours"] < 0

df.loc[
    df["invalid_resolution_time"],
    "resolution_hours",
] = float("nan")

# Correct age boundaries: age 18 belongs to 18–25.
df["age_group"] = pd.cut(
    df["customer_age"],
    bins=[0, 18, 26, 36, 46, 61, 101],
    labels=["Under 18", "18-25", "26-35", "36-45", "46-60", "61+"],
    right=False,
)

# Save the cleaned dataset.
Path("data/processed").mkdir(parents=True, exist_ok=True)

df.to_csv(
    "data/processed/support_tickets_clean.csv",
    index=False,
)

print("Cleaning completed.")
print("Total tickets:", len(df))
print("Valid duration tickets:", df["resolution_hours"].count())
print("Invalid durations:", df["invalid_resolution_time"].sum())
print("Rated tickets:", df["customer_satisfaction_rating"].count())