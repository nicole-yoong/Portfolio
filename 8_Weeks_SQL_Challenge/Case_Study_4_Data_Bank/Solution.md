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
WITH deposit_cte AS
(SELECT customer_id, COUNT(txn_type) AS type_count, 
AVG(txn_amount) as deposit_avg
FROM customer_transactions
WHERE txn_type = 'deposit'
GROUP BY customer_id)

SELECT AVG(type_count) AS avg_count, AVG(deposit_avg) AS avg_deposit
FROM deposit_cte
```
![image](https://user-images.githubusercontent.com/77920592/192097311-4f0203ad-37e7-4265-b6a9-855eb395b6da.png)

### For each month - how many Data Bank customers make more than 1 deposit and either 1 purchase or 1 withdrawal in a single month? ###
```sql
WITH monthly_transaction_cte AS

(SELECT customer_id, MONTH(txn_date) AS txn_month,
SUM(CASE WHEN txn_type = 'deposit' THEN 1 ELSE 0 END) AS deposit_count,
SUM(CASE WHEN txn_type = 'purchase' THEN 1 ELSE 0 END) AS purchase_count,
SUM(CASE WHEN txn_type = 'withdrawal' THEN 1 ELSE 0 END) AS withdrawal_count
FROM customer_transactions
GROUP BY customer_id, MONTH(txn_date)
)

SELECT txn_month, COUNT(DISTINCT customer_id) AS customer_count
FROM monthly_transaction_cte
WHERE deposit_count > 1 AND (purchase_count = 1 OR withdrawal_count = 1)
GROUP BY txn_month;
```
![image](https://user-images.githubusercontent.com/77920592/192097327-a37f70f0-2b24-4511-9c66-696076ab84f8.png)

### What is the closing balance for each customer at the end of the month? ###
```sql
WITH monthly_balance_cte AS

(SELECT customer_id, txn_amount, MONTH(txn_date) AS txn_month,
SUM(CASE WHEN txn_type='deposit' THEN txn_amount ELSE -txn_amount END) 
AS net_amount
FROM customer_transactions
GROUP BY customer_id, MONTH(txn_date), txn_amount)

SELECT customer_id, txn_month, net_amount,
SUM(net_amount) over(PARTITION BY customer_id
                     ORDER BY txn_month ROWS BETWEEN UNBOUNDED preceding AND CURRENT ROW) 
					 AS closing_balance
FROM monthly_balance_cte;
```
![image](https://user-images.githubusercontent.com/77920592/192099485-cf1a263e-6a6d-4cb0-9cd1-9b33e1bb721d.png)

### What is the percentage of customers who increase their closing balance by more than 5%? ###
```sql
```


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