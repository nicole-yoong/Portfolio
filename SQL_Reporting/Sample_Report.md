# Sql Reporting #

## Summarizing Data in SQL ##

### Show the following information related to all items with OrderID = 10248: the product name, the unit price (taken from the OrderItems table), the quantity, and the name of the supplier's company (as SupplierName). ###

```sql
select p.productname, oi.unitprice, oi.quantity, s.companyname as SupplierName
from products p 
join orderitems oi on p.productid = oi.productid
join suppliers s on p.supplierid = s.supplierid
where oi.orderid = 10248
```
### Show the following information for each product: the product name, the company name of the product supplier (use the Suppliers table), the category name, the unit price, and the quantity per unit. ###
```sql
select p.productname, s.companyname, ca.categoryname, p.quantityperunit, p.unitprice
from products p 
join suppliers s on p.supplierid = s.supplierid
join categories ca on p.categoryid = ca.categoryid
```

### Count the number of employees hired in 2013. Name the result NumberOfEmployees. ###
```sql
select count(employeeid) as NumberOfEmployees 
from employees 
where hiredate >= '2013-01-01' and hiredate < '2013-12-31'
```

### Show each SupplierID alongside the CompanyName and the number of products they supply (as the ProductsCount column). Use the Products and Suppliers tables. ###
```sql
select s.supplierid, s.companyname, count(p.productid) as ProductsCount
from products p 
join suppliers s on p.supplierid = s.supplierid
group by s.supplierid, s.companyname
```

### The template code shows the query from the explanation. The Northwind store offers its customers discounts for some products. The discount for each item is stored in the Discount column of the OrderItem table. (For example, a 0.20 discount means that the customer pays 1 - 0.2 = 0.8 of the original price.) Your task is to add a second column named TotalPriceAfterDiscount. ###
```sql
select sum(oi.unitprice * oi.quantity) AS TotalPrice, 
sum(oi.unitprice*oi.quantity*(1-oi.discount)) as TotalPriceAfterDiscount
from orders o 
join orderitems oi on o.orderid = oi.orderid
where o.orderid = 10250;
```

### We want to know the number of orders processed by each employee. Show the following columns: EmployeeID, FirstName, LastName, and the number of orders processed as OrdersCount. ###
```sql
select e.employeeid, e.firstname, e.lastname, count(distinct o.orderid) as OrdersCount
from employees e 
join orders o on e.employeeid = o.employeeid
group by e.employeeid, e.firstname, e.lastname
```

### How much are the products in stock in each category worth? Show three columns: CategoryID, CategoryName, and CategoryTotalValue. You'll calculate the third column as the sum of unit prices multiplied by the number of units in stock for all products in the given category. ###
```sql
select ca.categoryid, ca.categoryname, sum(p.unitprice*p.unitsinstock) as CategoryTotalValue
from categories ca 
join products p on ca.categoryid = p.categoryid
group by ca.categoryid, ca.categoryname
```

### Count the number of orders placed by each customer. Show the CustomerID, CompanyName, and OrdersCount columns. ###
```sql
select cu.customerid, cu.companyname, count(distinct o.orderid) as OrdersCount
from customers cu 
join orders o on cu.customerid = o.customerid
group by cu.customerid, cu.companyname
```

### Which customers paid the most for orders made in June 2016 or July 2016? Show two columns: ###
### - CompanyName ###
### - TotalPaid, calculated as the total price (after discount) paid for all orders made by a given customer in June 2016 or July 2016. ###
### Sort the results by TotalPaid in descending order. ###
```sql
select cu.companyname, sum(oi.unitprice*oi.quantity*(1-oi.discount)) as TotalPaid
from customers cu 
join orders o on cu.customerid = o.customerid
join orderitems oi on o.orderid = oi.orderid
where o.orderdate >= '2016-06-01' and o.orderdate <= '2016-07-31'
group by cu.companyname
order by TotalPaid desc
```

### Count the number of customers with and without a fax number. Show two columns: AllCustomersCount and CustomersWithFaxCount. ###
```sql
select count(*) as AllCustomersCount, count(fax) as CustomersWithFaxCount
from customers 
```

