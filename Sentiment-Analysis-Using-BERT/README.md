# Sentiment Analysis Using BERT
## 📚Table of Contents:

|**No.**  |**Section**|
|:-: | :------------ | 
|1.   |  [Overview](#overview)                              |
|2.   |  [Business Context](#business-context)                              |
|3.   |  [Objectives](#objectives)                              |
|4.   |  [Data Overview](#data-overview)                              |
|5.   |  [Dashboard Highlights](#dashboard-highlights)                              |
|6.   |  [Key Findings](#key-findings)                              |
|7.   |  [Recommendations](#recommendations)                              |



## 🚀Overview
IronPlay is an online retail business that experienced a decline in customer engagement and conversion rates despite increased spending on digital marketing. The purpose of this project is to analyze customer behavior, marketing performance, and customer feedback to understand what is going wrong and where improvements are needed.

The focus of this analysis is on:
- Conversion funnel performance
- Customer engagement across marketing content
- Customer feedback and sentiment

## 📌Business Context:
Over recent months, IronPlay observed a steady decline in user interaction across both its website and marketing campaigns. Fewer visitors were progressing through the purchase journey and completing transactions, leading to a noticeable drop in conversion rates.

At the same time, marketing spend continued to increase, but this additional investment did not translate into corresponding revenue growth, raising concerns about traffic quality and campaign effectiveness.

In parallel, IronPlay accumulated a large volume of customer reviews and social media comments. While this feedback contained valuable signals about customer experience, it was not being analyzed in a structured or consistent way, making it difficult to identify recurring issues or priorities.

## 🎯Objectives:

### Improve Conversion Rates
- Identify where users drop off during the purchase journey
- Understand which channels and devices underperform
- Highlight friction points affecting checkout completion

### Improve Customer Engagement
- Compare engagement levels across different types of marketing content
- Identify channels that attract high-quality traffic
- Understand behavior differences between new and returning users

### Understand Customer Feedback
- Analyze customer reviews and social media comments
- Identify recurring positive and negative themes
- Link feedback patterns to engagement and conversion issues

## 🗂Data Overview
The analysis is based on:
- Website interaction and session data
- Conversion funnel data (visit → cart → purchase)
- Marketing campaign performance data
- Customer reviews and social media comments

The dataset is anonymized and structured to reflect a realistic e-commerce setup.

You can find the dataset here: [.bak file]()

## 📊Approach


Data preparation and ETL were handled upstream in SQL to keep the model lean and consistent. Core business metrics were implemented in DAX to support interactive analysis across filters, slicers, and dimensions within the report.

Customer feedback required separate processing. Reviews and social media comments were analyzed using Python to derive sentiment labels and key themes and the results were saved and joined back with behavioral and conversion data for analysis.

## 🖥Dashboard Highlights:
The IronPlay Analytics Dashboard is structured around three questions:

1. Are visitors converting? (Journey)

2. Are they still engaging with content? (Engagement)

3. What are customers actually saying? (Review)

Each page answers one question clearly, without mixing signals.


## 💡Key Findings

## Year-over-Year Performance Overview

### 2023: Strong Baseline
2023 represents IronPlay’s healthiest year across all major dimensions. Conversion rates were high, revenue was at its peak, and engagement metrics showed consistent interaction across products and months. The funnel behaved as expected, with reasonable drop-offs and strong checkout completion.

This year serves as the benchmark for evaluating subsequent performance.

### 2024: Structural Decline
In 2024, performance declined sharply across multiple areas:
- Conversion rate dropped significantly compared to 2023
- Revenue fell by ~10%
- Engagement metrics (likes, clicks) declined faster than traffic volume

The most notable change was increased drop-off at the checkout stage, indicating friction after purchase intent was already established. At the same time, engagement quality deteriorated, suggesting that marketing campaigns were driving weaker or less relevant traffic.
This was not a seasonal dip. The decline was consistent across months and products, pointing to a structural issue rather than short-term volatility.

### 2025: Stabilization, Not Recovery
In 2025, metrics stopped deteriorating, but they did not return to 2023 levels:
- Conversion rate improved slightly versus 2024
- Revenue remained essentially flat
- Engagement collapsed further, especially likes and clicks

Purchases in 2025 appear to be driven by high-intent users and a small set of strong products, rather than by broad marketing effectiveness. While the funnel became more stable, the absence of engagement limits growth potential.



## Conversion & Funnel Insights

Across all three years, the early funnel (homepage to product page) remains relatively healthy. Users show interest and browse products consistently.

The main breakdown occurs at checkout:
- Checkout retention dropped sharply in 2024
- Partial recovery in 2025, but still below 2023 levels

The problem isn’t traffic — it’s friction in the buying experience.

## Product-Level Behavior

Product conversion analysis shows a clear shift over time:
- 2023 had a balanced mix of converting products
- 2024 leaned toward seasonal and outdoor products
- 2025 became highly concentrated around a few high-performing SKUs

In 2025, products like Hockey Stick, Climbing Rope, and Surfboard carry a disproportionate share of conversions. While these products perform well, this concentration increases business risk and limits scalability.

Mid-priced products consistently show stronger conversion than both low and high price extremes, indicating a clear pricing sweet spot. However High priced products had better conversion rate comparatively.

## Engagement Trends (Root Cause)

Engagement metrics explain much of the conversion story:
- 2023 showed healthy interaction across views, likes, and clicks
- 2024 saw a steep drop, especially in likes and clicks
- 2025 engagement nearly flatlined

The decline in engagement happened faster than the decline in revenue. This indicates that marketing relevance and audience attention weakened before conversion stabilized. By 2025, engagement was no longer a reliable leading indicator.

In practical terms, IronPlay is currently selling **despite** marketing engagement, not because of it.


## 🛠Recommendations


### 1. Fix Checkout First — That’s Where Money Is Being Lost
Users are clearly interested in the products. They reach product pages and even start checkout, but many don’t finish. This drop appears in 2024 and doesn’t fully recover in 2025, which tells us this isn’t a one-off issue.

Before spending more on ads or traffic, IronPlay should focus on cleaning up the checkout experience. This includes reducing steps, making shipping and pricing clearer upfront, and ensuring the mobile checkout experience is smooth. Improving checkout completion is the fastest way to recover lost revenue because it works on users who already want to buy.


### 2. Stop Chasing Engagement Volume — Focus on Useful Signals
Engagement didn’t just decline; it collapsed faster than revenue. Likes and clicks fell sharply between 2023 and 2025, but sales didn’t fall at the same pace. This means engagement metrics are no longer good indicators of demand.

Instead of trying to revive engagement numbers across the board, IronPlay should use engagement as a warning signal. If content or campaigns don’t show early interaction, they should be paused quickly rather than refined endlessly. The goal should be relevance, not reach.


### 3. Use High-Selling Products as Entry Points, Not End Points
By 2025, conversion is driven by a small group of products. Items like **Fitness Tracker**, while not always the highest in conversion rate, show strong and consistent demand and volume. These products bring users in.

Rather than pushing these products alone, IronPlay should use them as entry points for bundles and combo offers. For example, pairing a Fitness Tracker with accessories or complementary fitness gear can increase order value while reducing dependency on single-item purchases.


### 4. Compare Progress Against 2023, Not Short-Term Improvements
The slight improvement in 2025 can easily be mistaken for recovery, but the business is still operating below its 2023 baseline. Treating stabilization as success risks ignoring unresolved issues.

Any future improvements should be measured against 2023 funnel performance, engagement quality, and product spread. Real recovery only happens when those levels are reached again — and then exceeded.

## Customer Feedback: Practical Fixes

Customer reviews suggest that people generally trust IronPlay’s products. When things go right, feedback around quality and packaging is strong. The problems start when execution breaks down. Complaints about late delivery, poor experience, service issues, and “not worth the money” point to operational gaps rather than product flaws.

These issues matter because they show up at the worst possible time — right when customers are deciding whether to complete a purchase or come back again.

### What to Fix, Practically

- **Be stricter with products that keep causing problems**  
  A small number of repeat issues can undo a lot of good work. Products that show up frequently in negative reviews should go through tighter quality checks before they’re shipped. Consistency matters more than perfection.

- **Choose a reliable delivery partner over the cheapest option**  
  Delivery complaints come up often enough to hurt trust. It’s better to work with fewer, more reliable delivery partners than to keep switching based on cost. Missing delivery expectations does more damage than shipping a day later with clear communication.

- **Train support staff to actually solve problems**  
  Fast replies don’t help if customers still feel stuck. Support teams should be able to issue refunds, replacements, or credits without unnecessary back-and-forth. Resolution builds trust; speed alone doesn’t.

- **Stop promoting products that aren’t ready**  
  If a product has ongoing delivery or performance issues, pushing more traffic to it only makes things worse. Fix the problem first, then scale it again.

- **Use strong products to help other products — but only after fixes**  
  Products like Fitness Tracker already have customer trust. They can help lift other items through bundles or combos, but only after basic quality and delivery issues are under control. Otherwise, bundling will be counter productive.
'''

