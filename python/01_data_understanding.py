import pandas as pd

df = pd.read_csv(r"C:\Users\mohd5\Documents\customer-support-ticket-analytics\data\raw\customer_support_tickets.csv")



print("Shape of dataset:")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nData types:")
print(df.dtypes)