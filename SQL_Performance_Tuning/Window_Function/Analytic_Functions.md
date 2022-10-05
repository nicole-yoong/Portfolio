# Analytic Functions #

## LEAD(x) / LAG(x) ##

LEAD() with a single argument in the parentheses looks at the NEXT row in the given order and shows the value in the column specified as the argument. 

![image](https://user-images.githubusercontent.com/77920592/194063146-8ae18ebf-ec8d-4c9a-a0b6-0360bc5e291c.png)

LEAD() can be extremely useful when we want to calculate deltas, i.e. differences between two values. 

LAG() with a single argument in the parentheses looks at the PREVIOUS row in the given order and shows the value in the column specified as the argument. 

![image](https://user-images.githubusercontent.com/77920592/194081659-06652ca9-291b-4555-b52a-384dbf7c0861.png)

**Database**

![image](https://user-images.githubusercontent.com/77920592/194063659-bbc43497-6d8c-4a95-90a3-17ca84bb60a8.png)
![image](https://user-images.githubusercontent.com/77920592/194083636-af8159ec-ed26-4cae-bddd-8d7ac92bed75.png)

**Example 1:**

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

### LEAD(x,y) / LAG(x,y) ### 

The y argument is an offset – it defines how many rows we will use (going forward from the current row). 

**Example 1:**

There's a website with Id = 2. Find its statistics between May 1 and May 14, 2016. Show the Day, the number of users, and the number of users seven days later. Name the column Lead.

```sql
select day, users, 
lead(users, 7) over(order by day asc) as lead
from statistic
where day >= '2016-05-01' and day <= '2016-05-14' and 
websiteid = 2
```

![image](https://user-images.githubusercontent.com/77920592/194081089-7d364f42-e074-4938-a982-123375aa7679.png)

### LEAD(x,y,z) / LAG(x,y,z) ### 

The third argument (z) tells the function what it should return if no matching value is found. Default is NULL.

**Example 1:**

Using the previous queries as example and replace NULL with -1. 

```sql
select day, users, 
lead(users, 7, -1) over(order by day asc) as lead
from statistic
where day >= '2016-05-01' and day <= '2016-05-14' and 
websiteid = 2
```

![image](https://user-images.githubusercontent.com/77920592/194081458-a7f3fe11-5aa9-4592-b75c-c5e1251f8ed6.png)


## FIRST_VALUE(x) / LAST_VALUE(x)##

FIRST_VALUE returns the first value in the column x in the given order. 

LAST_VALUE returns the last value in the column x in the given order. 

**Example 1:**

Show the statistics for WebsiteId = 2. For each row, show the Day, the number of users, and the number of users on the first day ever. Name the column FirstUsers.

```sql
select day, users, first_value(users) over(order by day asc) as FirstUsers
from statistic
where websiteid = 2
```

![image](https://user-images.githubusercontent.com/77920592/194084086-8392a779-2641-4b0d-9f99-279c2d1645ae.png)


**Example 2:**

LAST_VALUE works slightly different than FIRST_VALUE.

For example, to find the highest value of opendate:

```sql
select name, opendate,
last_value(opendate) over(order by opendate asc) as lastopendate
from website;
```

![image](https://user-images.githubusercontent.com/77920592/194084733-176ac57a-0292-4d4e-9f12-0fccad5317a2.png)

The result is a bit different from our expectations. LAST_VALUE() shows the current value instead of the highest value.
If there is an ORDER BY clause, RANGE UNBOUNDED PRECEDING will be used as the default window frame.
Therefore, we need to define the right window frame:

```sql
select name, opendate,
last_value(opendate) over(order by opendate asc rows between unbounded preceding and unbounded following) as lastopendate
from website;
```

**Example 3:**

For each row where WebsiteId = 1, show the Day, the number of users, the number of users on the last day and the difference between these two values. Name the columns LastUsers and Difference

```sql
select day, users, 
last_value(users) over(order by day rows between unbounded preceding and unbounded following) as LastUsers,
users - last_value(users) over(order by day rows between unbounded preceding and unbounded following) as Difference
from statistic
where websiteid = 1
```

![image](https://user-images.githubusercontent.com/77920592/194086063-4fd74f90-fe73-43a0-980f-87c9e291015c.png)
