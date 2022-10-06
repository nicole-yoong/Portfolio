# Common Problems with Window Functions #

The only places where we can use window functions without subqueries are the SELECT and ORDER BY clauses.

# Database #

![image](https://user-images.githubusercontent.com/77920592/194302116-4c3838a2-a9da-4882-91eb-f0c866984f55.png)
![image](https://user-images.githubusercontent.com/77920592/194302160-e189906f-638d-45de-ad48-7820d3e0f3cf.png)

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

Divide all auctions into six equal groups, based on AskingPrice in ascending order. Show the columns GroupNo, MinAskingPrice, AvgAskingPrice and MaxAskingPrice for each group. Sort in ascending order by group.

```sql
select groupno, min(askingprice) as MinAskingPrice, 
avg(askingprice) as AvgAskingPrice, max(askingprice) as MaxAskingPrice
from (
		select askingprice, ntile(6) over(order by askingprice asc) as GroupNo 
  		from auction) c
group by groupno
```

![image](https://user-images.githubusercontent.com/77920592/194301893-0eee2e7f-7f24-4639-bef9-c12f78f4b542.png)

Group the auctions by the Country. Show the country, its minimal number of participants in an auction and the average minimal number of participants across all countries. Name the last columns MinParticipants and AvgMinParticipants.

```sql
select country, min(participants) as MinParticipants, 
avg(min(participants)) over() as AvgMinParticipants
from auction
group by country
```

![image](https://user-images.githubusercontent.com/77920592/194302823-e26f4c04-7bc4-4c15-b46d-ea9aa915f525.png)

For each end date, show the following:
- the EndDate
- the sum of views from auctions that ended on that day (name this column SumViews)
- the sum of views from the previous day (name this column PreviousDay)
- the difference between the sum of views on that day and on the previous day (name this column Delta)

```sql
select enddate, sum(views) as SumViews,
lag(sum(views), 1) over(order by enddate asc) as PreviousDay,
sum(views) - lag(sum(views), 1) over(order by enddate asc) as Delta
from auction
group by enddate
```

![image](https://user-images.githubusercontent.com/77920592/194304261-70357e77-085b-4b26-a2d4-9162bb596067.png)

Group all auctions by category and end date and show the following columns:
- CategoryId
- EndDate
- the average daily final price as DailyAvgFinalPrice for that category on that day
- the maximal daily average (as DailyMaxAvg) in that category for any day

```sql
select categoryid, enddate, 
avg(finalprice) as DailyAvgFinalPrice,
max(avg(finalprice)) over(partition by categoryid) as DailyMaxAvg
from auction
group by categoryid, enddate
```

![image](https://user-images.githubusercontent.com/77920592/194304866-7de97c5a-47c4-4877-8ce5-137a4be57158.png)

