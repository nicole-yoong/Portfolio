# Introduction #
There is a new innovation in the financial industry called Neo-Banks: new aged digital only banks without physical branches.
Danny thought that there should be some sort of intersection between these new age banks, cryptocurrency and the data world…so he decides to launch a new initiative - Data Bank!
Data Bank runs just like any other digital bank - but it isn’t only for banking activities, they also have the world’s most secure distributed data storage platform!
Customers are allocated cloud data storage limits which are directly linked to how much money they have in their accounts. There are a few interesting caveats that go with this business model, and this is where the Data Bank team need your help!
The management team at Data Bank want to increase their total customer base - but also need some help tracking just how much data storage their customers will need.
This case study is all about calculating metrics, growth and helping the business analyse their data in a smart way to better forecast and plan for their future developments!


# Case Study Questions #
The following case study questions include some general data exploration analysis for the nodes and transactions before diving right into the core business questions and finishes with a challenging final request!

## A. Customer Nodes Exploration ##
How many unique nodes are there on the Data Bank system?

```sql
select count(distinct node_id) from customer_nodes
```
![image](https://user-images.githubusercontent.com/77920592/192092863-0f91fce2-f6c1-475a-85e4-7566461dc145.png)

### What is the number of nodes per region? ###
```sql
select regions.region_id, regions.region_name, count(node_id) as node_count
from customer_nodes join regions 
on customer_nodes.region_id = regions.region_id
group by regions.region_id, regions.region_name
order by regions.region_id
```

![image](https://user-images.githubusercontent.com/77920592/192093089-df876c49-7097-4028-8b76-627b939ddb07.png)

### How many customers are allocated to each region? ###
```sql
select regions.region_id, count(distinct customer_id) as customer_count
from customer_nodes join regions 
on customer_nodes.region_id = regions.region_id
group by regions.region_id
```

![image](https://user-images.githubusercontent.com/77920592/192093186-9aaea2fd-0f66-486f-b0a3-f6ba0e873ba6.png)

### How many days on average are customers reallocated to a different node? ###
```sql
SELECT avg(datediff(day, start_date, end_date)) AS avg_days
FROM customer_nodes
WHERE end_date!='9999-12-31';
```

### What is the median, 80th and 95th percentile for this same reallocation days metric for each region? ###
```sql
```

## B. Customer Transactions ## 

### What is the unique count and total amount for each transaction type? ###
```sql
SELECT txn_type, COUNT (*) AS unique_count,
SUM (txn_amount) AS total_amont
FROM customer_transactions
GROUP BY txn_type
```
![image](https://user-images.githubusercontent.com/77920592/192097298-6841a19d-daaa-48da-b79c-19fb9417e3aa.png)

### What is the average total historical deposit counts and amounts for all customers? ###
```sql
with cte as
(
select customer_id, count(txn_type) as TotalCount, 
sum(txn_amount) as TotalAmount
from customer_transactions
where txn_type = 'deposit'
group by customer_id
)
select avg(TotalCount), avg(TotalAmount) as AvgTotalAmount
from cte 
```
![image](https://user-images.githubusercontent.com/77920592/196947051-1b2bc3f3-4c33-4d43-b179-46f042f70227.png)

### For each month - how many Data Bank customers make more than 1 deposit and either 1 purchase or 1 withdrawal in a single month? ###
```sql
with cte as
(
select customer_id, datepart(month, txn_date) as Month,
sum(case when txn_type = 'deposit' then 1 else 0 end) as deposit,
sum(case when txn_type = 'withdrawal' then 1 else 0 end) as withdrawal,
sum(case when txn_type = 'purchase' then 1 else 0 end) as purchase
from customer_transactions
group by datepart(month, txn_date), customer_id
)
select count(customer_id) as TotalCount, month
from cte
where deposit > 1 and (purchase = 1 or withdrawal = 1)
group by month;
```
![image](https://user-images.githubusercontent.com/77920592/196954838-39643750-45ac-4cab-b9b7-0a1581d2bcca.png)

### What is the closing balance for each customer at the end of the month? ###
```sql
with cte as
(
select customer_id, datepart(month, txn_date) as Closing_month, txn_date,
(case when txn_type = 'deposit' then +txn_amount else -txn_amount end) as TotalAmount
from customer_transactions 
),
cte2 as
(
select customer_id, closing_month, txn_date, TotalAmount,
sum(TotalAmount) over(partition by customer_id, closing_month order by txn_date asc rows between unbounded preceding and current row) as Closing_balance,
rank() over(partition by customer_id, closing_month order by txn_date desc) as Rank
from cte
)
select customer_id, closing_month, closing_balance
from cte2
where rank = 1
order by customer_id;
```
![image](https://user-images.githubusercontent.com/77920592/196954720-faca7d14-c37f-4cc0-804c-082ce0404e91.png)

### What is the percentage of customers who increase their closing balance by more than 5%? ###
```sql
with cte as
(
select customer_id, datepart(month, txn_date) as Closing_month, txn_date,
(case when txn_type = 'deposit' then +txn_amount else -txn_amount end) as TotalAmount
from customer_transactions 
),
cte2 as
(
select customer_id, closing_month, txn_date, TotalAmount,
sum(TotalAmount) over(partition by customer_id, closing_month order by txn_date asc rows between unbounded preceding and current row) as Closing_balance,
rank() over(partition by customer_id, closing_month order by txn_date desc) as Rank
from cte
),
cte3 as
(
select customer_id, closing_month, closing_balance, lag(closing_balance, 1, 0) over(partition by customer_id order by closing_month asc) as previous_closing_balance
from cte2
where rank = 1
),
cte4 as 
(
select customer_id, closing_month, closing_balance, previous_closing_balance, round(((closing_balance*1.0 - previous_closing_balance) / closing_balance),2) as percentage_change
from cte3
)
select count(distinct customer_id) as Count from cte4
where percentage_change >= 5
```
![image](https://user-images.githubusercontent.com/77920592/196961488-55479fc4-6015-49fe-a3ee-4ea6a68cdc5d.png)

## C. Data Allocation Challenge ##

To test out a few different hypotheses - the Data Bank team wants to run an experiment where different groups of customers would be allocated data using 3 different options:

Option 1: data is allocated based off the amount of money at the end of the previous month
Option 2: data is allocated on the average amount of money kept in the account in the previous 30 days
Option 3: data is updated real-time
For this multi-part challenge question - you have been requested to generate the following data elements to help the Data Bank team estimate how much data will need to be provisioned for each option:
- running customer balance column that includes the impact each transaction
- customer balance at the end of each month
- minimum, average and maximum values of the running balance for each customer

Using all of the data available - how much data would have been required for each option on a monthly basis?
