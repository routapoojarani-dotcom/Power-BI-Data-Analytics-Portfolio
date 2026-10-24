--Create View Journey as
WITH CTE_Duplicates as
    (SELECT 
       [JourneyID] as 'Journey ID'
      ,[CustomerID] as 'Customer ID'
      ,[ProductID] as 'Product ID'
      ,CONVERT(DATE,[VisitDate]) as 'Visiting Date'
      ,UPPER([Stage]) AS 'Customer Stage'
      ,[Action]
      ,COALESCE([DURATION], AVG([Duration]) over(partition by [Stage])) as 'Duration'
      ,ROW_NUMBER() over(partition by [customerid],[productid],[visitdate],[stage],[action] order by [Visitdate]) as Rnk
  FROM [MarketingData].[dbo].[customer_journey])
  SELECT 
  [Journey ID],
  [Customer ID],
  [Product ID],
  [Visiting Date],
  [Customer Stage],
  [Action],
  [Duration]
  FROM CTE_Duplicates
  WHERE Rnk = 1