## Union / Intersect ## 
 
For example, we want to select the total number of customers who have placed their orders before. 
We join and scan both Orders and Customers tables

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


