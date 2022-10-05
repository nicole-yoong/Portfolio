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

# Window Frame #

Window frames define precisely which rows should be taken into account when computing the results and are always relative to the current row.
For example, you can create a window frame that includes the current row, the three rows before it, and the three rows after it. This opens up the possibility of new kinds of queries.

Two rows before and two rows after the current row are selected:

![image](https://user-images.githubusercontent.com/77920592/194053036-0075fe71-b000-4826-81ab-96f05d99a5a7.png)

### ROW ###

- UNBOUNDED PRECEDING – the first possible row.
- n PRECEDING – the n-th row before the current row (instead of n, write the number of your choice).
- CURRENT ROW – the current row only.
- n FOLLOWING – the n-th row after the current row.
- UNBOUNDED FOLLOWING – the last possible row.

The lower bound must come before the upper bound. 
In other words, a construction like: ...ROWS BETWEEN CURRENT ROW AND UNBOUNDED PRECEDING doesn't make sense. 

For the following example, the query computes:
- the total price of all orders placed so far (this kind of sum is called a running total), and
- the total price of the current order, the 3 preceding orders and the 3 following orders.

```sql
select
  id,
  totalprice,
  sum(totalprice) over(order by placeddate asc rows unbounded preceding) as runningtotal,
  sum(totalprice) over(order by placeddate asc rows between 3 preceding and 3 following) as sum3beforeafter
from singleorder
order by placeddate asc;
```

![image](https://user-images.githubusercontent.com/77920592/194054209-e42d3818-e857-4290-97cd-5905950e58c5.png)

Abbreviations:

SQL Server allows us to use abbreviated syntax to make things easier:

- ROWS UNBOUNDED PRECEDING means BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
- ROWS n PRECEDING means BETWEEN n PRECEDING AND CURRENT ROW
- ROWS n FOLLOWING means BETWEEN CURRENT ROW AND n FOLLOWING
- ROWS CURRENT ROW means BETWEEN CURRENT ROW AND CURRENT ROW

### RANGE ###

The difference between ROWS and RANGE is that RANGE will take into account all rows that have the same value in the column which we order by. This might be helpful with dates.

For example, we want to calculate the running sum from all orders sorted by date but we don't really need to see how the running sum changed during single days. 
We just need to show the values at the end of the day. If there are multiple orders on a single day, add them together.

We could do something like this:
```sql
select
  id,
  placeddate,
  totalprice,
  sum(totalprice) over(order by placeddate asc range unbounded preceding) as runningsum
from singleorder;
```

![image](https://user-images.githubusercontent.com/77920592/194055997-9b35a01b-6068-4171-8623-5baab7f494e3.png)

More examples on RANGE:

![image](https://user-images.githubusercontent.com/77920592/194058423-a2a0f9ff-aa8d-47b0-b408-c138e3dd6713.png)

** Example 1: **

For each StockChange, show Id, ProductId, Quantity, ChangedDate and the total quantity change from all StockChange for that product. Name the column SumQuantity.
We want to know total quantity change of a certain product, regardless of the changeddate. Therefore, RANGE will be used. 

```sql
select id, productid, quantity, changeddate,
sum(quantity) over(order by productid asc range current row) as SumQuantity
from stockchange
```

![image](https://user-images.githubusercontent.com/77920592/194058505-583ca772-cf73-465e-9038-4fd3b90a71d7.png)

** Example 2: **

For each StockChange, show its Id, the ChangedDate, and the number of stock changes that took place on the same day or any time earlier. Name this column StockChangeNumber.

```sql
select id, changeddate,
count(*) over(order by changeddate asc range between unbounded preceding and current row) as StockChangeNumber
from stockchange
```

![image](https://user-images.githubusercontent.com/77920592/194059135-7742d182-45b3-4125-a5c1-b6ec8b25a75e.png)

### ROWS and RANGE – what's the difference? ###

For the following queries with ROWS, it  sums the TotalPrice for all rows which have a ROW_NUMBER() less than or equal to the row number of the current row.
```sql
select
  id,
  placeddate,
  totalprice,
  row_number() over(order by placeddate asc) as rownumber,
  sum(totalprice) over(order by
    placeddate asc rows unbounded preceding) as runningsum
from singleorder;
```
![image](https://user-images.githubusercontent.com/77920592/194056828-c7eb3cea-4596-4195-97c4-9eb319c74705.png)

For the following queries with RANGE,  it sums up the TotalPrice for all rows which have a RANK() less than or equal to the rank of the current row.
```sql
select
  id,
  placeddate,
  totalprice,
  rank() over(order by placeddate asc) as ranking,
  sum(totalprice) over(order by
    placeddate asc range unbounded preceding) as runningsum
from singleorder;
```
![image](https://user-images.githubusercontent.com/77920592/194056861-6e73138c-dacf-4f89-af75-190078e21ea9.png)


