from getpass import getpass

import pandas as pd
from sqlalchemy import URL, create_engine, inspect, text
from sqlalchemy.dialects.mysql import insert

# Load the AI-ready dataset.
df = pd.read_csv("data/processed/support_tickets_ai_ready.csv")

if df.empty:
    raise ValueError("The AI-ready CSV is empty.")

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

# Convert dates for MySQL.
df["date_of_purchase"] = pd.to_datetime(
    df["date_of_purchase"],
    errors="raise",
).dt.date

for column in ["first_response_time", "time_to_resolution"]:
    df[column] = pd.to_datetime(df[column], errors="raise")

# Convert the invalid-duration flag to 1 or 0.
df["invalid_resolution_time"] = (
    df["invalid_resolution_time"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({"true": 1, "false": 0, "1": 1, "0": 0})
)

if df["invalid_resolution_time"].isna().any():
    raise ValueError("Invalid duration flags must be True/False or 1/0.")

df["invalid_resolution_time"] = df["invalid_resolution_time"].astype(int)

# Ask for the password instead of storing it in this file.
password = getpass("Enter your MySQL password: ")

connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",  # Change this if you use another MySQL account.
    password=password,
    host="localhost",
    port=3306,
    database="customer_support_analytics",
    query={"charset": "utf8mb4"},
)

engine = create_engine(
    connection_url,
    pool_pre_ping=True,
    hide_parameters=True,
)


# pandas calls this function for each batch.
def upsert_tickets(table, connection, keys, data_iter):
    records = [dict(zip(keys, row)) for row in data_iter]

    statement = insert(table.table).values(records)

    updates = {
        column: statement.inserted[column]
        for column in keys
        if column != "ticket_id"
    }

    connection.execute(
        statement.on_duplicate_key_update(**updates)
    )


try:
    inspector = inspect(engine)

    if not inspector.has_table("support_tickets"):
        raise ValueError("Run sql/01_create_database.sql first.")

    primary_key = inspector.get_pk_constraint("support_tickets")

    if primary_key.get("constrained_columns") != ["ticket_id"]:
        raise ValueError(
            "ticket_id must be the primary key. "
            "Check the existing table in MySQL Workbench."
        )

    database_columns = {
        column["name"]
        for column in inspector.get_columns("support_tickets")
    }

    if database_columns != set(df.columns):
        raise ValueError(
            "CSV and database columns do not match. "
            "Check SHOW CREATE TABLE support_tickets."
        )

    options = inspector.get_table_options("support_tickets")

    if options.get("mysql_engine", "").lower() != "innodb":
        raise ValueError("The table must use InnoDB for this import.")

    # All batches are committed together or rolled back on failure.
    with engine.begin() as connection:
        before = connection.execute(
            text("SELECT COUNT(*) FROM support_tickets")
        ).scalar_one()

        # append keeps the existing table.
        # The custom method updates matching IDs instead of duplicating them.
        # pandas converts missing values into SQL NULL.
        df.to_sql(
            name="support_tickets",
            con=connection,
            if_exists="append",
            index=False,
            chunksize=500,
            method=upsert_tickets,
        )

        after = connection.execute(
            text("SELECT COUNT(*) FROM support_tickets")
        ).scalar_one()

    print("Import completed successfully.")
    print("CSV tickets processed:", len(df))
    print("Database rows before:", before)
    print("Database rows after:", after)
    print("Rows absent from the CSV were retained.")

finally:
    engine.dispose()