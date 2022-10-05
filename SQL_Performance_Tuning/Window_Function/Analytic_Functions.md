## Analytic Functions ##

### LEAD ###

LEAD() with a single argument in the parentheses looks at the next row in the given order and shows the value in the column specified as the argument. 

![image](https://user-images.githubusercontent.com/77920592/194063146-8ae18ebf-ec8d-4c9a-a0b6-0360bc5e291c.png)

LEAD() can be extremely useful when we want to calculate deltas, i.e. differences between two values. 

**Example 1:**

![image](https://user-images.githubusercontent.com/77920592/194063659-bbc43497-6d8c-4a95-90a3-17ca84bb60a8.png)

For WebsiteId = 1, show each statistics row: Day, Revenue, Revenue on the next day (NextDayRevenue) and the Difference between these two values (as next day's minus that day's revenue).

```sql
select
  day,
  revenue,
  lead(revenue) over(order by day asc) as nextdayrevenue,
  lead(revenue) over(order by day asc) - revenue as difference
from statistic
where websiteid = 1;
```

![image](https://user-images.githubusercontent.com/77920592/194064339-852e9cfa-1076-491d-9962-d0b933ec3601.png)

