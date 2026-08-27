-- 1. DATA UNDERSTANDING

SELECT *
FROM Housing_Data;


SELECT COUNT(*) AS Total_Records
FROM Housing_Data;


-- Number of columns / basic structure
SELECT
    COUNT(DISTINCT house_id) AS Unique_Houses
FROM Housing_Data;


-- 2. DATA QUALITY

-- Missing values
SELECT
    SUM(CASE WHEN date IS NULL THEN 1 ELSE 0 END) AS Missing_Date,
    SUM(CASE WHEN quarter IS NULL THEN 1 ELSE 0 END) AS Missing_Quarter,
    SUM(CASE WHEN house_id IS NULL THEN 1 ELSE 0 END) AS Missing_HouseID,
    SUM(CASE WHEN house_type IS NULL THEN 1 ELSE 0 END) AS Missing_HouseType,
    SUM(CASE WHEN sales_type IS NULL THEN 1 ELSE 0 END) AS Missing_SalesType,
    SUM(CASE WHEN purchase_price IS NULL THEN 1 ELSE 0 END) AS Missing_PurchasePrice,
    SUM(CASE WHEN sqm IS NULL THEN 1 ELSE 0 END) AS Missing_SQM,
    SUM(CASE WHEN sqm_price IS NULL THEN 1 ELSE 0 END) AS Missing_SQMPrice,
    SUM(CASE WHEN city IS NULL THEN 1 ELSE 0 END) AS Missing_City,
    SUM(CASE WHEN area IS NULL THEN 1 ELSE 0 END) AS Missing_Area,
    SUM(CASE WHEN region IS NULL THEN 1 ELSE 0 END) AS Missing_Region
FROM Housing_Data;


-- Missing economic indicators
SELECT
    SUM(CASE WHEN nom_interest_rate% IS NULL THEN 1 ELSE 0 END) AS Missing_Interest_Rate,
    SUM(CASE WHEN dk_ann_infl_rate% IS NULL THEN 1 ELSE 0 END) AS Missing_Inflation,
    SUM(CASE WHEN yield_on_mortgage_credit_bonds% IS NULL THEN 1 ELSE 0 END) AS Missing_Mortgage_Yield
FROM Housing_Data;


-- Duplicate House IDs
SELECT
    house_id,
    COUNT(*) AS Record_Count
FROM Housing_Data
GROUP BY house_id
HAVING COUNT(*) > 1;


-- 3. DISTINCT VALUES / CATEGORICAL CHECKS

SELECT DISTINCT house_type
FROM Housing_Data
ORDER BY house_type;


SELECT DISTINCT sales_type
FROM Housing_Data
ORDER BY sales_type;


SELECT DISTINCT region
FROM Housing_Data
ORDER BY region;


SELECT DISTINCT area
FROM Housing_Data
ORDER BY area;


-- 4. DATA VALIDATION

-- Invalid / zero purchase prices
SELECT *
FROM Housing_Data
WHERE purchase_price <= 0;


-- Invalid / zero SQM
SELECT *
FROM Housing_Data
WHERE sqm <= 0;


-- Invalid SQM prices
SELECT *
FROM Housing_Data
WHERE sqm_price <= 0;


-- Invalid number of rooms
SELECT *
FROM Housing_Data
WHERE no_rooms <= 0;


-- Invalid year built
SELECT *
FROM Housing_Data
WHERE year_build < 1000
   OR year_build > YEAR(GETDATE());


-- Invalid offer vs purchase percentage
SELECT *
FROM Housing_Data
WHERE [%_change_between_offer_and_purchase] < -100;


-- 5. DATE / TIME VALIDATION

SELECT
    MIN(date) AS Earliest_Date,
    MAX(date) AS Latest_Date
FROM Housing_Data;


SELECT DISTINCT
    quarter
FROM Housing_Data
ORDER BY quarter;


-- Check that quarter matches the date
SELECT *
FROM Housing_Data
WHERE quarter <> CONCAT(
    YEAR(date),
    'Q',
    DATEPART(QUARTER, date)
);


-- 6. NUMERIC / TEXT CLEANING CHECKS

-- Check for negative values
SELECT *
FROM Housing_Data
WHERE purchase_price < 0
   OR sqm < 0
   OR sqm_price < 0
   OR no_rooms < 0
   OR year_build < 0;


-- Check for unexpected blank text values
SELECT *
FROM Housing_Data
WHERE LTRIM(RTRIM(house_type)) = ''
   OR LTRIM(RTRIM(sales_type)) = ''
   OR LTRIM(RTRIM(city)) = ''
   OR LTRIM(RTRIM(region)) = '';


-- 7. DUPLICATE CHECK USING WINDOW FUNCTION

WITH Duplicate_Check AS
(
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY house_id
            ORDER BY date DESC
        ) AS rn
    FROM Housing_Data
)

SELECT *
FROM Duplicate_Check
WHERE rn > 1;


-- 8. CLEAN DATASET

WITH Cleaned_Data AS
(
    SELECT
        date,
        quarter,
        house_id,
        LTRIM(RTRIM(house_type)) AS house_type,
        LTRIM(RTRIM(sales_type)) AS sales_type,
        year_build,
        purchase_price,
        [%_change_between_offer_and_purchase],
        no_rooms,
        sqm,
        sqm_price,
        LTRIM(RTRIM(city)) AS city,
        area,
        LTRIM(RTRIM(region)) AS region,
        nom_interest_rate%,
        dk_ann_infl_rate%,
        yield_on_mortgage_credit_bonds%
    FROM Housing_Data
    WHERE house_id IS NOT NULL
      AND date IS NOT NULL
)

SELECT *
FROM Cleaned_Data;