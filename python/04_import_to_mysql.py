import os
from getpass import getpass
from pathlib import Path

import pandas as pd
from sqlalchemy import MetaData, Table, URL, create_engine, inspect
from sqlalchemy.dialects.mysql import insert


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "support_tickets_ai_ready.csv"
)

TABLE_NAME = "support_tickets"

EXPECTED_COLUMNS = {
    "ticket_id",
    "customer_name",
    "customer_email",
    "customer_age",
    "customer_gender",
    "product_purchased",
    "date_of_purchase",
    "ticket_type",
    "ticket_subject",
    "ticket_description",
    "ticket_status",
    "resolution",
    "ticket_priority",
    "ticket_channel",
    "first_response_time",
    "time_to_resolution",
    "customer_satisfaction_rating",
    "resolution_hours",
    "invalid_resolution_time",
    "age_group",
    "ticket_text",
    "sentiment_score",
    "sentiment_label",
    "risk_level",
    "needs_alert",
}


def load_records():
    df = pd.read_csv(CSV_PATH)

    if set(df.columns) != EXPECTED_COLUMNS:
        missing = sorted(EXPECTED_COLUMNS - set(df.columns))
        extra = sorted(set(df.columns) - EXPECTED_COLUMNS)
        raise ValueError(
            f"CSV columns do not match. Missing: {missing}; extra: {extra}"
        )

    if df.empty:
        raise ValueError("The CSV is empty. Nothing was imported.")

    # Validate IDs before using them as database keys.
    ids = pd.to_numeric(df["ticket_id"], errors="raise")

    if (
        ids.isna().any()
        or ((ids % 1) != 0).any()
        or not ids.between(1, 2147483647).all()
    ):
        raise ValueError("Ticket IDs must be positive MySQL INT values.")

    df["ticket_id"] = ids.astype("int64")

    if df["ticket_id"].duplicated().any():
        raise ValueError(
            "Duplicate ticket IDs found in the CSV. Fix them before importing."
        )

    # Parse dates; invalid non-empty values raise an error.
    date_columns = [
        "date_of_purchase",
        "first_response_time",
        "time_to_resolution",
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(df[column], errors="raise")

    # Convert the CSV flag into Python booleans.
    flags = (
        df["invalid_resolution_time"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "true": True,
            "false": False,
            "1": True,
            "0": False,
        })
    )

    if flags.isna().any():
        raise ValueError(
            "invalid_resolution_time must contain True/False or 1/0."
        )

    df["invalid_resolution_time"] = flags

    # Object dtype allows missing numeric/date values to become None.
    # The database driver converts None into SQL NULL.
    records = (
        df.astype(object)
        .where(pd.notna(df), None)
        .to_dict(orient="records")
    )

    for record in records:
        if record["date_of_purchase"] is not None:
            record["date_of_purchase"] = (
                record["date_of_purchase"].date()
            )

        for column in ["first_response_time", "time_to_resolution"]:
            if record[column] is not None:
                record[column] = record[column].to_pydatetime()

    return records


def main():
    records = load_records()

    password = os.environ.get("MYSQL_PASSWORD")

    if password is None:
        password = getpass("Enter your MySQL password: ")

    # URL.create safely handles special characters in passwords.
    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=os.environ.get("MYSQL_USER", "root"),
        password=password,
        host=os.environ.get("MYSQL_HOST", "localhost"),
        port=int(os.environ.get("MYSQL_PORT", "3306")),
        database=os.environ.get(
            "MYSQL_DATABASE",
            "customer_support_analytics",
        ),
        query={"charset": "utf8mb4"},
    )

    engine = create_engine(
        connection_url,
        pool_pre_ping=True,
        hide_parameters=True,
    )

    try:
        inspector = inspect(engine)

        if not inspector.has_table(TABLE_NAME):
            raise RuntimeError(
                "support_tickets does not exist. Run the setup SQL first."
            )

        primary_key = inspector.get_pk_constraint(TABLE_NAME)

        if primary_key.get("constrained_columns") != ["ticket_id"]:
            raise RuntimeError(
                "ticket_id must be the table's primary key. "
                "Complete Step 2 before importing."
            )

        table = Table(
            TABLE_NAME,
            MetaData(),
            autoload_with=engine,
        )

        if set(table.columns.keys()) != EXPECTED_COLUMNS:
            raise RuntimeError(
                "The database table columns do not match the CSV schema."
            )

        # This table should use InnoDB for transactional imports.
        options = inspector.get_table_options(TABLE_NAME)
        storage_engine = options.get("mysql_engine", "")

        if storage_engine.lower() != "innodb":
            raise RuntimeError(
                "The table must use InnoDB for transactional imports. "
                "Check SHOW CREATE TABLE support_tickets."
            )

        # Commit all batches together, or roll back if an error occurs.
        with engine.begin() as connection:
            for start in range(0, len(records), 500):
                batch = records[start:start + 500]

                statement = insert(table).values(batch)

                statement = statement.on_duplicate_key_update(
                    **{
                        column.name: statement.inserted[column.name]
                        for column in table.columns
                        if column.name != "ticket_id"
                    }
                )

                connection.execute(statement)

        print(f"Successfully processed {len(records):,} tickets.")
        print("New ticket IDs were inserted.")
        print("Existing ticket IDs were updated.")
        print("Rows absent from the CSV were retained.")

    finally:
        engine.dispose()


if __name__ == "__main__":
    main()