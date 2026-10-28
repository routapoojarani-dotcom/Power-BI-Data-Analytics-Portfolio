# 📊 Sales Operations Performance & MIS Dashboard

## 🔹 Project Overview
This project simulates a real-world **MIS Executive / Operations Analyst workflow**, starting from raw sales data to clean reporting, exception handling, KPI calculation, and dashboard visualization using **Microsoft Excel and Power BI**.

The objective is to demonstrate **data cleaning, validation, reporting accuracy, and business insights**, similar to what is expected in corporate MIS and operations roles.

---

## 🔹 Tools Used
- **Microsoft Excel** (Advanced formulas, Pivot Tables, Dashboards,Data preparation and analysis)
- **Power BI Desktop** (Data modeling, DAX, interactive visual Dashboard)
 
---
## 🔹 Dataset Source
This project uses a publicly available sales dataset from Kaggle for educational and demonstration purposes.

Source: Kaggle – Sales Dataset  
🔗 Dataset Link:  
[Sales Dataset on Kaggle](https://www.kaggle.com/datasets/lawrenceekeogu/sales-dataset?resource=download)

---
## 🔹 Data Workflow Architecture

### **Raw_Data**
- Original transactional sales data  
- No modifications made  

### **Cleaned_Data**
- Blank customer names replaced with **Unknown Customer**  
- Units Sold defaulted to **1** where missing  
- Auto-generated **Order IDs**  
- Proper case formatting applied  

### **MIS Pivot Reports**
- **Daily_Sales_MIS** → Date-wise revenue & order count  
- **Product_MIS** → Product-wise units & revenue  
- **State_MIS** → State-wise orders & revenue  
- **Channel_MIS** → Channel contribution analysis  

### **KPI_Backend**
- Total Revenue  
- Total Orders  
- Average Order Value (AOV)  
- Top Product & Top State (dynamic)  

### **Exception_Report**
Flags operational data issues:
- Zero Unit Price  
- Zero Revenue  
- Duplicate Order IDs  
- Missing Dates  

Includes:
- Exception reasons  
- Exception summary counts  

### **Power BI Dashboard**
- Monthly Revenue Trend  
- Units Sold by Product
- Channel Contribution  
- KPI Cards [Total Revenue ,Total Orders , Average Order Value (AOV)]
- Slicers(state,Year,Sales Channel)  

---

## 🔹 Business Assumptions
- Blank Units Sold → assumed as **1**  
- Blank Customer Name → marked as **Unknown Customer**  
- Blank Order ID → auto-generated  
- Data validation handled via **exception logic**  

---

## 🔹 Key Learning Outcomes
- End-to-end MIS reporting lifecycle  
- Data quality validation (OPS + MIS combination)  
- KPI calculation and interpretation  
- Dashboard storytelling using Excel & Power BI  

---