## String Search ##

The SQL LIKE operator very often causes unexpected performance behavior because some search terms prevent efficient index usage.
Retrieving the data by detecting the presence of a string in any position will be highly inefficient as the SQL Server is evaluating expression against every row to find patterns in the middle of the string.
Indexing is an alternative to speed up the this type of data retrieval. However, retriving substring, meaning that with the presence of % at the beginning/ending of a string, indexing becomes impossisble. 

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

### 1. Try to be specific. For example, if we specify we want to find out data about 'France', we can leading string search instead of wildcard string search. 
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

### 2. Apply indexing ###

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
