SELECT 
        c.CustomerID as 'Customer ID',
        c.Gender,
        c.Age,
        g.Country as Country,
        g.City as City
  FROM [MarketingData].[dbo].[customers] as c
  Left join [MarketingData].[dbo].[Geography] as g
  on c.GeographyID = g.GeographyID