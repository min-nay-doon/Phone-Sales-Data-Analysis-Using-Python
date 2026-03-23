## Phone Sales Data Analysis Project
#### Overview
This project analyzes phone sales data by cleaining raw datasets and extracting meaningful insights through visualization. The goal is to identify trends, best-selling models and inventory risks.
#### Data Cleaning
- Remove missing values from key columns
- Trimm and replace messy data
- Convert price and availability into numeric format
-  Extract brand and model from product titles
#### Engineering feature
- Create `sales_volume_numeric`
- Build `weighted_rating` using ratings and review counts
- Develop `popularity_score` to identity trending products
#### Data Visualizations
- Price vs Sales trend
- Top 10 Best Selling Models
- Top 10 Best Reviewed Models
- Low Stock Products (<=10 units)
- Most Popular Phones
#### Tools Used
Python (Pandas, Numpy, Matplotlib, Regex)
#### Key Insights
- Lower-priced phones generate higher sales volume, indicating strong demand for budget-friendly devices
- A small number of models dominate total sales, highlighting key revenue drivers
- High ratings do not always translate into high sales, suggesting the need for better marketing
- Several products are at critically low stock levels, risking potential revenue loss
- Popular models combine strong sales and high customer satisfaction
