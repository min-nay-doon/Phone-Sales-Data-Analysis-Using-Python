# Phone Sales Data Analysis Project
## Overview
This project analyzes phone sales data by cleaining raw datasets and extracting meaningful insights through visualization. The analysis focuses on identifying best-selling products, high rated models, pricing trends, and potential stock issues using Python-based data processing and visualization.
## Oblectives
- Analyze the relationship between product price and sales volume
- Identify top-selling and best-reviewed phone models
- Detect low-stock products to highlight inventory risks
- Discover popular products vased on combined demand and ratings
## Tools & Libraries
- Python
- Pandas
- Matplotlib
- Numpy
- Re
## Dataset
- Source: phone search dataset
## Data Cleaning & Preparation
- Remove missing values from key columns
- Trimm and replace messy data
- Convert price and availability into numeric format
- Extract brand and model from product titles
## Feature Enginnering
- Create `sales_volume_numeric`
- Build `weighted_rating` using ratings and review counts
- Develop `popularity_score` to identity trending products
## Data Visualizations
- Price vs Sales trend
- Top 10 Best Selling Models
- Top 10 Best Reviewed Models
- Low Stock Products (<=10 units)
- Most Popular Phones
## Key Insights
- Lower-priced phones generate higher sales volume, indicating strong demand for budget-friendly devices
- A small number of models dominate total sales, highlighting key revenue drivers
- High ratings do not always translate into high sales, suggesting the need for better marketing
- Several products are at critically low stock levels, risking potential revenue loss
- Popular models combine strong sales and high customer satisfaction
## Conclusion
The analysis reveals key patterns in customer preferences, pricing dynamics, and product performance. It highlights opportunities for optimizing pricing strategies, and identifying high-potential products.
## Files Included
- Python script (.py)
- phone search.csv
- Visualization screenshots
## Future Improvements
- Add interactive dashboards using Power BI
- Perform time-series analysis on sales trends
- Apply clustering for product segmentation
- Build predictive models for demand forecasting
