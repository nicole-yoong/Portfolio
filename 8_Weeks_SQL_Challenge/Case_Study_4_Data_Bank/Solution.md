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
```

### What is the median, 80th and 95th percentile for this same reallocation days metric for each region? ###
```sql
```

## B. Customer Transactions ## 

### What is the unique count and total amount for each transaction type? ###
```sql
```

### What is the average total historical deposit counts and amounts for all customers? ###
```sql
```

### For each month - how many Data Bank customers make more than 1 deposit and either 1 purchase or 1 withdrawal in a single month? ###
```sql
```

### What is the closing balance for each customer at the end of the month? ###
```sql
```

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