### Find the total number of products provided by each supplier. Show the CompanyName and ProductsCount (the number of products supplied) columns. Include suppliers that haven't provided any products. ###
```sql
select s.companyname, count(P.productid) as ProductsCount
from suppliers s left 
join products p on s.supplierid = p.supplierid
group by s.companyname
```
### Show the number of unique companies (as NumberOfCompanies) that had orders shipped to Spain. ###
```sql
select count(distinct customerid) as numberofcompanies
from orders
where shipcountry = 'Spain'
```

### Find the total number of products supplied by each supplier. Show the following columns: SupplierID, CompanyName, and ProductsSuppliedCount (the number of products supplied by that company). ###
```sql
select s.supplierid, s.companyname, count(p.productid) as ProductsSuppliedCount
from suppliers s 
join products p on s.supplierid = p.supplierid
group by s.supplierid, s.companyname
```

### How many distinct products are there in all orders shipped to France? Name the result DistinctProducts. ###
```sql
select
count(distinct oi.productid) as distinctproducts
from orders o
join orderitems oi on o.orderid = oi.orderid
where shipcountry = 'France'
```

### Show three kinds of information about product suppliers: ### 
### - AllSuppliers (the total number of suppliers) ### 
### - SuppliersRegionAssigned (the total number of suppliers who are assigned to a region) ### 
### - UniqueSupplierRegions (the number of unique regions suppliers are assigned to) ###
```sql
select count(s.supplierid) as AllSuppliers,
count(region) as SuppliersRegionAssigned,
count(distinct region) as UniqueSupplierRegions
from suppliers s
```

### Which employees processed the highest -value orders made during June and July 2016? ###
### For each employee, compute the total order value before discount from all orders processed by this employee between 5 July 2016 and 31 July 2016. Ignore employees without any orders processed. Show the following columns: FirstName, LastName, and SumOrders. Sort the results by SumOrders in descending order. ###
```sql
select e.firstname, e.lastname, sum(oi.unitprice * quantity) as Sumorders
from employees e 
join orders o on e.employeeid = o.employeeid
join orderitems oi on o.orderid = oi.orderid
where o.orderdate >= '2016-07-05' and o.orderdate <= '2016-07-31'
group by e.employeeid, e.firstname, e.lastname
order by Sumorders desc 
```
## Classifying Data with CASE WHEN and GROUP BY ##

### We want to create a report measuring the level of experience each Northwind employee has with the company. Show the FirstName, LastName, HireDate, and Experience columns for each employee. The Experience column should display the following values: ###
### N'junior' for employees hired after January, 1st 2014. ###
### N'middle' for employees hired after January, 1st 2013 but before January, 1st 2014. ###
### N'senior' for employees hired on or before January, 1st 2013. ###
```sql
select e.firstname, e.lastname, e.hiredate, 
case 
	when hiredate > '2014-01-01' then N'junior'
	when hiredate > '2013-01-01' and hiredate < '2014-01-01' then N'middle'
	when hiredate <= '2013-01-01' then N'senior'
end as experience
from employees e

```
### We want to show the following basic customer information (the Customers table): ###
### 1. CustomerID ###
### 2. CompanyName ###
### 3. Country ###
### 4. Language ###

### The value of the Language column will be decided by the following rules: ###
### - N'German' for companies from Germany, Switzerland, and Austria. ###
### - N'English' for companies from the UK, Canada, the USA, and Ireland. ###
### - N'Other' for all other countries. ###
```sql
select customerid, companyname, country, 
case
  when country in ('Germany', 'Switzerland', 'Austria') then N'German'
  when country in ('UK', 'Canada', 'USA','Ireland') then N'English'
  else N'Other'
end as language
from customers 
```

### Let's create a report that will divide all products into vegetarian and non-vegetarian categories. For each product, show the following columns: ###
### 1. ProductName ###
### 2. CategoryName ###
### 3. DietType: ###
### - N'Non-vegetarian' for products from the categories N'Meat/Poultry' and N'Seafood'. ###
### - N'Vegetarian' for any other category. ###
```sql
select p.productname, ca.categoryname,
case
  when ca.categoryname in (N'Meat/Poultry', N'Seafood') then N'Non-vegetarian'
  else N'Vegetarian'
end as diettype
from products p 
join categories ca on p.categoryid = ca.categoryid
```

