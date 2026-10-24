SELECT 
      [ProductID] as 'Product ID',
      [ProductName] as 'Product Name',
      [Price],
      CASE 
        WHEN [price] > 300 THEN 'High'
        WHEN [Price] > 150 THEN 'Medium'
        ELSE 'Low'
        END as 'Price Category'
  FROM [MarketingData].[dbo].[products]
