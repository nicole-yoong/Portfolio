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

**Abbreviations:**

SQL Server allows us to use abbreviated syntax to make things easier:

- ROWS UNBOUNDED PRECEDING means BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
- ROWS n PRECEDING means BETWEEN n PRECEDING AND CURRENT ROW
- ROWS n FOLLOWING means BETWEEN CURRENT ROW AND n FOLLOWING
- ROWS CURRENT ROW means BETWEEN CURRENT ROW AND CURRENT ROW


### RANGE ###

The difference between ROWS and RANGE is that RANGE will take into account all rows that have the same value in the column which we order by. This might be helpful with dates.
RANGE is only supported with UNBOUNDED and CURRENT ROW window frame delimiters. 

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

**Example 1:**

For each StockChange, show Id, ProductId, Quantity, ChangedDate and the total quantity change from all StockChange for that product. Name the column SumQuantity.
We want to know total quantity change of a certain product, regardless of the changeddate. Therefore, RANGE will be used. 

```sql
select id, productid, quantity, changeddate,
sum(quantity) over(order by productid asc range current row) as SumQuantity
from stockchange
```

![image](https://user-images.githubusercontent.com/77920592/194058505-583ca772-cf73-465e-9038-4fd3b90a71d7.png)

**Example 2:**

For each StockChange, show its Id, the ChangedDate, and the number of stock changes that took place on the same day or any time earlier. Name this column StockChangeNumber.

```sql
select id, changeddate,
count(*) over(order by changeddate asc range between unbounded preceding and current row) as StockChangeNumber
from stockchange
```

![image](https://user-images.githubusercontent.com/77920592/194059135-7742d182-45b3-4125-a5c1-b6ec8b25a75e.png)


**Example 3:**

![image](https://user-images.githubusercontent.com/77920592/194059557-a9d7433c-63ab-47db-a9fc-0587bb3ba1ad.png)

Our finance department needs to estimate future cash flows for each date. To do that, we need to show each order's Id, PlacedDate, TotalPrice, and the total sum of all order prices from the same day or any later date. Name the column FutureCashFlow.

```sql
select id, placeddate, totalprice,
sum(totalprice) over(order by placeddate range between current row and unbounded following) as FutureCashFlow
from singleorder
```

![image](https://user-images.githubusercontent.com/77920592/194059629-b4fc607a-dd18-4343-898d-e5d9873a9407.png)

**Default window timeframe for RANGE:**

- If you don't specify an ORDER BY clause within OVER(...), the whole partition of rows will be used as the window frame.
- If you do specify an ORDER BY clause within OVER(...), the database will assume RANGE UNBOUNDED PRECEDING as the window frame.

![image](https://user-images.githubusercontent.com/77920592/194059557-a9d7433c-63ab-47db-a9fc-0587bb3ba1ad.png)

**Example 1:**

For each single order, show its Id, the date when it was placed, the total price, and the sum of all total prices (SumTotalPrice).

```sql
select id, placeddate, totalprice,
sum(totalprice) over() as SumTotalPrice
from singleorder
```

![image](https://user-images.githubusercontent.com/77920592/194060659-5062afc3-2f59-4cd8-8808-90e8c1541d51.png)

**Example 2:**

For each order, show its Id, PlacedDate, TotalPrice and the sum of all total prices. Sort the orders by PlacedDate, but do not specify any window frame.
The sum of TotalPrices should be calculated as if you wrote RANGE UNBOUNDED PRECEDING.

```sql
select id, placeddate, totalprice,
sum(totalprice) over(order by placeddate) as SumTotalPrice
from singleorder
```

![image](https://user-images.githubusercontent.com/77920592/194060955-2cd9a6ba-44c8-44b5-bb03-93a7e32d61ec.png)

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

# More Complex Queries #

### Database ###

![image](https://user-images.githubusercontent.com/77920592/194087824-9a70f020-658f-4e04-a48e-27344d9fba7c.png)
![image](https://user-images.githubusercontent.com/77920592/194087904-dac1ac7a-bb19-4a4d-bc6a-7c42dec4fa18.png)

Take sales from August 1 to August 10, 2016. For each row, show the following information: StoreId, Day, number of transactions, and the average number of transactions for that store in the window frame starting 2 days before and ending 2 days after the current row. Name the column AvgTransactions.

```sql
select storeid, day, transactions, 
avg(transactions) over(partition by storeid order by day asc 
                       rows between 2 preceding and 2 following) as AvgTransactions
from sales
where day between '2016-08-01' and '2016-08-10'
```

![image](https://user-images.githubusercontent.com/77920592/194293730-22fba7d7-797d-4d32-8d46-7316f402ef5b.png)

For each sales row, show the following information: StoreId, Day, Revenue, and the future cash flow receivable by headquarters (i.e. the total revenue in that store, counted from the current day until the last day in our table). Name the column FollowingRevenue.

```sql
select storeid, day, revenue,
sum(revenue) over(partition by storeid order by day asc
                 rows between current row and unbounded following) as FollowingRevenue
from sales
```

![image](https://user-images.githubusercontent.com/77920592/194294369-0efdc6d2-abb7-4d74-953a-0e6f1468a475.png)