### Create a report that shows the number of products supplied from a specific continent. Display two columns: SupplierContinent and ProductCount. The SupplierContinent column should have the following values: ###
### - N'North America' for products supplied from N'USA' and N'Canada'. ###
### - N'Asia' for products from N'Japan' and N'Singapore'. ###
### - N'Other' for other countries. ###
```sql
select count(p.productid) as ProductCount,
case
  when s.country in (N'USA' , N'Canada') then N'North America'
  when s.country in (N'Japan' , N'Singapore') then N'Asia'
  else N'Other'
end as SupplierContinent
from products p 
join suppliers s on p.supplierid = s.supplierid
group by 
case
  when s.country in (N'USA' , N'Canada') then N'North America'
  when s.country in (N'Japan' , N'Singapore') then N'Asia'
  else N'Other'
end
```

### We want to create a simple report that will show the number of young and old employees at Northwind. Show two columns: Age and EmployeeCount. ###
### The Age column has the following values: ###
### N'young' for people born after 1 Jan 1980. ###
### N'old' for all other employees. ###
```sql
select
case
  when birthdate > '1980-01-01' then N'young'
  else 'old'
end as age,
count(employeeid) as EmployeeCount
from employees
group by 
case
  when birthdate > '1980-01-01' then N'young'
  else 'old'
end
```

### How many customers are represented by owners (ContactTitle = N'Owner'), and how many aren't? Show two columns with appropriate values: RepresentedByOwner and NotRepresentedByOwner. ###
```sql
select 
count(case when contacttitle = N'Owner' then customerid end) as RepresentedByOwner,
count (case when contacttitle != N'Owner' then customerid end) as NotRepresentedByOwner
from customers
```

### Washington (WA) is Northwind's primary region. How many orders have been processed by employees in the WA region, and how many by employees in other regions? Show two columns with their respective counts: OrdersWAEmployees and OrdersNotWAEmployees. ###
```sql
select
count(case when region = N'WA' then orderID end) as OrdersWAEmployees,
count(case when region != N'WA' then orderID end) as OrdersNotWAEmployees
from employees e join orders o on
e.employeeid = o.employeeid
```
### We need a report that will show the number of products with high and low availability in all product categories. Show three columns: CategoryName, HighAvailability (count the products with more than 30 units in stock) and LowAvailability (count the products with 30 or fewer units in stock). ###
```sql
select categoryname, 
count(case when unitsinstock > 30 then productid end) as n'HighAvailability',
count(case when unitsinstock <= 30 then productid end) as n'LowAvailability'
from categories c join products p on
c.categoryid = p.categoryid
group by c.categoryname
```

### There have been a lot of orders shipped to France. Of these, how many order items were sold at full price and how many were discounted? Show two columns with the respective counts: FullPrice and DiscountedPrice. ###
```sql
select
sum (case when discount = 0.0 then 1 end) as FullPrice,
sum (case when discount != 0.0 then 1 end) as DiscountedPrice
from orderitems oi 
join orders o on oi.orderid = o.orderid
where shipcountry = 'France'
```

### This time, we want a report that will show each supplier alongside their number of units in stock and their number of expensive units in stock. Show four columns: SupplierID, CompanyName, AllUnits (all units in stock supplied by that supplier), and ExpensiveUnits (units in stock with a unit price over 40.0, supplied by that supplier). ###
```sql
select s.supplierid, s.companyname, sum(p.unitsinstock) as allunits,
sum(case when unitprice > 40.0 then UnitsInStock else 0 end) as ExpensiveUnits
from suppliers s
join products p on s.supplierid = p.supplierid
group by s.supplierid, s.companyname
```

