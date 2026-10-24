CREATE TABLE IF NOT EXISTS customer_churn (
    CustomerID        INTEGER PRIMARY KEY,
    Age               INTEGER,
    Gender            VARCHAR(10),
    Tenure            INTEGER,
    MonthlyCharges    DECIMAL(10,2),
    Contract          VARCHAR(20),
    PaymentMethod     VARCHAR(30),
    TotalCharges      DECIMAL(10,2),
    Churn             VARCHAR(5),
    Churn_Binary      INTEGER,       -- 1 = Churned, 0 = Retained
    TenureGroup       VARCHAR(20),
    AvgMonthlySpend   DECIMAL(10,2),
    HighRisk          INTEGER,       -- 1 = High risk, 0 = Standard
    AgeGroup          VARCHAR(10),
    Gender_Enc        INTEGER,
    Contract_Enc      INTEGER
);


-- OVERALL CHURN RATE
SELECT
    COUNT(*)                                        AS total_customers,
    SUM(Churn_Binary)                               AS churned_customers,
    COUNT(*) - SUM(Churn_Binary)                    AS retained_customers,
    ROUND(AVG(Churn_Binary) * 100.0, 2)             AS churn_rate_pct,
    ROUND((1 - AVG(Churn_Binary)) * 100.0, 2)       AS retention_rate_pct
FROM customer_churn;

-- CHURN BY CONTRACT TYPE
SELECT
    Contract,
    COUNT(*)                                    AS total_customers,
    SUM(Churn_Binary)                           AS churned,
    ROUND(AVG(Churn_Binary) * 100.0, 2)         AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)               AS avg_monthly_charges,
    ROUND(SUM(TotalCharges), 2)                 AS total_revenue
FROM customer_churn
GROUP BY Contract
ORDER BY churn_rate_pct DESC;


-- ============================================================
-- CHURN BY TENURE GROUP
SELECT
    TenureGroup,
    COUNT(*)                                    AS total_customers,
    SUM(Churn_Binary)                           AS churned,
    ROUND(AVG(Churn_Binary) * 100.0, 2)         AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)               AS avg_monthly_charges
FROM customer_churn
WHERE TenureGroup IS NOT NULL
GROUP BY TenureGroup
ORDER BY
    CASE TenureGroup
        WHEN '0-12 months'  THEN 1
        WHEN '13-24 months' THEN 2
        WHEN '25-48 months' THEN 3
        WHEN '49-72 months' THEN 4
    END;

-- CHURN BY PAYMENT METHOD
SELECT
    PaymentMethod,
    COUNT(*)                                    AS total_customers,
    SUM(Churn_Binary)                           AS churned,
    ROUND(AVG(Churn_Binary) * 100.0, 2)         AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)               AS avg_monthly_charges
FROM customer_churn
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;

-- REVENUE IMPACT OF CHURN
SELECT
    Churn,
    COUNT(*)                                        AS customers,
    ROUND(SUM(TotalCharges), 0)                     AS total_revenue,
    ROUND(AVG(TotalCharges), 2)                     AS avg_revenue_per_customer,
    ROUND(AVG(MonthlyCharges), 2)                   AS avg_monthly_charges,
    ROUND(SUM(MonthlyCharges), 0)                   AS monthly_revenue_impact
FROM customer_churn
GROUP BY Churn;

-- HIGH-RISK CUSTOMER SEGMENTS
SELECT
    Contract,
    TenureGroup,
    CASE
        WHEN MonthlyCharges >= 100 THEN 'High Spend (>=100)'
        WHEN MonthlyCharges >= 60  THEN 'Mid Spend (60-99)'
        ELSE                            'Low Spend (<60)'
    END                                             AS SpendTier,
    COUNT(*)                                        AS customers,
    SUM(Churn_Binary)                               AS churned,
    ROUND(AVG(Churn_Binary) * 100.0, 2)             AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)                   AS avg_monthly_charges,
    ROUND(SUM(MonthlyCharges), 0)                   AS monthly_revenue_at_risk
FROM customer_churn
WHERE Contract = 'Month-to-month'
  AND TenureGroup = '0-12 months'
GROUP BY Contract, TenureGroup, SpendTier
ORDER BY churn_rate_pct DESC;

-- HIGH-RISK FLAG VALIDATION
SELECT
    HighRisk,
    COUNT(*)                                    AS customers,
    SUM(Churn_Binary)                           AS churned,
    ROUND(AVG(Churn_Binary) * 100.0, 2)         AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)               AS avg_monthly_charges,
    ROUND(SUM(MonthlyCharges), 0)               AS monthly_revenue_at_risk
FROM customer_churn
GROUP BY HighRisk
ORDER BY HighRisk DESC;

-- AGE GROUP CHURN ANALYSIS
SELECT
    AgeGroup,
    COUNT(*)                                    AS customers,
    SUM(Churn_Binary)                           AS churned,
    ROUND(AVG(Churn_Binary) * 100.0, 2)         AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2)               AS avg_monthly_charges
FROM customer_churn
WHERE AgeGroup IS NOT NULL
GROUP BY AgeGroup
ORDER BY AgeGroup;

-- CONTRACT UPGRADE OPPORTUNITY

WITH mtm_churners AS (
    SELECT
        COUNT(*)                    AS mtm_churned_count,
        ROUND(SUM(MonthlyCharges), 0) AS monthly_rev_lost,
        ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charge
    FROM customer_churn
    WHERE Contract    = 'Month-to-month'
      AND Churn_Binary = 1
),
annual_churn_rate AS (
    SELECT ROUND(AVG(Churn_Binary) * 100.0, 2) AS annual_churn_pct
    FROM customer_churn
    WHERE Contract IN ('One year', 'Two year')
)
SELECT
    m.mtm_churned_count,
    m.monthly_rev_lost,
    m.avg_monthly_charge,
    a.annual_churn_pct                      AS annual_contract_churn_rate,
    ROUND(
        m.monthly_rev_lost *
        (1 - a.annual_churn_pct / 100.0), 0
    )                                       AS estimated_monthly_revenue_saved
FROM mtm_churners m, annual_churn_rate a;

-- WINDOW FUNCTION — RUNNING CHURN RATE BY TENURE
WITH tenure_summary AS (
    SELECT
        Tenure,
        COUNT(*)            AS customers,
        SUM(Churn_Binary)   AS churned
    FROM customer_churn
    GROUP BY Tenure
),
running AS (
    SELECT
        Tenure,
        customers,
        churned,
        SUM(customers) OVER (ORDER BY Tenure)   AS cumulative_customers,
        SUM(churned)   OVER (ORDER BY Tenure)   AS cumulative_churned
    FROM tenure_summary
)
SELECT
    Tenure,
    customers,
    churned,
    ROUND(churned * 100.0 / customers, 2)                       AS monthly_churn_rate,
    cumulative_customers,
    cumulative_churned,
    ROUND(cumulative_churned * 100.0 / cumulative_customers, 2) AS cumulative_churn_rate
FROM running
ORDER BY Tenure
LIMIT 24;  -- First 24 months — the critical early window