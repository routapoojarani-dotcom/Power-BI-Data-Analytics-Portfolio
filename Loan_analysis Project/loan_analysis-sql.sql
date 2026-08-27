
-- 1. DATA UNDERSTANDING

SELECT *
FROM Loan_default;

SELECT COUNT(*) AS Total_Records
FROM Loan_default;


-- 2. DATA QUALITY

-- Missing values
SELECT
    SUM(CASE WHEN Income IS NULL THEN 1 ELSE 0 END) AS Missing_Income,
    SUM(CASE WHEN LoanAmount IS NULL THEN 1 ELSE 0 END) AS Missing_LoanAmount,
    SUM(CASE WHEN CreditScore IS NULL THEN 1 ELSE 0 END) AS Missing_CreditScore
FROM Loan_default;


-- Duplicate Loan IDs
SELECT LoanID, COUNT(*)
FROM Loan_default
GROUP BY LoanID
HAVING COUNT(*) > 1;


-- 3. BASIC BUSINESS ANALYSIS

SELECT
    EmploymentType,
    COUNT(*) AS Total_Loans
FROM Loan_default
GROUP BY EmploymentType;


-- Default rate
SELECT
    100.0 * SUM(CASE WHEN Default = 1 THEN 1 ELSE 0 END)
    / COUNT(*) AS Default_Rate
FROM Loan_default;


-- Default rate by employment
SELECT
    EmploymentType,
    COUNT(*) AS Total_Loans,
    SUM(CASE WHEN Default = 1 THEN 1 ELSE 0 END) AS Defaults,
    100.0 *
    SUM(CASE WHEN Default = 1 THEN 1 ELSE 0 END)
    / COUNT(*) AS Default_Rate
FROM Loan_default
GROUP BY EmploymentType;