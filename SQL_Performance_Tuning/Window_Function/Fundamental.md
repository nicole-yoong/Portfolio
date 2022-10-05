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



