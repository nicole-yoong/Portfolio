# Crypto Market Transaction Monitoring #

Create a query to return a list of suspicious transactions.

Suspicious transactions are defined as:

- a series of two or more transactions occur at intervals of an hour or less
- they are from the same sender
- the sum of transactions in a sequence is 150 or greater

A sequence of suspicious transactions may occur over time periods greater than one hour. 

As an example, there are 5 transactions from one sender for 30 each. They occur at intervals of less than an hour between from 8 AM to 11AM. These are suspicious and will all be reported as one sequence that starts at 8AM, ends at 11AM, with 5 transactions that sum to 150.

The result should return the following:
- sender
- sequence_start: timestamp of the first transaction in the sequence
- sequence_end: timestamp of the last transaction in the sequence
- transactions_count: number of transactions in the sequence
- transactions_sum: sum of transaction amounts in the sequence to 6 places after the decimal

```sql
with cte2 as(
select dt, sender, amount, 
datediff(minute, lag(dt) over(order by sender, dt), dt) as Interval,
row_number() over(order by sender, dt) as rownumber
from transact),

cte3  as(
select * from cte2
where rownumber in (select rownumber from cte2 where abs(interval)< 60)
),

cte4 as(
select * from cte2 where rownumber in (select rownumber from cte3
union select rownumber - 1 as rownumber from cte3)
)
select sender, min(dt) as sequence_start, 
max(dt) as sequence_end, count(rownumber) as transaction_count,
sum(amount) as transaction_sum
from cte4
group by sender
having sum(amount) >= 150
```
