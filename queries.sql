-- queries.sql

-- FILTERED_DATA_CUSTOMER_DESCRIPTION
select * from onlineretail
where CustomerID is not null and Description is not null;

-- FILTERED_DATA_QUANTITY_POSITIVE
select * from onlineretail
where Quantity>0;

-- TOP_10_MOST_PURCHASED_PRODUCTS
select Description, sum(Quantity) as TotalSold
from onlineretail
group by Description
order by TotalSold desc
limit 10;

-- TOP_CUSTOMERS_BY_PURCHASE_VOLUME
select CustomerID, sum(Quantity) as TotalUnits
from onlineretail
group by CustomerID
order by TotalUnits desc
limit 10;

-- TOTAL_REVENUE_PER_PRODUCT
select Description, sum(Quantity * UnitPrice) as Revenue
from onlineretail
group by Description
order by Revenue desc
limit 10;

-- FREQUENTLY_BOUGHT_TOGETHER_BASIC
select A.Description as ProductA, B.description as ProductB, count(*) as Frequency
from onlineretail A
join onlineretail B
on A.InvoiceNo = B.InvoiceNo
and A.StockCode <> B.StockCode
group by A.Description, B.Description
order by Frequency desc
limit 20;

-- CREATE_FREQUENTLY_BOUGHT_TOGETHER_VIEW
CREATE VIEW FrequentlyBoughtTogether AS
select A.Description as ProductA, B.Description as ProductB , count(*) as Frequency
from onlineretail A
join onlineretail B
on A.InvoiceNo =B.InvoiceNo
and A.StockCode <> B.StockCode
group by A.Description, B.Description
having count(*) > 50
order by Frequency desc;

-- GET_FREQUENTLY_BOUGHT_TOGETHER_FOR_PRODUCT
select * from FrequentlyBoughtTogether
where ProductA= '{product_description}';

-- GET_PRODUCT_RECOMMENDATIONS_FOR_CUSTOMER
select f.ProductB as RecommendedProduct, sum(f.Frequency) as Strength
from (
select distinct Description
from onlineretail
where CustomerID={customer_id}
) as c
join FrequentlyBoughtTogether f
on c.Description = f.ProductA
group by f.ProductB
order by Strength desc
limit 5;

-- GET_ALL_PRODUCT_DESCRIPTIONS
SELECT DISTINCT Description FROM onlineretail ORDER BY Description;

-- GET_ALL_CUSTOMER_IDS
SELECT DISTINCT CustomerID FROM onlineretail ORDER BY CustomerID;