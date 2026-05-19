-- Total Revenue
SELECT 
    ROUND(SUM(Quantity * UnitPrice),2) AS Total_Revenue
FROM OnlineRetail;

-- Total Orders
SELECT 
    COUNT(DISTINCT InvoiceNo) AS Total_Orders
FROM OnlineRetail;

-- Total Customers
SELECT 
    COUNT(DISTINCT CustomerID) AS Total_Customers
FROM OnlineRetail;

-- Average Order Value
SELECT 
    ROUND(SUM(Quantity * UnitPrice) / COUNT(DISTINCT InvoiceNo),2) AS Avg_Order_Value
FROM OnlineRetail;

-- Top 10 Customers by Revenue
SELECT 
    CustomerID,
    ROUND(SUM(Quantity * UnitPrice),2) AS Revenue
FROM OnlineRetail
GROUP BY CustomerID
ORDER BY Revenue DESC
LIMIT 10;

-- Top 10 Products by Revenue
SELECT 
    Description,
    ROUND(SUM(Quantity * UnitPrice),2) AS Revenue
FROM OnlineRetail
GROUP BY Description
ORDER BY Revenue DESC
LIMIT 10;

-- Revenue by Country
SELECT 
    Country,
    ROUND(SUM(Quantity * UnitPrice),2) AS Revenue
FROM OnlineRetail
GROUP BY Country
ORDER BY Revenue DESC;

-- Monthly Sales Trend
SELECT 
    EXTRACT(MONTH FROM InvoiceDate) AS Month,
    ROUND(SUM(Quantity * UnitPrice),2) AS Revenue
FROM OnlineRetail
GROUP BY Month
ORDER BY Month;

-- Top 5 Countries by Orders
SELECT 
    Country,
    COUNT(DISTINCT InvoiceNo) AS Total_Orders
FROM OnlineRetail
GROUP BY Country
ORDER BY Total_Orders DESC
LIMIT 5;

-- Most Frequently Purchased Products
SELECT 
    Description,
    SUM(Quantity) AS Total_Quantity_Sold
FROM OnlineRetail
GROUP BY Description
ORDER BY Total_Quantity_Sold DESC
LIMIT 10;

-- Customers with Highest Purchase Frequency
SELECT 
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS Purchase_Frequency
FROM OnlineRetail
GROUP BY CustomerID
ORDER BY Purchase_Frequency DESC
LIMIT 10;

-- Repeat Customers
SELECT 
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS Total_Orders
FROM OnlineRetail
GROUP BY CustomerID
HAVING COUNT(DISTINCT InvoiceNo) > 5
ORDER BY Total_Orders DESC;

-- Revenue by Month and Country
SELECT 
    Country,
    EXTRACT(MONTH FROM InvoiceDate) AS Month,
    ROUND(SUM(Quantity * UnitPrice),2) AS Revenue
FROM OnlineRetail
GROUP BY Country, Month
ORDER BY Revenue DESC;

-- Top Revenue Generating Days
SELECT 
    EXTRACT(DAY FROM InvoiceDate) AS Day,
    ROUND(SUM(Quantity * UnitPrice),2) AS Revenue
FROM OnlineRetail
GROUP BY Day
ORDER BY Revenue DESC;

-- Customer Segmentation by Revenue
SELECT
    CustomerID,
    ROUND(SUM(Quantity * UnitPrice),2) AS Total_Spent,
    CASE
        WHEN SUM(Quantity * UnitPrice) > 10000 THEN 'High Value'
        WHEN SUM(Quantity * UnitPrice) BETWEEN 5000 AND 10000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS Customer_Segment
FROM OnlineRetail
GROUP BY CustomerID
ORDER BY Total_Spent DESC;
