# AI-Assisted Customer Support Ticket Analytics & Risk Monitoring Dashboard

## Project Overview

Customer support teams receive thousands of support tickets from different channels every day. Identifying urgent customer issues quickly while monitoring overall support performance is essential for maintaining customer satisfaction.

This project analyzes customer support ticket data using **Python, SQL, MySQL, and Power BI** to identify customer support trends, evaluate operational performance, classify customer sentiment using AI-assisted analysis, and monitor high-risk unresolved tickets through an interactive dashboard.

---

## Business Problem

Customer support teams often struggle to prioritize urgent customer issues because tickets arrive from multiple channels with different priorities and varying customer sentiment.

Without an effective monitoring system:

- High-priority tickets may remain unresolved for too long.
- Negative customer experiences may go unnoticed.
- Managers have limited visibility into support performance and operational risks.

This project provides an analytical solution to help support teams monitor performance, identify high-risk tickets, and support faster decision-making.

---

## Project Objectives

- Analyze customer support ticket trends and operational performance.
- Measure key support KPIs such as ticket volume, customer satisfaction, and resolution time.
- Apply AI-assisted sentiment analysis to customer ticket descriptions.
- Identify high-risk unresolved tickets using rule-based risk classification.
- Build an interactive Power BI dashboard for business monitoring and decision-making.

---

## Dataset

**Source:** Kaggle – Customer Support Ticket Dataset

The dataset contains customer support records including:

- Ticket Status
- Ticket Priority
- Ticket Type
- Ticket Channel
- Product Purchased
- Customer Satisfaction Rating
- Ticket Description
- Resolution Details
- Response Time

---

## Tools & Technologies

- Python (Pandas)
- SQL
- MySQL Workbench
- Power BI
- VS Code
- VADER Sentiment Analysis

---

## Project Workflow

```
Raw Dataset
      │
      ▼
Data Cleaning (Python)
      │
      ▼
Feature Engineering
      │
      ▼
AI Sentiment Analysis
      │
      ▼
Risk Classification
      │
      ▼
SQL Analysis (MySQL)
      │
      ▼
Power BI Dashboard
      │
      ▼
Business Insights & Recommendations
```

---

## Data Cleaning

Data preprocessing was performed using **Python Pandas** to prepare an analysis-ready dataset.

The cleaning process included:

- Standardizing column names
- Removing duplicate records
- Handling missing values
- Standardizing text fields
- Converting date and time columns
- Creating Resolution Hours
- Creating Age Group categories
- Preparing data for SQL and Power BI analysis

---

## AI-Assisted Sentiment Analysis

Customer ticket descriptions were analyzed using **VADER Sentiment Analysis**.

Each ticket was classified into one of three categories:

- Positive
- Neutral
- Negative

A rule-based risk classification was then applied to identify support tickets requiring immediate attention.

### High Risk Logic

A ticket is classified as **High Risk** when:

- Ticket Priority = High or Critical
- Ticket Status ≠ Closed
- Customer Sentiment = Negative

Tickets meeting these conditions are automatically flagged for monitoring.

---

## SQL Analysis

SQL queries were written to analyze:

- Total ticket volume
- Ticket status distribution
- Ticket priority distribution
- Ticket channel performance
- Most common ticket types
- Product complaint trends
- Customer satisfaction
- Resolution time
- High-risk tickets

---

# Power BI Dashboard

The dashboard consists of **three pages**.

---

## Page 1 — Executive Overview

Provides a high-level summary of customer support operations.

### KPIs

- Total Tickets
- Open Tickets
- High Risk Tickets
- Average Customer Satisfaction

### Visualizations

- Monthly Ticket Trend (Line Chart)
- Ticket Status Distribution (Donut Chart)
- Tickets by Priority (Bar Chart)
- Top Products with Most Support Tickets (Bar Chart)

### Filters

- Ticket Status
- Ticket Priority
- Product Purchased
- Ticket Channel

---

## Page 2 — Support Performance Analysis

Analyzes operational performance and customer support efficiency.

### KPIs

- Average Resolution Hours
- Average Customer Satisfaction
- Average First Response Time

### Visualizations

- Most Common Ticket Types
- Average Resolution Hours by Priority
- Average Customer Satisfaction by Product
- Resolution Hours vs Customer Satisfaction (Scatter Plot)

---

## Page 3 — AI Risk Monitoring

Monitors customer sentiment and identifies high-risk unresolved tickets.

### KPIs

- High Risk Tickets
- Negative Sentiment
- Needs Alert

### Visualizations

- Sentiment Distribution
- Risk Level by Priority
- High Risk Ticket Table
- AI Recommendation Panel

---

## Automation Workflow Design

The project includes a rule-based workflow to automatically identify tickets requiring immediate attention.

```
New Ticket
      │
      ▼
Data Cleaning
      │
      ▼
AI Sentiment Analysis
      │
      ▼
Check Ticket Priority
      │
      ▼
Check Ticket Status
      │
      ▼
Negative Sentiment?
      │
      ▼
Yes
      │
      ▼
High Risk Ticket
      │
      ▼
Needs Alert = Yes
```

This workflow demonstrates how business rules can be combined with AI-assisted sentiment analysis to support faster ticket prioritization.

---

## Business Insights

The dashboard enables several operational insights, including:

- Technical Support tickets generated the highest number of customer requests.
- Products with longer average resolution times generally received lower customer satisfaction ratings.
- High-priority unresolved tickets were more likely to have negative customer sentiment.
- Email and Chat were the most frequently used customer support channels.
- A small number of products accounted for a large proportion of support tickets, indicating potential product quality or usability issues.

---

## Business Recommendations

Based on the analysis, the following recommendations were identified:

- Prioritize unresolved High Risk tickets to improve customer satisfaction.
- Review products generating the highest complaint volumes.
- Reduce response and resolution times for High Priority tickets.
- Monitor negative sentiment tickets daily to identify customer pain points.
- Consider implementing automated notifications for High Risk support cases.

---

## Repository Structure

```
AI-Customer-Support-Ticket-Analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── python/
│
├── sql/
│
├── dashboard/
│   ├── Customer Support Dashboard.pbix
│   └── dashboard_screenshots/
│
├── images/
│
├── README.md
│
└── requirements.txt
```

---

## Future Improvements

Potential future enhancements include:

- Connect Power BI directly to MySQL for live reporting.
- Integrate Power Automate for automated email notifications.
- Develop a machine learning model for ticket classification.
- Publish the dashboard using Power BI Service.
- Create real-time monitoring using streaming data.

---

## Skills Demonstrated

- Data Cleaning
- Exploratory Data Analysis (EDA)
- SQL Querying
- Database Management (MySQL)
- Python (Pandas)
- AI-Assisted Sentiment Analysis
- Rule-Based Risk Classification
- Data Visualization
- Power BI Dashboard Development
- Business Intelligence
- Data Storytelling
- Business Recommendations

---