### For each product, show the following columns: ProductID, ProductName, UnitPrice, and PriceLevel. The PriceLevel column should show one of the following values: ###
### - N'expensive' for products with a unit price above 100. ###
### - N'average' for products with a unit price above 40 but no more than 100. ###
### - N'cheap' for other products. ###
```sql
select productid, productname, unitprice, 
case
	when unitprice > 100 then N'expensive'
	when unitprice > 40 and unitprice <= 100 then N'average'
	else N'cheap'
end as pricelevel
from products
```

### We would like to categorize all orders based on their total price (before any discount). For each order, show the following columns: ###
### 1. OrderID ###
### 2. TotalPrice (calculated before discount) ###
### 3. PriceGroup, which should have the following values: ###
### - N'high' for a total price over $2,000. ###
### - N'average' for a total price between $600 and $2,000, both inclusive. ###
### - N'low' for a total price under $600. ###
```sql
select o.orderid, sum(oi.unitprice*oi.quantity) as totalprice,
case 
	when sum(oi.unitprice*oi.quantity) > 2000 then N'high'
	when sum(oi.unitprice*oi.quantity) >= 600 and sum(oi.unitprice*oi.quantity) <= 2000 then N'average'
	else N'low'
end as pricegroup
from orders o 
join orderitems oi on o.orderid = oi.orderid
group by o.orderid
```
### Group all orders based on the Freight column. Show three columns in your report: ###
### LowFreight – the number of orders where the Freight value is less than 40.0. ###
### AvgFreight – the number of orders where the Freight value is greater than equal to or 40.0 but less than 80.0. ###
### HighFreight – the number of orders where the Freight value is greater than equal to or 80.0. ###
```sql
select 
sum (case when o.freight < 40 then 1 end) as LowFreight,
sum (case when o.freight >= 40 and o.freight < 80 then 1 end) as AvgFreight,
sum (case when o.freight >= 80 then 1 end) as HighFreight
from orders o
```
## Multi-level Aggregation ##

### What's the average number of products in each category? Show a single value in a column named AvgProductCount. ###
### In the inner query, calculate the number of products for each category ID. In the outer query, find the average product count. ###
```sql
with TotalProduct_cte as
(
  select categoryid, count(productid) as TotalProduct
  from products
  group by categoryid
)
select avg(TotalProduct) as AvgProductCount
from TotalProduct_cte
```
### For each employee from the Washington (WA) region, show the average value for all orders they placed. Show the following columns: EmployeeID, FirstName, LastName, and AvgTotalPrice (calculated as the average total order price, before discount). ###
### In the inner query, calculate the value of each order and select it alongside the ID of the employee who processed it. In the outer query, join the CTE with the Employees table to show all the required information and filter the employees by region. ###
```sql
with TotalValue_cte as
(
  select o.employeeid, oi.orderid, sum(oi.unitprice * oi.quantity) as TotalValue
  from orders o
  join orderitems oi on o.orderid = oi.orderid
  group by oi.orderid, o.employeeid
)
select e.employeeid, e.firstname, e.lastname, avg(TotalValue) as AvgTotalPrice
from TotalValue_cte tvc 
join employees e on tvc.employeeid = e.employeeid
where e.region = N'WA'
group by e.employeeid, e.firstname, e.lastname, e.region
```

### For each shipping country, we want to find the average count of unique products in each order. Show the ShipCountry and AvgDistinctItemCount columns. Sort the results by count, in descending order. ###
### In the inner query, find the number of distinct products in each order and select it alongside the ShipCountry column. In the outer query, apply the proper aggregation. ###
```sql
with TotalProduct_cte as 
(
  select oi.orderid, count(distinct oi.productid) as TotalProduct, o.shipcountry
  from orders o
  join orderitems oi on o.orderid = oi.orderid
  group by oi.orderid, o.shipcountry
)
select avg(TotalProduct) as AvgDistinctItemCount, shipcountry
from TotalProduct_cte
group by shipcountry
order by AvgDistinctItemCount desc
```

###  ###
```sql

```

###  ###
```sql

```

###  ###
```sql

```

###  ###
```sql

```

###  ###
```sql

```

###  ###
```sql

```

###  ###
```sql

```

###  ###
```sql

```

###  ###
```sql

```
