# Case Study #7 - Balanced Tree Clothing Co. #

![image](https://user-images.githubusercontent.com/77920592/199336620-547c4ca5-95f3-4f0c-a784-49ec138fa24f.png)

# Introduction #

Balanced Tree Clothing Company prides themselves on providing an optimised range of clothing and lifestyle wear for the modern adventurer!

Danny, the CEO of this trendy fashion company has asked you to assist the team’s merchandising teams analyse their sales performance and generate a basic financial report to share with the wider business.

# Case Study Questions #

The following questions can be considered key business questions and metrics that the Balanced Tree team requires for their monthly reports.

Each question can be answered using a single query - but as you are writing the SQL to solve each individual problem, keep in mind how you would generate all of these metrics in a single SQL script which the Balanced Tree team can run each month.

## High Level Sales Analysis ##

### What was the total quantity sold for all products? ###
```sql
select product_name, sum(qty) as TotalSales from sales s
join product_details pd on s.prod_id = pd.product_id
group by product_name
order by sum(qty) desc
```
![image](https://user-images.githubusercontent.com/77920592/198996317-a8a82229-16c1-46aa-a8d2-4c7fa6f703a8.png)

### What is the total generated revenue for all products before discounts? ###
```sql
select product_name, sum(qty*s.price) as TotalRevenues from sales s
join product_details pd on s.prod_id = pd.product_id
group by product_name
```
![image](https://user-images.githubusercontent.com/77920592/198996378-38329310-59d9-4aa7-be5e-576f0c944425.png)

### What was the total discount amount for all products? ###
```sql
select product_name, sum(qty*discount) as TotalDiscount from sales s
join product_details pd on s.prod_id = pd.product_id
group by product_name
```
![image](https://user-images.githubusercontent.com/77920592/198996433-0b0a085c-32c4-4203-925d-dbcb97ff9015.png)

## Transaction Analysis ##
### How many unique transactions were there? ###
```sql
select count(distinct txn_id) as UniqueTrans from sales
```
![image](https://user-images.githubusercontent.com/77920592/198996486-ae2370b6-724b-4ee7-addb-dcc5264e742d.png)

### What is the average unique products purchased in each transaction? ###
```sql
with cte as(
select count(distinct prod_id) as UniqueProd from sales
group by txn_id)
select avg(UniqueProd) as AvgUniqueProd from cte
```
![image](https://user-images.githubusercontent.com/77920592/198996533-9c861b10-e7fd-4b55-9353-b603361fd80c.png)

### What are the 25th, 50th and 75th percentile values for the revenue per transaction? ###
```sql
select distinct
percentile_cont(0.25) within group(order by qty*price) over () as perc_25,
percentile_cont(0.50) within group(order by qty*price) over () as perc_50,
percentile_cont(0.75) within group(order by qty*price) over () as perc_75
from sales
```
![image](https://user-images.githubusercontent.com/77920592/198996620-e4e0aa73-ff5b-4f4c-b409-6d68ac202538.png)

### What is the average discount value per transaction? ###
```sql
select distinct avg(discount) over() AvgDiscount from sales
```
![image](https://user-images.githubusercontent.com/77920592/198996650-8e35d43d-2dc1-4873-8725-966c06c35a69.png)

### What is the percentage split of all transactions for members vs non-members? ###
```sql
select 
sum(case when member = 't' then 1 else 0 end) * 100.0 / 
	(select count(*) from sales) as members, 
sum(case when member = 'f' then 1 else 0 end) * 100.0 / 
	(select count(*) from sales) as non_members 
from sales
```
![image](https://user-images.githubusercontent.com/77920592/198996697-4c03ecc0-6c70-417d-a433-9e60b706de98.png)

### What is the average revenue for member transactions and non-member transactions? ###
```sql
select
avg(case when member = 't' then qty*price end) as Member_Trans,
avg(case when member = 'f' then qty*price end) as Non_Member_Trans
from sales
```
![image](https://user-images.githubusercontent.com/77920592/198996755-9c1d82bd-4bb4-47e4-b60d-2504bb8abaec.png)

## Product Analysis ##

### What are the top 3 products by total revenue before discount? ###
```sql
select distinct product_name, sum(qty*s.price) as TotalRevenue
from sales s
join product_details pd on s.prod_id = pd.product_id
group by product_name
order by sum(qty*s.price) desc
```
![image](https://user-images.githubusercontent.com/77920592/198996827-039cff3f-1e1f-4a6f-a14c-ea82505ce500.png)

### What is the total quantity, revenue and discount for each segment? ###
```sql
select segment_name, sum(qty) as TotalQuantity, sum(qty*s.price) as TotalRevenue,
sum(discount) as TotalDiscount
from sales s
join product_details pd on s.prod_id = pd.product_id
group by segment_name
```
![image](https://user-images.githubusercontent.com/77920592/198996901-d063f351-f20a-429b-b21e-83a8ae053d55.png)

### What is the top selling product for each segment? ###
```sql
with cte as
(
select segment_name, product_name, sum(qty) as TotalQuantity,
rank() over(partition by segment_name order by sum(qty) desc) as rank
from sales s
join product_details pd on s.prod_id = pd.product_id
group by segment_name, product_name
)
select * from cte
where rank = 1
```
![image](https://user-images.githubusercontent.com/77920592/198996951-be4e857f-3edd-4160-a9d3-ca8154579a83.png)

### What is the total quantity, revenue and discount for each category? ###
```sql
select category_name, sum(qty) as TotalQuantity, sum(qty*s.price) as TotalRevenue,
sum(discount) as TotalDiscount
from sales s
join product_details pd on s.prod_id = pd.product_id
group by category_name
```
![image](https://user-images.githubusercontent.com/77920592/198997003-69674f55-13f8-44b9-b95f-ab3e49c8db38.png)

### What is the top selling product for each category? ###
```sql
with cte as
(
select category_name, product_name, sum(qty) as TotalQuantity,
rank() over(partition by category_name order by sum(qty) desc) as rank
from sales s
join product_details pd on s.prod_id = pd.product_id
group by category_name, product_name
)
select * from cte
where rank = 1
```
![image](https://user-images.githubusercontent.com/77920592/198997038-29e03fb5-3791-4c43-ad20-2fe920c04f4d.png)

### What is the percentage split of revenue by product for each segment? ###
```sql
with cte as
(
select segment_name, product_name, sum(qty*s.price) as TotalRevenue
from sales s
join product_details pd on s.prod_id = pd.product_id
group by segment_name, product_name
)
select *, round(TotalRevenue *100.0 / (select sum(qty*price) from sales),2) as PercentageSplit
from cte
```
![image](https://user-images.githubusercontent.com/77920592/198997094-56873e59-86eb-45f4-9491-3485daa96dde.png)

### What is the percentage split of revenue by segment for each category? ###
```sql
with cte as
(
select category_name, segment_name, sum(qty*s.price) as TotalRevenue
from sales s
join product_details pd on s.prod_id = pd.product_id
group by category_name, segment_name
)
select *, round(TotalRevenue *100.0 / (select sum(qty*price) from sales),2) as PercentageSplit
from cte
```
![image](https://user-images.githubusercontent.com/77920592/198997149-bf7f7670-d66b-4923-81d0-ae655dd0660f.png)

### What is the percentage split of total revenue by category? ###
```sql
with cte as
(
select category_name, sum(qty*s.price) as TotalRevenue
from sales s
join product_details pd on s.prod_id = pd.product_id
group by category_name
)
select *, round(TotalRevenue *100.0 / (select sum(qty*price) from sales),2) as PercentageSplit
from cte
```
![image](https://user-images.githubusercontent.com/77920592/198997191-b298d91e-7674-46a0-bb8e-a2e8587f3610.png)

### What is the total transaction “penetration” for each product? (hint: penetration = number of transactions where at least 1 quantity of a product was purchased divided by total number of transactions) ###
```sql
select s.prod_id, product_name, count(distinct txn_id) * 100.0 / 
				(select count(distinct txn_id) from sales) as penetration_ratio
from sales s
join product_details pd on s.prod_id = pd.product_id
group by s.prod_id, product_name
order by penetration_ratio desc
```
![image](https://user-images.githubusercontent.com/77920592/198997289-4576697e-92cf-47d1-8e45-333ebe83cd90.png)

### What is the most common combination of at least 1 quantity of any 3 products in a 1 single transaction? ###
```sql
select a.prod_id, b.prod_id, c.prod_id, count(*) as Count
from sales a inner join sales b
on a.txn_id = b.txn_id and a.prod_id < b.prod_id
inner join sales c 
on b.txn_id = c.txn_id and b.prod_id < c.prod_id
where a.prod_id = '5d267b'
group by a.prod_id, b.prod_id, c.prod_id
order by Count desc
```
![image](https://user-images.githubusercontent.com/77920592/198997432-08673ba5-b428-4c3f-a91f-e45fb5a0db8b.png)

