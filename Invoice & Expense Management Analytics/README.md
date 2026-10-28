# Invoice & Expense Management Analytics

An interactive **Microsoft Excel dashboard** designed to analyze invoice data, monitor business expenses, evaluate vendor spending, track payment status, and generate actionable business insights.

This project demonstrates practical **Excel data-cleaning, lookup, aggregation, duplicate detection, analysis, and dashboard-building skills** using a realistic invoice dataset.

---
## Project Overview

The **Invoice & Expense Management Analytics** transforms raw invoice records into a structured analytical report that helps answer key business questions:

* How much has the business spent?
* How many invoices have been recorded?
* How much has been paid, is pending, or is overdue?
* Which expense categories consume the most budget?
* Which vendors account for the highest spending?
* How does spending change month by month?
* Are there duplicate invoice records?
* What business actions can be taken from the data?

The workbook follows a complete workflow:

**Raw Data → Data Cleaning → Vendor Mapping → Analysis → Dashboard → Business Insights**

---

## Tools & Skills

| Tool / Skill           | Application                               |
| ---------------------- | ----------------------------------------- |
| Microsoft Excel        | Data processing and dashboard development |
| XLOOKUP                | Vendor information mapping                |
| SUMIFS                 | Expense aggregation                       |
| COUNTIFS               | Invoice and status analysis               |
| Data Cleaning          | Standardizing and preparing invoice data  |
| Duplicate Detection    | Identifying repeated invoice records      |
| PivotTables / Analysis | Expense and vendor analysis               |
| Dashboard Design       | KPI and management reporting              |
| Business Analysis      | Converting data into actionable insights  |

---

## Workbook Structure

### 1. `Raw Data`

Contains the original invoice dataset, including:

* Invoice ID
* Invoice Date
* Due Date
* Vendor ID
* Vendor Name
* Expense Category
* Department
* Description
* Quantity
* Unit Cost
* Invoice Amount
* Payment Status

The raw dataset contains **83 invoice records**, including deliberate duplicate records for testing duplicate-detection logic.

---

### 2. `Vendor Mapping`

A reference table used to map vendor information and categorize vendors.

Fields include:

* Vendor ID
* Vendor Name
* Department
* Vendor Category

This sheet demonstrates how lookup functions can be used to enrich transactional data.

---

### 3. `Project Notes`

Documents the purpose of the project and explains the data-cleaning and analysis exercises included in the workbook.

---

### 4. `Cleaned Data`

Contains the processed invoice dataset with additional calculated fields and duplicate-check logic.

This layer separates the original source data from the analysis-ready dataset.

---

### 5. `Analysis`

Contains the calculations used to power the dashboard, including:

* Total Expenses
* Total Invoices
* Paid Amount
* Pending Amount
* Overdue Amount
* Duplicate Invoice Records
* Expense by Category
* Expense by Vendor
* Invoice Count by Payment Status
* Monthly Expense Trends

---

### 6. `Dashboard`

The main reporting page containing high-level KPIs and visual analysis.

Key metrics include:

|      KPI       |     Value      |
| -------------- | -------------: |
| Total Expenses | **644,365.57** |
| Total Invoices |         **83** |
| Paid Amount    | **396,411.13** |
| Pending Amount | **176,934.52** |
| Overdue Amount |  **71,019.92** |

---

### 7. `Insights`

Summarizes the major findings from the analysis and translates the numbers into business-oriented observations.

---

## Key Business Insights

### Highest-Spend Category

**Facilities** is the largest expense category, with total spending of approximately:

**161,792.97**

This suggests that facilities-related costs represent a significant portion of overall business expenditure and may be an area worth reviewing for potential cost optimization.

---

### Highest-Spend Vendor

**Bright Marketing Co** is the highest-spend vendor, accounting for approximately:

**105,967.49**

A detailed review of the services, pricing, and contract terms with this vendor could help identify opportunities for savings.

---

### Payment Status

Of the total invoice value:

* **396,411.13** has been paid
* **176,934.52** is pending
* **71,019.92** is overdue

The pending and overdue balances should be monitored closely to improve cash-flow visibility and prevent late-payment issues.

---

### Duplicate Detection

The dataset contains **3 deliberate duplicate invoice records**.

Duplicate-check logic was incorporated into the cleaned dataset to demonstrate how repeated invoice combinations can be identified before financial reporting.

---

## Analysis Areas

The dashboard analyzes expenses across multiple dimensions:

### Expense Category

Identifies which categories contribute most to total spending.

### Vendor

Ranks vendors based on total invoice expenditure.

### Payment Status

Breaks invoices into:

* Paid
* Pending
* Overdue

### Monthly Trends

Tracks expense patterns throughout the year to identify periods of unusually high or low spending.

---

## Business Value

This dashboard can help finance and management teams:

* Monitor overall expenditure
* Identify high-cost categories
* Evaluate vendor concentration
* Track outstanding payments
* Identify overdue invoices
* Detect potential duplicate records
* Understand monthly spending patterns
* Support budgeting and cost-control decisions

---

## What This Project Demonstrates

This project showcases the ability to take a raw business dataset and turn it into a structured analytical solution.

### Data Preparation

* Cleaning transactional data
* Structuring datasets
* Mapping reference information
* Detecting duplicate records

### Data Analysis

* Aggregating financial metrics
* Analyzing vendors and categories
* Tracking payment statuses
* Examining monthly trends

### Data Visualization

* Designing KPI-driven dashboards
* Presenting financial information clearly
* Creating management-friendly reporting

### Business Intelligence

* Identifying spending patterns
* Highlighting financial risks
* Translating analysis into actionable insights

---

## How to Use

1. Download the Excel workbook.
2. Open `Invoice_Expense_Analysis_Dashboard.xlsx` in Microsoft Excel.
3. Start with the **Dashboard** sheet for a high-level overview.
4. Review the **Analysis** sheet to understand the underlying calculations.
5. Explore **Cleaned Data** to see the data-preparation process.
6. Review **Insights** for the key business findings.

---

## Project Files

```text
Invoice-Expense-Analysis/
│
├── 📊 Invoice_Expense_Analysis_Dashboard.xlsx
└── 📄 README.md
```

---

## Potential Future Improvements

The project could be extended with:

* Interactive date filters
* Department-level expense analysis
* Budget vs. actual spending
* Year-over-year expense comparisons
* Automated overdue-invoice alerts
* Vendor performance scoring
* Cost-per-department analysis
* Automated Power Query data refresh
* Power BI version of the dashboard

---