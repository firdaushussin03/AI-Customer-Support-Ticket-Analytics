# AI Customer Support Ticket Analytics

A portfolio project using **Python, MySQL, SQL, VADER sentiment analysis, and Power BI** to examine support workload, customer satisfaction, response-to-resolution time, and tickets requiring review.

The current dataset contains **8,469 unique tickets**. A transparent rule flags **791 tickets** that are unresolved, have High or Critical priority, and contain negative sentiment. These flags support human review; they are not predictions of escalation or evidence that notifications were sent.

## Project objectives

- Understand how ticket volume varies by issue type, channel, priority, and status.
- Compare customer satisfaction across products and issue types.
- Examine the relationship between response-to-resolution time and satisfaction.
- Identify unresolved tickets that meet the defined high-risk rule.
- Present findings through a three-page Power BI report.

## Tools

| Tool | Purpose |
|---|---|
| Python, pandas, NumPy | Data inspection, cleaning, and derived fields |
| VADER | Lexicon-based sentiment scoring of ticket subject and description |
| MySQL, SQLAlchemy, PyMySQL | Optional database import and SQL analysis |
| Power BI | Interactive reporting and visual analysis |

VADER is a rule-based NLP baseline. This project does not train a machine-learning model or use a large language model.

## Repository structure

```text
AI-Customer-Support-Ticket-Analytics/
├── dashboard/
│   ├── Customer Support Ticket Analytics & AI Risk Monitoring Dashboard.pbix
│   ├── Executive Overview.png
│   ├── Support Performance Analysis.png
│   └── AI Risk Monitoring Dashboard.png
├── data/
│   ├── raw/
│   │   └── customer_support_tickets.csv
│   └── processed/
│       ├── support_tickets_clean.csv
│       └── support_tickets_ai_ready.csv
├── images/
│   ├── Automation Workflow Design.jpg
│   └── Project Workflow.jpg
├── python/
│   ├── 01_data_understanding.py
│   ├── 02_clean_data.py
│   ├── 03_sentiment_and_risk.py
│   └── 04_import_to_mysql.py
├── sql/
│   ├── 01_create_database.sql
│   └── 02_analysis.sql
├── .gitignore
├── requirement.txt
└── README.md
```

## Data preparation

The current cleaning script:

1. Standardizes column names and removes identical duplicate rows.
2. Strips whitespace and standardizes selected categorical fields.
3. Parses purchase dates, first-response timestamps, and resolution timestamps.
4. Fills missing ages with the median and adds age groups.
5. Preserves missing satisfaction ratings and excludes ratings outside 1–5.
6. Calculates `resolution_hours` as resolution timestamp minus first-response timestamp.
7. Flags negative durations using `invalid_resolution_time`, then sets those durations to missing without deleting the tickets.
8. Exports the cleaned CSV before sentiment scoring and risk classification.

The final AI-ready file contains **25 columns**. It adds combined ticket text, sentiment scores and labels, risk levels, and an alert eligibility flag.

## Sentiment and risk rules

VADER assigns a compound sentiment score to the combined ticket subject and description.

| Compound score | Sentiment |
|---|---|
| At least 0.05 | Positive |
| At most -0.05 | Negative |
| Between -0.05 and 0.05 | Neutral |

For the recognized statuses in this dataset, unresolved means **Open** or **Pending Customer Response**.

| Condition | Risk level |
|---|---|
| Unresolved, High/Critical priority, and Negative sentiment | High Risk |
| Unresolved and either High/Critical priority or Negative sentiment, excluding High Risk above | Medium Risk |
| Remaining cases | Low Risk |

`needs_alert` is `Yes` for High Risk and `No` otherwise. It identifies review candidates; no notification delivery is implemented.

**Implementation limitation:** the current script checks `status != "closed"` rather than validating allowed statuses. Unknown or missing statuses could therefore be treated as unresolved. Input validation is a recommended improvement.

## Power BI report

### Executive Overview

Shows total tickets, unresolved tickets, high-risk tickets, average satisfaction, and ticket distributions by issue type, status, channel, and priority.

### Support Performance Analysis

Shows average response-to-resolution hours, valid duration count, average satisfaction, and rated ticket count. Visuals compare duration by priority, satisfaction by issue type, the five highest-rated products, and product-average duration versus satisfaction.

Each scatterplot point represents one product. Its duration and satisfaction averages can use different sets of available records.

### AI Risk Monitoring Dashboard

Shows high-risk count, high-risk share of unresolved tickets, Critical high-risk tickets, Open high-risk tickets, priority breakdowns, sentiment distribution, and a review queue filtered to `needs_alert = Yes`.

Status, priority, channel, and product slicers support exploration. Cross-page slicer synchronization and button behavior should be checked in Power BI Desktop.

## Key metrics

These values describe the complete processed dataset before dashboard filtering.

| Metric | Result | Definition |
|---|---:|---|
| Total tickets | 8,469 | Unique ticket IDs |
| Unresolved tickets | 5,700 | Open or Pending Customer Response |
| Unresolved share | 67.3% | Unresolved / all tickets |
| High-risk tickets | 791 | Tickets meeting the high-risk rule |
| High-risk share | 13.9% | High risk / unresolved tickets |
| Critical high-risk tickets | 399 | High-risk tickets with Critical priority |
| Open high-risk tickets | 401 | High-risk tickets with Open status |
| Average satisfaction | 2.99 / 5 | Mean of available valid ratings |
| Rated tickets | 2,769 | Tickets with a valid satisfaction rating |
| Average response-to-resolution time | 7.58 hours | Mean of available nonnegative durations |
| Valid duration tickets | 1,404 | Tickets contributing to the duration average |
| Invalid duration tickets | 1,365 | Resolution timestamp precedes first response |

