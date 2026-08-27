# Housing Market Analysis

## Project Overview

An end-to-end Business Intelligence and Data Analytics project focused on analyzing housing transaction data to understand property pricing, regional sales performance, property characteristics, and market trends.

The project combines **SQL, Python, and Power BI** to perform data validation, data cleaning, exploratory analysis, transformation, data modeling, visualization, and interactive dashboard development.

The analysis covers **100,000 housing transactions** and examines patterns across regions, property types, property characteristics, pricing, transaction details, and sales performance.

---

## Business Objective

The primary objective of this project is to analyze housing transaction data to:

- Understand housing sales and pricing patterns
- Compare sales performance across different regions and areas
- Analyze property types and characteristics
- Examine factors related to property pricing
- Identify trends in housing transactions over time
- Perform data-quality and consistency checks
- Develop interactive Power BI reports and visualizations
- Convert housing data into meaningful business insights

---

## Dataset

The dataset contains **100,000 housing transaction records** with information related to properties, transactions, pricing, location, and property characteristics.

Key data attributes include:

- Property / House ID
- Region
- Area
- Property Type
- Purchase Price
- Square Meters
- Number of Rooms
- Year Built
- Offer Type
- Purchase Date
- Sales / Transaction information
- Other property and transaction attributes

---

## Tools & Technologies

### Business Intelligence
- Power BI Desktop
- DAX
- Power Query
- Data Modeling
- Interactive Dashboards
- Data Visualization
- KPI Reporting

### Database & SQL
- SQL
- SQL Server
- Data Validation
- Data Quality Checks
- Data Cleaning
- Data Transformation
- Aggregation
- Business Analysis

### Programming & Analytics
- Python
- Pandas
- NumPy
- Exploratory Data Analysis

---

## Project Workflow

Raw Housing Transaction Data
            ↓
Data Quality & Validation
            ↓
SQL Cleaning & Analysis
            ↓
Python Exploratory Analysis
            ↓
Data Transformation
            ↓
Power BI Data Model
            ↓
DAX Calculations & KPIs
            ↓
Interactive Dashboard
            ↓
Housing Market Insights
Data Quality & Validation

A detailed data-quality assessment was performed before the analysis to improve the reliability and consistency of the dataset.

## The SQL validation process included:

Checking for missing values
Identifying duplicate house_id records
Validating purchase prices
Checking property size values
Validating room counts
Checking year-built values
Validating offer and purchase information
Checking transaction dates
Validating quarter classifications
Identifying negative or invalid numerical values
Checking blank or inconsistent text values
Removing duplicate records using SQL window functions
Cleaning text fields using LTRIM() and RTRIM()

These checks helped identify potential data-quality issues and prepare a cleaner dataset for analysis and reporting.

## SQL Analysis

SQL was used for data exploration, validation, cleaning, transformation, and business analysis.

Key SQL activities included:

Record-count analysis
Missing-value analysis
Duplicate property detection
Property-price validation
Property-size validation
Room-count validation
Year-built validation
Date and quarter validation
Offer and purchase analysis
Regional analysis
Property-type analysis
Sales and pricing analysis
Data cleaning and preparation
Example Business Questions
How does housing sales performance vary across regions?
Which property types are most common?
How do property prices vary across locations?
How does property size relate to purchase price?
How do housing transactions change over time?
What patterns can be observed across different property segments?
Are there data-quality issues that could affect the analysis?

## Python Analysis

Python was used for data inspection, cleaning, exploratory analysis, and preparation of the housing data.

Key activities included:

Loading and inspecting the dataset
Exploring data distributions
Identifying missing and inconsistent values
Data cleaning and preprocessing
Exploratory Data Analysis (EDA)
Examining relationships between housing attributes
Preparing data for visualization and reporting
Libraries Used
Pandas
NumPy
Matplotlib
Seaborn

Python analysis provided an additional analytical layer before developing the Power BI report.

## Power BI Development

Power BI Desktop was used to transform the cleaned housing data into interactive analytical reports.

The Power BI development process included:

Importing and preparing data
Data transformation using Power Query
Building a data model
Creating analytical calculations using DAX
Developing KPI-focused visualizations
Designing interactive reports
Analyzing regional sales performance
Comparing property types and characteristics
Visualizing housing prices and sales trends

## Power BI Dashboard

The dashboard focuses on several key areas of housing market analysis.

Regional Sales Analysis

Provides a visual comparison of housing sales performance across different regions and areas.

The analysis helps identify:

Regional sales patterns
Differences in sales performance
Geographic distribution of transactions
Regional housing trends
Property & Pricing Analysis
Examines the relationship between property characteristics and pricing.

## The analysis covers:

Property types
Purchase prices
Property size
Number of rooms
Year built
Other property characteristics
Sales Trend Analysis
Visualizes housing transaction activity over time to identify changes and trends in the market.

The report provides an interactive view of:
Transaction trends
Time-based sales patterns
Regional changes
Property-segment trends
Key Findings
Analyzed 100,000 housing transactions to understand property pricing, regional sales, property characteristics, and transaction trends.
Performed extensive data-quality validation covering missing values, duplicate property IDs, invalid prices, property sizes, room counts, year-built values, dates, and categorical fields.
Identified and addressed data inconsistencies before using the dataset for downstream analysis.
Used SQL to perform data cleaning, validation, transformation, and analytical queries.
Examined housing performance across regions, areas, property types, pricing, size, rooms, and transaction characteristics.
Used Python for exploratory analysis and preparation of housing data for reporting.
Developed an interactive Power BI report to analyze regional sales, property pricing, property characteristics, and housing trends.
Combined SQL, Python, and Power BI into an end-to-end analytical workflow for converting raw housing transaction data into structured business insights.

## Project Files
File	Description
house_data-sql.sql	SQL queries for data validation, cleaning, transformation, and analysis
House_data-Power BI.ipynb	Python-based exploratory analysis and data preparation
House_data-Power BI.pbix	Power BI report, data model, calculations, and dashboard
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
Data Cleaning
Data Transformation
Aggregation
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
Data Quality Assessment
KPI Analysis
Business Reporting
Data-Driven Insights

## Conclusion

This project demonstrates an end-to-end Business Intelligence workflow for housing market analysis, from data validation and SQL-based cleaning to Python exploration and Power BI reporting.

The project shows how structured data-quality checks, analytical techniques, data modeling, and interactive visualization can be combined to transform raw housing transaction data into useful insights about sales performance, property characteristics, pricing, and market trends
