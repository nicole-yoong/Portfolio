## NORTHWIND DATABASE ##

The Northwind database is a sample database used by Microsoft to demonstrate the features of some of its products, including SQL Server and Microsoft Access. The database contains the sales data for Northwind Traders, a fictitious specialty foods exportimport company.

## EMPLOYEE ANALYSIS ##

### Number of employees hired each year ###
```sql
select datepart(year, hiredate) as Year, count(*) as Count from employees
group by datepart(year, hiredate)
```
![image](https://user-images.githubusercontent.com/77920592/196151570-52eaf4a3-4e50-4f01-9230-87b25962adf6.png)

### Average age of the employees ###

```sql
select avg(datediff(year, birthdate, getdate())) from employees;
```
![image](https://user-images.githubusercontent.com/77920592/196151642-94360555-eba1-4356-9fe1-3bfc11f54a6c.png)

### Number of employees in different positions ###

```sql
select title, count(*) as Count from employees
group by title;
```
![image](https://user-images.githubusercontent.com/77920592/196151765-448a4d54-1466-4b92-851a-a2db924731e3.png)

### Number of orders processed by each employee ###

```sql
select e.employeeid, e.firstname, e.lastname, count(distinct o.orderid) as OrdersCount
from employees e 
join orders o on e.employeeid = o.employeeid
group by e.employeeid, e.firstname, e.lastname
order by count(distinct o.orderid) desc
```
![image](https://user-images.githubusercontent.com/77920592/196152118-697470b3-f6a9-4a95-a703-ccad7433a147.png)

### Order values processed by each employee ###

```sql
select e.firstname, e.lastname, sum(od.unitprice * quantity) as Sumorders
from employees e 
join orders o on e.employeeid = o.employeeid
join [order details] od on o.orderid = od.orderid
group by e.employeeid, e.firstname, e.lastname
order by sum(od.unitprice * quantity) desc 
```
![image](https://user-images.githubusercontent.com/77920592/196152205-437fbdc4-24e3-4335-91a6-9e1e0cfc3670.png)

### Order values processed by each employee on an annual basis ###

```sql
select datepart(year, orderdate) as Year, e.firstname, e.lastname, sum(od.unitprice * quantity) as Sumorders
from employees e 
join orders o on e.employeeid = o.employeeid
join [order details] od on o.orderid = od.orderid
group by e.employeeid, e.firstname, e.lastname, datepart(year, orderdate)
order by datepart(year, orderdate), sum(od.unitprice * quantity) desc 
```
![image](https://user-images.githubusercontent.com/77920592/196154764-1281fa64-18f7-4421-adde-77c314ca9fc8.png)
![image](https://user-images.githubusercontent.com/77920592/196154862-3a74812c-9aaa-4652-95b3-f53e46371ae6.png)

Northwind hires an average of 3 employees each year and the age of all employees are relatively high, with an average of 66 years old. 
2/3 of its employees are sales representatives, who are the key personnels pushing the business. 

Margaret Peacock is the top performing employees processesing the highest number of order counts with the greatest value, followed by Janet Leverling and Nancy Davolio.
However, when comparing their performances on an annual basis, Janet Leverling overtook Margaret Peacock and became the top performing employees in terms of revenue generation.

## COMPANY PERFORMANCE ANALYSIS ##

### Revenues on an annual basis ###


## CUSTOMER ANALYSIS ##

### Percentage of customers in different country ###

```sql
with cte as 
(
select country, count(*) as Count from customers
group by country
)
select country, Count, round((count * 100.0/(select count(*) from customers)),3) as Percentage
from cte
group by country, count
order by round((count * 100.0/(select count(*) from customers)),3) desc
```
![image](https://user-images.githubusercontent.com/77920592/196159443-d17dd56c-8476-4328-806d-631108f02374.png)

### Country that contributes to the most revenues ###

```sql
with cte as
(
select cu.country, sum(od.unitprice*quantity) as TotalValue
from customers cu join orders o on o.customerid = cu.customerid
join [Order Details] od on o.orderid = od.orderid
group by cu.country
)
select country, TotalValue, round((TotalValue * 100.0/(select sum(unitprice*quantity) from [order details])),3) as Percentage
from cte
group by country, TotalValue
order by round((TotalValue * 100.0/(select sum(unitprice*quantity) from [order details])),3) desc
```
![image](https://user-images.githubusercontent.com/77920592/196160456-a01335c9-b21b-4d2f-8a09-9416a2827875.png)

### 25th, 50th and 75th percentile values for the revenue (unitprice * quantity) per transaction ###

```sql
select distinct percentile_cont(0.25) within group(order by (unitprice*quantity)) over() as [25th_percentile]
from [order details];
select distinct percentile_cont(0.50) within group(order by (unitprice*quantity)) over() as [50th_percentile]
from [order details];
select distinct percentile_cont(0.75) within group(order by (unitprice*quantity)) over() as [75th_percentile]
from [order details];
```
![image](https://user-images.githubusercontent.com/77920592/196162697-2e93048a-966d-4769-9a9c-ee34d8010b32.png)

### Find the average discount value per transaction ###

```sql
select round(avg(discount) * 100.0, 2) as AvgDiscount 
from [order details]
```
![image](https://user-images.githubusercontent.com/77920592/196165521-b2a83b62-93bb-4e8b-9055-f3e458c3c42e.png)


### Number of orders placed by each customer ###

```sql
select cu.customerid, cu.companyname, count(distinct o.orderid) as OrdersCount
from customers cu 
join orders o on cu.customerid = o.customerid
group by cu.customerid, cu.companyname
order by count(distinct o.orderid) desc
```
![image](https://user-images.githubusercontent.com/77920592/196155606-08c11912-a24b-4482-8dc0-86462ad1fd9d.png)

### Total revenues generated by each customer ###

```sql
select cu.customerid, cu.companyname, sum(od.unitprice*quantity) as TotalValue
from customers cu join orders o on o.customerid = cu.customerid
join [Order Details] od on o.orderid = od.orderid
group by cu.customerid, cu.companyname
order by sum(od.unitprice*quantity) desc
```
![image](https://user-images.githubusercontent.com/77920592/196155661-2bf764d2-223d-4e61-90a4-b8b724302b66.png)

### Customers in different tiers based on the order values: i) 10k and below = Bronze, ii) 10k - 50k = Silver, iii) 50k - 100k = Gold, iv) 100k and above = Platinum ###
```sql
with cte as
(
select cu.customerid, cu.companyname, sum(od.unitprice*quantity) as TotalValue,
case
when sum(od.unitprice*quantity) < 10000 then 'Bronze'
when sum(od.unitprice*quantity) >= 10000 and sum(od.unitprice*quantity) < 50000 then 'Silver'
when sum(od.unitprice*quantity) >= 50000 and sum(od.unitprice*quantity) < 100000 then 'Gold'
when sum(od.unitprice*quantity) >= 100000 then 'Platinum'
end MemberTier 
from customers cu join orders o on o.customerid = cu.customerid
join [Order Details] od on o.orderid = od.orderid
group by cu.customerid, cu.companyname
)
select count(*) as Count, round(count(*) * 100.0 / (select count(*) from customers), 3) as Percentage, MemberTier
from cte 
group by MemberTier
order by Count desc
```
![image](https://user-images.githubusercontent.com/77920592/196161733-4ff45b05-eed6-4fb2-b8b7-f682eb79dc5f.png)

Customers in USA purchase the most frequent from Northwind, and it is followed by France and Germany. 
In terms of the order values, customers in USA contribute the most as expected. 
Despite customers in France placed quite a number of orders but Germany, Austria, and Brazil overtook France in terms of the order values. 

Looking at the percentile of order values, 25% of the order values lie below $154, 25% of the order values lie above $722.5, and the median order values is $360. 
In the meantime, some orders are given a discount and the average percentage of discount is 5.62%.

Based on the member tiers developed in accordance to the total order values, only less than 6% of customers have exceeded a value of 50k, while the order values of majority of the customers are below 50k. 

## PRODUCTS ANALYSIS ##

### Find the total quantity, revenue for each category ###

```sql
select c.categoryid, c.categoryname, sum(od.quantity) as Quantity, sum(od.unitprice*quantity) as Revenue
from [order details] od join products p on od.productid = p.productid 
join categories c on p.categoryid = c.categoryid
group by c.categoryid, c.categoryname
order by sum(od.unitprice*quantity) desc
```
![image](https://user-images.githubusercontent.com/77920592/196166947-e980ef4d-ea4c-4933-8a9b-bc2fa045d4e9.png)

### Find the percentage split of total revenue by category ###

```sql
with cte as
(
select c.categoryname, sum(od.unitprice*quantity) as TotalRevenue
from [order details] od join products p on od.productid = p.productid 
join categories c on p.categoryid = c.categoryid
group by c.categoryname
)
select categoryname, round((TotalRevenue * 100.0) / sum(TotalRevenue) over(),3) as Percentage
from cte
order by (TotalRevenue * 100.0) / sum(TotalRevenue) over() desc
```
![image](https://user-images.githubusercontent.com/77920592/196167328-cb7638b6-818d-4558-829b-12f31213038a.png)

### Find how much are the products in stock in each category worth ###

```sql
select c.categoryid, c.categoryname, sum(p.unitprice*p.unitsinstock) as CategoryTotalValue
from categories c
join products p on c.categoryid = p.categoryid
group by c.categoryid, c.categoryname
order by sum(p.unitprice*p.unitsinstock) desc
```
![image](https://user-images.githubusercontent.com/77920592/196168653-d742a646-4df0-4c9f-9324-b4f80ed9dd52.png)

### Average product prices of each category ###
```sql
select c.categoryid, c.categoryname, round(sum(p.unitprice)/count(p.productid),3) as AvgProductValue
from categories c
join products p on c.categoryid = p.categoryid
group by c.categoryid, c.categoryname
order by round(sum(p.unitprice)/count(p.productid),3) desc
```
![image](https://user-images.githubusercontent.com/77920592/196170569-14104e9d-93b7-409c-a9b0-de5ad276d108.png)


### Find the top selling product(most quantity) for each category ###

```sql
with cte as
(
select c.categoryname, p.productname, sum(od.quantity) as TotalQuantity,
rank() over(partition by c.categoryname order by sum(od.quantity) desc) as Rank
from [order details] od join products p on od.productid = p.productid 
join categories c on p.categoryid = c.categoryid
group by c.categoryname, p.productname
)
select categoryname, productname, totalquantity
from cte
where rank = 1;
```
![image](https://user-images.githubusercontent.com/77920592/196165865-348a6f14-1d45-49f3-bc91-c3093ab44362.png)

### Find the top 3 products by total revenue before discount ###

```sql
with cte as
(
select od.productid, productname, sum(od.unitprice*quantity) as Revenue,
rank() over(order by sum(od.unitprice*quantity) desc) as Rank
from [order details] od join products p on od.productid = p.productid
group by od.productid, productname
)
select productid, productname, revenue from cte
where Rank in (1,2,3)
```
![image](https://user-images.githubusercontent.com/77920592/196165952-39a57e4f-1476-467c-93ff-3649f13c30cd.png)

Beverages contributes to the greatest amount of revenues, which is 21% of the total revenues, with 9532 units being sold throughout the business. It is then followed by dairy products, and meat/poultry. 
Grains/cereals are the least sold products, probably because of the nature of the products where it is not consumed by many people, or the quality or price is not satisfactory compared to other companies. 

Looking at the total values of those in-stock products, seafood category tops the chart with a value of $13010.35, followed by beverages and condiments categories. 
However, a further examination into the average price for each product in each category reveals that meats/poultry are the most expensive, with an average price of $57.

## SUPPLIER

### Find the total number of products provided by each supplier ###

```sql
select s.companyname, count(P.productid) as ProductsCount
from suppliers s left 
join products p on s.supplierid = p.supplierid
group by s.companyname
```

## FREIGHT COST

### Group all orders based on the Freight column ###

```sql
select 
sum (case when o.freight < 40 then 1 end) as LowFreight,
sum (case when o.freight >= 40 and o.freight < 80 then 1 end) as AvgFreight,
sum (case when o.freight >= 80 then 1 end) as HighFreight
from orders o
```
