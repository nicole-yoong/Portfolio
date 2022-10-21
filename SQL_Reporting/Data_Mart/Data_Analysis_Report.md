# Introduction #

Data Mart is Danny’s latest venture and after running international operations for his online supermarket that specialises in fresh produce - Danny is asking for your support to analyse his sales performance.

In June 2020 - large scale supply changes were made at Data Mart. All Data Mart products now use sustainable packaging methods in every single step from the farm all the way to the customer.

Danny needs your help to quantify the impact of this change on the sales performance for Data Mart and it’s separate business areas.

The key business question he wants you to help him answer are the following:

- What was the quantifiable impact of the changes introduced in June 2020?
- Which platform, region, segment and customer types were the most impacted by this change?
- What can we do about future introduction of similar sustainability updates to the business to minimise impact on sales?

# Case Study Questions #

The following case study questions require some data cleaning steps before we start to unpack Danny’s key business questions in more depth.

## Data Cleansing Steps ##

In a single query, perform the following operations and generate a new table in the data_mart schema named clean_weekly_sales:
Convert the week_date to a DATE format
- Add a week_number as the second column for each week_date value, for example any value from the 1st of January to 7th of January will be 1, 8th to 14th will be 2 etc
- Add a month_number with the calendar month for each week_date value as the 3rd column
- Add a calendar_year column as the 4th column containing either 2018, 2019 or 2020 values
- Add a new column called age_band after the original segment column using the following mapping on the number inside the segment value
![image](https://user-images.githubusercontent.com/77920592/197146879-5ce829a3-9815-47d7-bb31-89d5445ff90d.png)
- Add a new demographic column using the following mapping for the first letter in the segment values:
![image](https://user-images.githubusercontent.com/77920592/197146980-44f0d86a-1d23-4220-b907-44160eea9027.png)
- Ensure all null string values with an "unknown" string value in the original segment column as well as the new age_band and demographic columns

```sql
create table #clean_weekly_sales
(
week_date date,
week_number int,
month_number int,
calender_year int,
region varchar(50),
platform varchar(50),
segment varchar(50),
age_band varchar(50),
demographic varchar(50),
transactions int,
sales int
)

with cte as
(
select 
convert(datetime, week_date, 5) as week_date,
datepart(day, convert(datetime, week_date, 5)) as  week_number,
datepart(month, convert(datetime, week_date, 5)) as  month_number,
datepart(year, convert(datetime, week_date, 5)) as  calender_year, 
region, platform, segment, 
case 
when right (segment,1) = '1' then 'Young Adults'
when right (segment,1) = '2' then 'Middle Aged'
when right (segment,1) in ('3','4') then 'Retirees'
else 'Unknown' end as age_band,
case
when left(segment, 1) = 'C' then 'Couples'
when left(segment, 1) = 'F' then 'Families'
else 'Unknown' end as demographic, 
sales, transactions from weekly_sales
)
insert into #clean_weekly_sales
(
week_date, week_number, month_number, calender_year, region,
platform, segment, age_band, demographic, transactions, sales
)
select * from cte;
```

## Data Exploration ##

### What day of the week is used for each week_date value? ###
```sql
select distinct (datename(dw, week_date)) as Day_name 
from #clean_weekly_sales
```
![image](https://user-images.githubusercontent.com/77920592/197158230-0cdb1f74-5b8c-49c3-8902-75cdaa3257b6.png)

### What range of week numbers are missing from the dataset? ###
```sql
with counter(current_value) as
(
select 1 union all select current_value + 1
from counter
where current_value < 53
)

select distinct(c.current_value) from counter c
left outer join #clean_weekly_sales ws 
on c.current_value = ws.week_number
where ws.week_number is null
```
![image](https://user-images.githubusercontent.com/77920592/197161603-ddc9cf63-9ed8-43b8-a1a6-658ddbc092ee.png)

### How many total transactions were there for each year in the dataset? ###
```sql
select datepart(year, week_date) as Year, count(transactions) as Count
from #clean_weekly_sales
group by datepart(year, week_date) 
```
![image](https://user-images.githubusercontent.com/77920592/197176544-b315c8f0-e41e-42ed-95db-cff9e310a95a.png)

### What is the total sales for each region for each month? ###
```sql
select region, datepart(month, week_date) as Month, sum(sales) as TotalSales 
from #clean_weekly_sales
group by region, datepart(month, week_date)
order by region, datepart(month, week_date) asc
```
![image](https://user-images.githubusercontent.com/77920592/197176465-3c7bc2d2-e139-46b1-af07-5e1b9b789a94.png)

### What is the total count of transactions for each platform ###
```sql
select platform, sum(cast(transactions as bigint)) as Count
from #clean_weekly_sales
group by platform
```
![image](https://user-images.githubusercontent.com/77920592/197176389-d71ce8d9-9e1a-438c-9101-d0cc9899f2a0.png)

### What is the percentage of sales for Retail vs Shopify for each month? ### 
```sql
with cte as
(
select platform, datepart(year, week_date) as Year,
datepart(month, week_date) as Month,
sum(sales) as Total_Sales
from #clean_weekly_sales
group by platform, datepart(year, week_date), datepart(month, week_date)
),
cte2 as
(
select platform, year, month, total_sales, 
sum(total_sales) over(partition by year, month) as Total_Monthly_Sales
from cte
)
select platform, year, month, total_sales, total_monthly_sales,
round((total_sales * 100.0 / total_monthly_sales),2) as Percentage
from cte2
```
![image](https://user-images.githubusercontent.com/77920592/197175972-54dbae75-8312-4971-bfa7-05b99ec47491.png)

### What is the percentage of sales by demographic for each year in the dataset? ###
```sql
with cte as
(
select demographic, datepart(year, week_date) as Year,
sum(sales) as Total_Sales
from #clean_weekly_sales
group by demographic, datepart(year, week_date)
),
cte2 as
(
select demographic, year, total_sales, 
sum(total_sales) over(partition by year) as Total_Yearly_Sales
from cte
)
select demographic, year, total_sales, total_yearly_sales,
round((total_sales * 100.0 / total_yearly_sales),2) as Percentage
from cte2
```
![image](https://user-images.githubusercontent.com/77920592/197175905-58475efe-6c2c-4b39-8041-58c937fd3ebb.png)

### Which age_band and demographic values contribute the most to Retail sales? ###
```sql
with cte as
(
select age_band, demographic, sum(sales) as Total_Sales
from #clean_weekly_sales
where platform = 'retail'
group by age_band, demographic
)
select age_band, demographic, total_sales,
round(total_sales * 100.0 / (select sum(sales) from #clean_weekly_sales
				where platform = 'retail'),2) as Percentage 
from cte
order by total_sales desc
```
![image](https://user-images.githubusercontent.com/77920592/197175845-48216cce-3900-47d2-b7f1-60ca64c4edfb.png)

### Find the average transaction size for each year for Retail vs Shopify ###
```sql
with cte as
(
select platform, datepart(year, week_date) as Year, sum(sales) as Total_Sales, 
sum(cast(transactions as bigint)) as Total_Transactions
from #clean_weekly_sales
group by platform, datepart(year, week_date)
)
select platform, year, total_sales, total_transactions, 
round(avg(total_sales * 100.0/ total_transactions),2) as Avg_Transaction_Size
from cte
group by platform, year, total_sales, total_transactions
order by year 
```
![image](https://user-images.githubusercontent.com/77920592/197175785-cfcb5cc9-d2e5-4940-a333-e4e0cd5448bd.png)

## Before & After Analysis ##

Taking the week_date value of 2020-06-15 as the baseline week where the Data Mart sustainable packaging changes came into effect.
We would include all week_date values for 2020-06-15 as the start of the period after the change and the previous week_date values would be before.

### What is the total sales for the 4 weeks before and after 2020-06-15? What is the growth or reduction rate in actual values and percentage of sales? ### 


### What about the entire 12 weeks before and after? ### 
### How do the sale metrics for these 2 periods before and after compare with the previous years in 2018 and 2019? ### 