## Insights and suggested actions

### 1. Most tickets are unresolved in this dataset

There are **5,700 unresolved tickets**, representing **67.3%** of all tickets. This includes **2,819 Open** and **2,881 Pending Customer Response** tickets.

**Suggestion:** separate active support work from cases awaiting a customer reply. Ticket age and historical snapshots would be needed to assess whether the backlog is growing or overdue.

### 2. The risk rule creates a focused review queue

The **791 high-risk tickets** include **399 Critical** and **392 High** priority cases. By status, **401 are Open** and **390 await a customer response**.

**Suggestion:** review Critical cases first and check the underlying text before taking action. The flag is a prioritization rule, not a calibrated probability of escalation.

### 3. Workload is fairly evenly distributed

Refund Request has the most tickets (**1,752**), narrowly ahead of Technical Issue (**1,747**). Channel volumes are also similar: Email **2,143**, Phone **2,132**, Social Media **2,121**, and Chat **2,073**.

**Suggestion:** avoid recommending a major staffing shift from volume alone. Compare handling effort, staffing capacity, and customer outcomes before reallocating resources.

### 4. Satisfaction is close to the middle of the rating scale

Average satisfaction is **2.99/5** across **2,769 rated tickets**, approximately **32.7%** of all tickets. The top five product averages are close together, around **3.20–3.22**.

**Suggestion:** show rating counts alongside averages and use a **0–5 axis** for satisfaction bars. Small differences between products should not be presented as meaningful performance gaps without further analysis.

### 5. Duration quality limits performance conclusions

Of **2,769 closed tickets**, **1,365 (49.3%)** have resolution timestamps earlier than first response. The **7.58-hour** average describes only the **1,404 valid records**.

**Suggestion:** investigate timestamp inconsistencies before using duration averages for operational targets. Keep the valid-record count and exclusion note visible beside duration charts.

### 6. The scatterplot does not establish causation

The product-level scatterplot compares average valid duration with average satisfaction. These averages may come from different tickets, and aggregation can hide variation within a product.

**Suggestion:** use it to explore patterns, not to claim that faster resolution causes higher satisfaction. A follow-up analysis should use tickets with both valid duration and rating data.

## Run the project locally

### 1. Install dependencies

Use Python 3.10 or later. Run these commands from the repository root in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirement.txt
```

MySQL Server and Power BI Desktop are separate applications and are not installed by this command.

### 2. Prepare and process the data

Ensure `data/raw/customer_support_tickets.csv` is present. Create the output directory if needed:

```powershell
New-Item -ItemType Directory -Force data/processed
```

The optional inspection script currently contains an absolute Windows path. Update its `pd.read_csv(...)` path to your local raw CSV before running it:

```powershell
.\.venv\Scripts\python.exe python/01_data_understanding.py
```

Run the main pipeline from the repository root:

```powershell
.\.venv\Scripts\python.exe python/02_clean_data.py
.\.venv\Scripts\python.exe python/03_sentiment_and_risk.py
```

The scripts write `support_tickets_clean.csv` and `support_tickets_ai_ready.csv` under `data/processed/`.

### 3. Optional MySQL analysis

1. Start MySQL and run `sql/01_create_database.sql` if the database does not already exist.
2. Configure the connection in `python/04_import_to_mysql.py` for your local server. The current script embeds connection credentials; move them to environment variables or a password prompt before publishing changes.
3. Run the importer:

```powershell
.\.venv\Scripts\python.exe python/04_import_to_mysql.py
```

4. Select the database and run the analysis queries:

```sql
USE customer_support_analytics;
```

Run `sql/02_analysis.sql` in your SQL client after selecting the database.

**Current importer behavior:** `if_exists="replace"` replaces the `support_tickets` table. It is intended here for a disposable analysis database, not incremental loading into a maintained operational table. The setup SQL currently creates only the database; pandas creates the imported table.

### 4. Open Power BI

1. Open the PBIX in `dashboard/`.
2. In Power Query, update the CSV source path to your local `data/processed/support_tickets_ai_ready.csv`.
3. Preserve the existing query/table name to retain visual and measure references.
4. If the CSV Source step fixes the column count at 24, update it to 25 or remove the fixed count so `needs_alert` is included.
5. Apply changes and refresh. Compare the unfiltered cards with the metric table above.

## Limitations and next improvements

- **Validation:** add checks for conflicting duplicate IDs, required columns, and allowed status/priority values. These checks are not currently implemented.
- **Age groups:** fix the current bin boundaries: age 18 is included in the group labelled `Below 18`, and the `60+` label does not accurately describe its greater-than-60 interval.
- **Text handling:** handle absent subject/description columns and missing text explicitly before sentiment scoring.
- **Sentiment quality:** validate VADER labels against a manually reviewed sample. Sentiment is not the same measure as a customer satisfaction rating.
- **Database loading:** replace embedded credentials and table replacement with secure configuration, an explicit schema, and primary-key upserts if incremental loading is required.
- **Dashboard polish:** clarify the high-risk denominator, set satisfaction bars to 0–5, show duration exclusions, and prioritize the review queue by severity.
- **Time analysis:** obtain ticket-created timestamps before calculating total resolution time, backlog age, or ticket-arrival trends. Purchase date is not a ticket-created date.
- **Automation:** notification delivery, deduplication, and delivery logging remain future work. Workflow design images do not establish that these features are implemented.
- **Testing:** add automated checks for cleaning boundaries and risk rules. This repository currently has no automated test suite.

Results are descriptive findings from the supplied dataset. They do not demonstrate a measured business improvement, predictive accuracy, or a live monitoring deployment.
