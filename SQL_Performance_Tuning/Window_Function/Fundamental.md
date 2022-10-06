# Fundamental Knowledge #

## Sample Database ##

![image](https://user-images.githubusercontent.com/77920592/194050135-c05bc442-682f-47c3-9b49-916254d071ab.png)
![image](https://user-images.githubusercontent.com/77920592/194050263-cb09a9c0-59cb-4294-a828-cb6f1ec6f902.png)


## Rank ##
It returns the rank of each row as a number. This rank is determined by the sorting criteria specified within the RANK() statement's brackets.

Find the Name, Genre, and Size of the smallest game in our database.
```sql
with ranking_cte as
(
  select name, genre, size, rank() over(order by size asc) as rank
  from game
)

select name, genre, size
from ranking_cte 
where rank = 1
```
![image](https://user-images.githubusercontent.com/77920592/194052400-7df5b884-09b6-40b6-ac6e-8c4d232fde64.png)

## Dense_Rank ##
It gives a "dense" rank indeed – there are no gaps in the numbering.

## Row_Number ##
It gives a unique rank to each row. The order is nondeterministic.

### Differences ###
For each game, show its name, genre, and date of release. In the next three columns, show each game's RANK(), DENSE_RANK() and ROW_NUMBER() sorted by the date of release. Name these columns Rank, DenseRank, and RowNumber
```sql
select name, genre, releasedate,
rank() over(order by releasedate) as Rank,
dense_rank() over(order by releasedate) as DenseRank,
row_number() over(order by releasedate) as RowNumber
from game
```
![image](https://user-images.githubusercontent.com/77920592/194051282-d6b8ef42-ce7c-4adf-8bf8-524249a9b1ee.png)

## NTILE(X) ##
It distributes the rows into a set number of groups, which is specified by X.

![image](https://user-images.githubusercontent.com/77920592/194051822-4c02fa0a-4ea1-4dab-960e-47b7299f507e.png)

We want to divide games into four groups based on size, with the biggest games coming first. For each game, show its Name, Genre, Size, and the GroupNo it belongs to.
```sql
select name, genre, size, 
ntile(4) over(order by size desc) as GroupNo
from game
```
![image](https://user-images.githubusercontent.com/77920592/194051785-eccd7d7e-749f-4fe4-8bda-0cb4a34d5aae.png)


# More Complex Queries #

### Database ###

![image](https://user-images.githubusercontent.com/77920592/194087824-9a70f020-658f-4e04-a48e-27344d9fba7c.png)
![image](https://user-images.githubusercontent.com/77920592/194087904-dac1ac7a-bb19-4a4d-bc6a-7c42dec4fa18.png)

For all sales between August 10 and August 14, 2016, show the following information: StoreId, Day, number of customers and rank (based on the number of customers in that store). Name the column Ranking.

```sql
select storeid, day, customers, 
rank() over(partition by storeid order by customers asc) as Ranking
from sales
where day between '2016-08-10' and '2016-08-14'
```

![image](https://user-images.githubusercontent.com/77920592/194088062-aa681024-1cf0-46cb-b3b3-bed77e389906.png)

Take the sales between August 1 and August 10, 2016. For each row, show the StoreId, the Day, the Revenue on that day, and the quartile number based on the Revenue of that store in descending order. Name the column Quartile.

```sql
select storeid, day, revenue,
ntile(4) over(partition by storeid order by revenue desc) as Quartile
from sales
where day between '2016-08-01' and '2016-08-10'
```

![image](https://user-images.githubusercontent.com/77920592/194088653-14189bd1-397f-4b8a-8987-448d1cb10043.png)

For each store, show a row with three columns: StoreId, the highest daily Revenue for that store, and the Day when that revenue was achieved.

```sql
with cte as
(
  select storeid, day, revenue, 
  rank() over(partition by storeid order by revenue desc) as rank
  from sales
)
select storeid, day, revenue
from cte
where rank = 1
```

![image](https://user-images.githubusercontent.com/77920592/194292029-b0b5842b-c1b1-4cb3-879b-4e777bc90087.png)

Let's analyze sales data between August 1 and August 3, 2016. For each row, show the StoreId, Day, Transactions and the ranking of the store (based on the daily number of transactions). The store with the greatest number of transactions should get Rank = 1. Use individual row ranks even when two rows share the same value.

```sql
select storeid, day, transactions, 
row_number() over(partition by day order by transactions desc) as rank
from sales
where day between '2016-08-01' and '2016-08-03'
```

![image](https://user-images.githubusercontent.com/77920592/194292113-987ba84f-a6a7-42ca-bab6-c67eeeee134a.png)

For each sales day, show the Day, the StoreId of the best store in terms of the Revenue on that Day, and that store's Revenue.

```sql
with cte as
(
  select day, storeid, revenue,
  rank() over(partition by day order by revenue desc) as rank
  from sales
)
select day, storeid, revenue
from cte
where rank = 1
```

![image](https://user-images.githubusercontent.com/77920592/194292649-c956701d-2a85-4411-bb8d-79d429e4eeb6.png)

