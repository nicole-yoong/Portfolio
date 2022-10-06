SQL performance tuning is the process of improving SQL queries to accelerate your servers performance.

## Indexing the OVER() clause ##

The PARTITION BY() and ORDER BY() within the OVER() clause can cause sorting. 

**Example 1:**

```sql
select orderid, shipcountry, freight as TotalValue, 
row_number() over(partition by shipcountry order by freight asc) as Rank
from orders
```
![image](https://user-images.githubusercontent.com/77920592/194341084-2f4a06e1-2eda-4439-8078-d9cb0649d855.png)

![image](https://user-images.githubusercontent.com/77920592/194341769-2fd5ec4f-39e4-4b39-91c7-c2947e6f241e.png)

![image](https://user-images.githubusercontent.com/77920592/194342954-e7cd1ae8-c2ee-422f-84d8-516fef2037d1.png)

```sql
create nonclustered index shipcountry_freight
on orders
(shipcountry, freight);

select orderid, shipcountry, freight as TotalValue, 
row_number() over(partition by shipcountry order by freight asc) as Rank
from orders
```
![image](https://user-images.githubusercontent.com/77920592/194341092-a9f1a092-62bf-4162-b398-6e978e35ed98.png)

![image](https://user-images.githubusercontent.com/77920592/194341181-f12db793-ee61-47c1-a36a-00db3bb16cc3.png)

![image](https://user-images.githubusercontent.com/77920592/194341252-643e0207-0302-4d52-9908-cdab39888f24.png)

The execution plan shows just one sort operation, a combination of shipcountry and freight and the cost of sort operation is quite expensive, 57%. 
Using the non clustered index consisting the columns in the OVER() clause as shown above, the sort operation is now gone from the execution plan.

**Example 2:**

```sql
select o.orderid, o.orderdate, 
sum(unitprice*quantity) over
(partition by o.orderid order by o.orderdate asc
rows between unbounded preceding and current row) as RunningTotal
from orders o join [order details] od on o.orderid = od.orderid;
```

![image](https://user-images.githubusercontent.com/77920592/194327262-19b7fece-fb7f-4bf9-a3c4-9aab5330b720.png)

![image](https://user-images.githubusercontent.com/77920592/194327518-db8ab573-7cf9-4cca-a64e-1e67ceb7dd45.png)

![image](https://user-images.githubusercontent.com/77920592/194329662-69b4bddc-e08f-4ebf-8433-5e34986cb964.png)

```sql
create nonclustered index orderid_orderdate 
on orders
(orderid, orderdate);

select o.orderid, o.orderdate, 
sum(unitprice*quantity) over
(partition by o.orderid order by o.orderdate asc
rows between unbounded preceding and current row) as RunningTotal
from orders o join [order details] od on o.orderid = od.orderid;
```

![image](https://user-images.githubusercontent.com/77920592/194327262-19b7fece-fb7f-4bf9-a3c4-9aab5330b720.png)

![image](https://user-images.githubusercontent.com/77920592/194329893-cd71f066-350c-49eb-b6be-cf0a7891fb90.png)

![image](https://user-images.githubusercontent.com/77920592/194329953-dc37d242-b617-47ec-b1e3-0a52121c516e.png)

In the example above, despite cluster key is used as the ORDER BY option and no sorting is involved, the performance comparison is quite clear after a non clustered index is created for the OVER() clause. 
Itzik Ben-Gan in his book, Microsoft SQL Server 2012 High-Performance T-SQL Using Window Functions recommends the POC index. POC stands for (P)ARTITION BY, (O)RDER BY, and (c)overing. 
He recommends adding any columns used for filtering before the PARTITION BY and ORDER BY columns in the key. Then add any additional columns needed to create a covering index as included columns. 

## Framing ##

Another issue associated with the performance tuning is the default frame for SQL Server using **RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.** 
When using empty **OVER()** clause, RANGE will be the default specification. 
RANGE can be particularly useful in scenarios where we do not care about the changes of the amount during a single period, such as day. 
For example, when calculating the running sum from all orders sorted by date, RANGE will be used when we do not really need to see how the running sum changed during single days.

However, RANGE is always associated with some performance issues. 

We want to find the running total of the order amount (unitprice * quantity) in the following queries. 

```sql
select o.orderid, o.orderdate, 
sum(unitprice*quantity) over
(partition by o.orderid order by o.orderdate asc) as RunningTotal
from orders o join [order details] od on o.orderid = od.orderid;
```
![image](https://user-images.githubusercontent.com/77920592/194326927-e2e2c79c-f3ad-43c6-921f-33f3d2850ef4.png)

![image](https://user-images.githubusercontent.com/77920592/194327591-b58c0617-1599-476f-bfe7-7b1fe76c3318.png)

```sql
select o.orderid, o.orderdate, 
sum(unitprice*quantity) over
(partition by o.orderid order by o.orderdate asc
rows between unbounded preceding and current row) as RunningTotal
from orders o join [order details] od on o.orderid = od.orderid;
```

![image](https://user-images.githubusercontent.com/77920592/194327262-19b7fece-fb7f-4bf9-a3c4-9aab5330b720.png)

![image](https://user-images.githubusercontent.com/77920592/194327518-db8ab573-7cf9-4cca-a64e-1e67ceb7dd45.png)

Looking at the Statistic IO of the two queries, discrepancy can be observed. 
The first query without specifying the framing, with RANGE as the default, the worktable consists of 10281 logical reads. 
The worktable consists of 0 logical reads in the second query using ROWS framing. 

Besides, when the values in the ORDER BY column is not unique, such as the matching dates as part of the same window, calculation error can easily arise. 
Taking the queries above as example, there are multiple customers placing orders on the same date.
Therefore, when calculating the running total, the running total of these rows with the same date will show the same amount. 

In order to perform the window function calculation, such as a running total, SQL Server creates a worktable and populates it with each partition. 
Worktable is created in the tempdb when RANGE is used. In contrast, it is created in memory, consisting of no I/O when ROWS is used, so it performs much better.


Therefore, it is crucial to specify the frame where it’s supported.
