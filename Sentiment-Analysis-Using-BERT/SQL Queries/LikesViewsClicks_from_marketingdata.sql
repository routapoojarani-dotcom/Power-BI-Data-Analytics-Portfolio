SELECT 
        EngagementID as 'Engagement ID',
        UPPER(contenttype) as 'Content Type',
        CONVERT( date, EngagementDate) as 'Engagement Date',
        ProductID as 'Product ID',
        likes as 'Likes',
        CAST((SUBSTRING([ViewsClicksCombined], 1, CHARINDEX('-', [ViewsClicksCombined]) - 1)) as INT) AS 'Views',
        CAST((SUBSTRING([ViewsClicksCombined],CHARINDEX('-', [ViewsClicksCombined]) + 1,LEN([ViewsClicksCombined]))) as INT) AS 'Clicks'

  FROM [MarketingData].[dbo].[engagement_data];
