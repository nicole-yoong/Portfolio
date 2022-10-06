# Common Problems with Window Functions #

# Database #

## Can't use window functions in the WHERE clause, use subqueries instead ##

Find the Id, Country, and Views for auctions where the number of views was below the average.

```sql
select id, country, views
from (select id, country, views, avg(views) over() as avgviews from auction) c
where views < avgviews
```
![image](https://user-images.githubusercontent.com/77920592/194300320-1456ee5c-9596-4e94-b8ad-f99a3153f62b.png)

## Can't use window functions in the HAVING clause, use subqueries instead ##

Show the country name and average final auction price for countries that have higher than average final price. Correct the query by using a subquery.

```sql
select country, avg(finalprice) as avgfinalprice
from auction
group by country
having avg(finalprice) > (select avg(finalprice) from auction)
```

![image](https://user-images.githubusercontent.com/77920592/194301144-9a320932-ca5a-4539-90fb-894525ab75ac.png)

## Can't use window functions in the GROUP BY clause, use subqueries instead ##

