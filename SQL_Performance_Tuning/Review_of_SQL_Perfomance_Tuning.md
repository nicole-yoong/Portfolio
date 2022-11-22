# Review of SQL Performance Tuning #

SQL performance tuning is the process of improving SQL queries to accelerate your servers performance. This article provides a review and findings into the different approach of improving the perfomance of data retrieval. 

## A. String Search ##

The SQL LIKE operator very often causes unexpected performance behavior because some search terms prevent efficient index usage.
Retrieving the data by detecting the presence of a string in any position will be highly inefficient as the SQL Server is evaluating expression against every row to find patterns in the middle of the string.
Indexing is an alternative to speed up the this type of data retrieval. However, retriving substring, meaning that with the presence of % at the beginning/ending of a string, indexing becomes impossisble. 

**Example 1:**
For example, we want to select the total value of the orders where the shipcountry consists of the letters 'an'
```sql
select o.shipcountry, sum(od.unitprice*od.quantity) as TotalValue
from [Order Details] od 
join orders o on o.orderid = od.orderid
where o.shipcountry like '%an%'
group by o.shipcountry
```
![image](https://user-images.githubusercontent.com/77920592/193886361-b8bd981f-12fa-4d11-b6e7-7fadd6b075c0.png)
![image](https://user-images.githubusercontent.com/77920592/193886424-4b477b78-81c9-4414-a4f0-28b2c6b4a2dc.png)

We can only know if a substring exists within a column by going through every character in every row to search for its occurrences and this can be very time-consuming for a large dataset.

There are several approaches to resolve this issue:

### Method 1: Try to be specific. For example, if we specify we want to find out data about 'France', we can leading string search instead of wildcard string search. 

Instead of '%an%', use 'fra%' ###

```sql
select o.shipcountry, sum(od.unitprice*od.quantity) as TotalValue
from [Order Details] od 
join orders o on o.orderid = od.orderid
where o.shipcountry like 'Fra%'
group by o.shipcountry
```
![image](https://user-images.githubusercontent.com/77920592/193886751-3051be92-bec1-4323-9e00-2c0b57f86b7f.png)
![image](https://user-images.githubusercontent.com/77920592/193886826-f09384cd-6106-462d-a0f5-d9c3fc42d502.png)

The more specific the substring is, the more time-efficient the search is. 

### Method 2: Apply indexing ###

Even when we do indexing, LIKE expression can only use the characters before the wildcard.
The remaining characters does not narrow the scanned index range, meaning that the database still has to go through the entire tables to find the matching values. 

** Scenario 1: ** LIKE 'fra%' >>> The index can quickly find rows where the country value starts with the letter 'fra', since 'fra' appears before the wildcard. 
All such rows where the country name begins with a fra are returned because all of them match the criterion. 

** Scenario 2: ** LIKE 'f%a' >>> The index can only find rows with countries starting with 'f'. 
Then, the database needs to manually check these rows and return the ones that end with a 'a'. 

** Scenario 3: ** LIKE '%an' >>> The wildcard appears as the first letter, the index on country is of no use. The database has to check every row individually.

```sql
drop index customer_country on customers;
create index customer_country
on customers(country);
```

```sql
select o.shipcountry, sum(od.unitprice*od.quantity) as TotalValue
from [Order Details] od 
join orders o on o.orderid = od.orderid
where o.shipcountry like 'f%e'
group by o.shipcountry
```

![image](https://user-images.githubusercontent.com/77920592/193889425-17932317-6e75-4fc0-9853-703183022631.png)
![image](https://user-images.githubusercontent.com/77920592/193889464-5b0e9802-61de-4f89-ac24-202868f21bbe.png)

```sql
select o.shipcountry, sum(od.unitprice*od.quantity) as TotalValue
from [Order Details] od 
join orders o on o.orderid = od.orderid
where o.shipcountry like 'fr%'
group by o.shipcountry
```

![image](https://user-images.githubusercontent.com/77920592/193889425-17932317-6e75-4fc0-9853-703183022631.png)
![image](https://user-images.githubusercontent.com/77920592/193889464-5b0e9802-61de-4f89-ac24-202868f21bbe.png)

```sql
select o.shipcountry, sum(od.unitprice*od.quantity) as TotalValue
from [Order Details] od 
join orders o on o.orderid = od.orderid
where o.shipcountry = 'France'
group by o.shipcountry
```

![image](https://user-images.githubusercontent.com/77920592/193890240-81808dc8-94fe-41d3-906e-2687ee8bd2b7.png)
![image](https://user-images.githubusercontent.com/77920592/193890287-be6814b2-315a-4e62-af6a-730ba1f7855b.png)

The resulting execution plan shows you that the cost of the first operation, the LIKE expression, is much more expensive than the = expression.
We keep in mind that when using like, some sql flavors will ignore indexes, and that will kill performance.

### Note: ###

1. If your filter criteria uses equals = and the field is indexed, then most likely it will use an INDEX/CLUSTERED INDEX SEEK

2. If your filter criteria uses LIKE, with no wildcards (like if you had a parameter in a web report that COULD have a % but you instead use the full string), it is about as likely as #1 to use the index. The increased cost is almost nothing.

3. If your filter criteria uses LIKE, but with a wildcard at the beginning (as in shipcountry LIKE '%nce') it's much less likely to use the index, but it still may at least perform an INDEX SCAN on a full or partial range of the index.

4. If your filter criteria uses LIKE, but starts with a STRING FIRST and has wildcards somewhere AFTER that (as in shipcountry LIKE 'f%e'), then SQL may just use an INDEX SEEK to quickly find rows that have the same first starting characters, and then look through those rows for an exact match.

## B. Indexing the OVER() clause ##

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

## C. Framing ##

Another issue associated with the performance tuning is the default frame for SQL Server using **RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.** 
When using empty **OVER()** clause, RANGE will be the default specification. 
RANGE can be particularly useful in scenarios where we do not care about the changes of the amount during a single period, such as day. 
For example, when calculating the running sum from all orders sorted by date, RANGE will be used when we do not really need to see how the running sum changed during single days.

However, RANGE is always associated with some performance issues. The performance issues are more obvious in the cases of aggregration. 
Aggregration always result in a large number of logical reads, causing the data retrieval to perform slowly. There are multiple ways to address the weakness, such as specifying the frame **ROWS BETWEEN UNBOUND PROCEEDING AND CURRENT ROW** to the OVER clause to declare the aggregrated values. 

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

### Variable ###

Following the earlier discussion on the performance issues of using aggregation, there are other methods we can use to enhance the perfomance, such as using variable.

```sql
select orderid, unitprice, quantity,
sum(unitprice*quantity) over() as TotalValue
from [order details]
group by orderid, unitprice, quantity;
```

![image](https://user-images.githubusercontent.com/77920592/194760421-9ee392c9-035a-4689-94d2-8f195238602a.png)

```sql
declare @TotalValue money;
select @TotalValue = sum(unitprice*quantity) from [order details];

select orderid, unitprice, quantity,
@TotalValue as TotalValue
from [order details]
group by orderid, unitprice, quantity
```

![image](https://user-images.githubusercontent.com/77920592/194760449-2d23cbd3-a566-4b1b-b224-3509263ee084.png)

The first query only scans the table once, but it has 4382 logical reads in a worktable. 
The second query scans the table twice, but it doesn’t need the worktable.

## D. Union / Intersect ## 
 
For example, we want to select the total number of customers who have placed their orders before. 
We join and scan both Orders and Customers tables

**Example 1:**
```sql
select count (distinct o.customerid)
from orders o join customers c 
on o.customerid = c.customerid
where exists (select customerid from orders)
```

![image](https://user-images.githubusercontent.com/77920592/193830849-648ba300-526d-44ab-a235-dd2a46e29ec7.png)
![image](https://user-images.githubusercontent.com/77920592/193884370-7df156f7-756d-433a-898a-de0fa2c66907.png)

```sql
select count(*) from 
(
select customerid from orders
intersect
select customerid from customers
) I
```

![image](https://user-images.githubusercontent.com/77920592/193830976-88f022f3-19f6-411d-8ce6-e80ac7bf9309.png)
![image](https://user-images.githubusercontent.com/77920592/193884520-81867fc1-7a62-4e1b-986d-de923603bfe6.png)

In the first query, it took a massive computing power, 60 more times read to pull out the result.
Considering that Orders contains only 830 rows and Customers contains 91 rows, we read far more data than the full contents of each of these tables. 
