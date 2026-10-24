SELECT
    ReviewID    as 'Review ID',
    CustomerID  as 'Customer ID',
    ProductID   as 'Product ID',
    CONVERT( date, ReviewDate ) as 'Review Date',
    Rating,
    REPLACE(ReviewText, '  ', ' ') as 'Review Text'
FROM [MarketingData].[dbo].[customer_reviews]