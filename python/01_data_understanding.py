import pandas as pd

df = pd.read_csv("data/raw/customer_support_tickets.csv")

print("Dataset shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nExact duplicate rows:", df.duplicated().sum())

print("\nUnique ticket IDs:", df["Ticket ID"].nunique())

print("\nTicket status:")
print(df["Ticket Status"].value_counts(dropna=False))