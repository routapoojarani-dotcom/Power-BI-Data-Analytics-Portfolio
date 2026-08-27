# Loan Default Analysis

## Project Overview

An end-to-end Business Intelligence and Data Analytics project focused on analyzing loan application data to understand borrower characteristics, financial profiles, and factors associated with loan default risk.

The project combines **SQL, Python, and Power BI** to perform data validation, data cleaning, exploratory analysis, analytical calculations, data modeling, and interactive dashboard development.

The analysis covers **255,347 loan records** and identifies patterns in loan defaults across borrower demographics, employment characteristics, financial indicators, credit profiles, and loan attributes.


## Business Objective

The primary objective of this project is to analyze loan application and borrower data to:

- Understand overall loan default performance
- Identify patterns associated with loan default risk
- Analyze borrower demographics and financial characteristics
- Compare default rates across different borrower segments
- Evaluate key financial and credit-related risk indicators
- Develop interactive Power BI reports and KPI-focused dashboards
- Convert analytical results into meaningful business insights


## Dataset

The dataset contains **255,347 loan application records** with information related to borrowers, loans, financial characteristics, credit profiles, and loan outcomes.

Key data attributes include:

- Loan ID
- Income
- Loan Amount
- Credit Score
- Employment Type
- Loan Status
- Borrower characteristics
- Loan characteristics
- Other financial and demographic attributes


## Tools & Technologies

### Business Intelligence
- Power BI Desktop
- DAX
- Power Query
- Data Modeling
- Interactive Dashboards
- KPI Reporting
- Data Visualization

### Database & SQL
- SQL Server
- SQL
- Data Validation
- Data Quality Checks
- Aggregation
- Business Analysis

### Programming & Analytics
- Python
- Pandas
- NumPy
- Exploratory Data Analysis

## Project Workflow

Raw Loan Data
      ↓
Data Quality & Validation
      ↓
SQL Analysis
      ↓
Python Data Cleaning & Exploration
      ↓
Data Transformation
      ↓
Power BI Data Model
      ↓
DAX Measures & KPIs
      ↓
Interactive Dashboard
      ↓
Business Insights
Data Quality & Validation

## Before performing the analysis, the dataset was examined for data-quality issues using SQL.
## The validation process included:
Checking total record counts
Identifying missing values
Checking for duplicate Loan IDs
Validating important financial fields
Examining income and loan amount distributions
Checking credit score data
Reviewing categorical fields such as employment type
Validating data consistency before analysis
These checks helped ensure that the data was suitable for downstream analysis and reporting.

## SQL Analysis
SQL was used to perform data exploration, validation, aggregation, and business analysis.
Key SQL analyses included:
Total loan record analysis
Missing-value checks
Duplicate Loan ID detection
Borrower and employment analysis
Loan amount analysis
Credit score analysis
Overall loan default calculation
Default-rate analysis by employment type
Segment-level analysis of loan performance
Example Business Questions
What is the overall loan default rate?
How many loans are classified as defaulted?
Are there differences in default rates across employment categories?
What are the characteristics of borrowers with different loan outcomes?
How do financial and credit-related characteristics vary across loan segments?

## Python Analysis
Python was used for exploratory data analysis and data preparation.
Key activities included:
Data loading and inspection
Data cleaning
Missing-value analysis
Exploratory Data Analysis (EDA)
Distribution analysis
Feature-level exploration
Preparation of data for visualization and reporting
Libraries Used
Pandas
NumPy
Matplotlib
Seaborn
Python analysis helped identify patterns and relationships that could be further explored through Power BI.

## Power BI Development
Power BI Desktop was used to transform the analysis into an interactive Business Intelligence report.
The Power BI development process included:
Importing and preparing data
Data transformation using Power Query
Building a data model
Creating DAX measures
Developing KPI calculations
Designing interactive visual reports
Creating borrower and loan segment analysis
Developing financial risk visualizations
Creating an interactive dashboard for business analysis

## Power BI Dashboard
The dashboard is organized into three main analytical views.
## 1. Loan Default Overview
Provides a high-level view of loan portfolio performance and default trends.
Key areas include:
Overall loan performance
Default rate
Loan volume
Default trends
Portfolio-level indicators

## 2. Application Demographics & Financial Profile
Analyzes borrower characteristics and financial attributes.
The report examines areas such as:
Applicant demographics
Employment characteristics
Income
Loan characteristics
Credit profile
Borrower segmentation

## 3. Financial Risk Metrics
Focuses on financial indicators associated with loan performance and default risk.
The dashboard provides a visual view of:
Financial risk indicators
Loan-related metrics
Credit-related characteristics
Default patterns across borrower segments

## Key Findings
A total of 255,347 loan records were analyzed.
The overall loan default rate was 11.61%.
Loan default patterns were analyzed across employment type, borrower demographics, financial characteristics, credit profiles, and loan attributes.
Data-quality analysis identified and evaluated potential issues such as missing values and duplicate Loan IDs before the analytical stage.
Default rates were calculated at both the overall and segment levels to compare loan risk across different borrower groups.
The analysis provides a structured view of borrower characteristics, financial profiles, and loan risk indicators.
Power BI was used to convert the analysis into interactive reports and KPI-focused dashboards for easier interpretation of loan performance and risk.

## Project Files
File	Description
loan_analysis-sql.sql	SQL queries for data validation, exploration, and business analysis
loan_analysis-python.ipynb	Python-based data cleaning and exploratory analysis
loan_analysis-powerbi.pbix	Power BI report, data model, DAX calculations, and dashboard
Screenshots/	Power BI dashboard previews

## Skills Demonstrated
Power BI
Power BI Desktop
Power Query
DAX
Data Modeling
Dashboard Development
KPI Reporting
Interactive Data Visualization
SQL
Data Exploration
Data Validation
Data Quality Checks
Aggregation
Filtering
Grouping
Business Analysis
Python
Pandas
NumPy
Data Cleaning
Exploratory Data Analysis
Data Visualization
Business Intelligence
Data Transformation
Analytical Problem Solving
KPI Analysis
Business Insights
Data-Driven Reporting

## Conclusion

This project demonstrates an end-to-end approach to Business Intelligence, starting from data validation and SQL analysis through Python-based exploration and ending with Power BI data modeling, DAX calculations, KPI reporting, and interactive dashboard development.

The project demonstrates how raw loan application data can be transformed into structured analytical insights to support understanding of loan performance and default risk.
