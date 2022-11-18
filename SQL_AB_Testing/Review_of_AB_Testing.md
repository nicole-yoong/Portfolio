# Review of A/B Testing on SQL #

For a lot of e-commerce, subscription or internet companies, A/B testing is one of the approaches to compare two versions using metrics like conversion rates. 
In this review, multiple case studies in regards to A/B Testing are performed to understand its application. 

## Case Study #1 ##
Data Mart is an online supermarket that specialises in fresh produce. 
In June 2020 - large scale supply changes were made at Data Mart. All Data Mart products now use sustainable packaging methods in every single step from the farm all the way to the customer.
We want to quantify the impact of this change on the sales performance for Data Mart by performing an A/B Testing to answer the following questions:
- What was the quantifiable impact of the changes introduced in June 2020?
- Which platform, region, segment and customer types were the most impacted by this change?

Dataset can be found here. 

Taking the week_date value of 2020-06-15 as the baseline week where the Data Mart sustainable packaging changes came into effect. We would include all week_date values for 2020-06-15 as the start of the period after the change and the previous week_date values would be before.

### What is the total sales for the 4 weeks before and after 2020-06-15? What is the growth or reduction rate in actual values and percentage of sales? ### 
```sql
select distinct(dateadd(week, -4, '2020-06-15')) as Date_Before, 
(dateadd(week, 4, '2020-06-15')) as Date_After
from #clean_weekly_sales;

with cte as
(
select week_date, sum(sales) as Total_Sales
from #clean_weekly_sales
where week_date <= '2020-07-13' and week_date >= '2020-05-18'
group by week_date
),
cte2 as
(
select 
sum(case when week_date <= '2020-06-15' then total_sales end) as Sales_Before, 
sum(case when week_date >= '2020-06-15' then total_sales end) as Sales_After
from cte
)
select sales_before, sales_after, sales_after - sales_before as Figure_Differences,
((sales_after - sales_before) * 100.0 / sales_before) as Percentage_Differences
from cte2
```
![image](https://user-images.githubusercontent.com/77920592/197381043-69aac7b2-e2ed-434b-8071-3dec7ea8b50d.png)

The sales dropped $158838 at a negative of 0.102%, meaning that customers may not recognize the packaging changes, or they were not buying in to the changes yet!

### What about the entire 12 weeks before and after? ### 
```sql
select distinct(dateadd(week, -12, '2020-06-15')) as Date_Before, 
(dateadd(week, 12, '2020-06-15')) as Date_After
from #clean_weekly_sales;

with cte as
(
select week_date, sum(sales) as Total_Sales
from #clean_weekly_sales
where week_date <= '2020-09-07' and week_date >= '2020-03-23'
group by week_date
),
cte2 as
(
select 
sum(case when week_date <= '2020-06-15' then total_sales end) as Sales_Before, 
sum(case when week_date >= '2020-06-15' then total_sales end) as Sales_After
from cte
)
select sales_before, sales_after, sales_after - sales_before as Figure_Differences,
((sales_after - sales_before) * 100.0 / sales_before) as Percentage_Differences
from cte2
```

The sales has dropped even more to  a negative 8.96%! 

### How do the sale metrics for these 2 periods before and after compare with the previous years in 2018 and 2019? ###

We can use another approach, using the week number to compare the changes. 

```sql
select distinct week_number
from #clean_weekly_sales
where week_date = '2020-06-15'  and calender_year = '2020';
  
with cte as
(
select calender_year, week_number, sum(sales) as Total_Sales
from #clean_weekly_sales
where week_number between 21 and 28
group by calender_year, week_number
),
cte2 as
(
select calender_year, 
sum(case when week_number between 21 and 24 then total_sales end) as Sales_Before, 
sum(case when week_number between 25 and 28 then total_sales end) as Sales_After
from cte
group by calender_year
)
select calender_year, sales_before, sales_after, sales_after - sales_before as Figure_Differences,
((sales_after - sales_before) * 100.0 / sales_before) as Percentage_Differences
from cte2;
```
![image](https://user-images.githubusercontent.com/77920592/197381957-5c6bf039-ed18-4c98-8029-71f960a4c210.png)

Consistent sales increase can be observed in year 2018 and 2019, but not after the new packaging was introduced in 2020 where the sales dropped by around 0.20%
