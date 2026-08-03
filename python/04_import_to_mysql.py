import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("data/processed/support_tickets_ai_ready.csv")

# Convert empty/missing values into proper NULL values for MySQL
df = df.where(pd.notnull(df), None)

# Your MySQL connection
# Change password if your MySQL has a password
engine = create_engine(
    "mysql+pymysql://root:@localhost:3306/customer_support_analytics"
)

# Import dataframe into MySQL table
df.to_sql(
    name="support_tickets",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data imported successfully into MySQL.")
print("Total rows imported:", len(df))