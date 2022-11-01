# Case Study #3 - Foodie-Fi #

![image](https://user-images.githubusercontent.com/77920592/199336231-409a6332-05f4-4253-8139-5e1e327b205d.png)

# Introduction #
 
Subscription based businesses are super popular and Danny realised that there was a large gap in the market – he wanted to create a new streaming service that only had food related content – something like Netflix but with only cooking shows!
Danny finds a few smart friends to launch his new startup Foodie-Fi in 2020 and started selling monthly and annual subscriptions, giving their customers unlimited on-demand access to exclusive food videos from around the world!
Danny created Foodie-Fi with a data driven mindset and wanted to ensure all future investment decisions and new features were decided using data. This case study focuses on using subscription style digital data to answer important business questions.

# Available Data #

Danny has shared the data design for Foodie-Fi and also short descriptions on each of the database tables – our case study focuses on only 2 tables but there will be a challenge to create a new table for the Foodie-Fi team.
All datasets exist within the foodie_fi database schema – be sure to include this reference within your SQL scripts as you start exploring the data and answering the case study questions.

**Table 1: plans**

Customers can choose which plans to join Foodie-Fi when they first sign up.
Basic plan customers have limited access and can only stream their videos and is only available monthly at $9.90
Pro plan customers have no watch time limits and are able to download videos for offline viewing. Pro plans start at $19.90 a month or $199 for an annual subscription.
Customers can sign up to an initial 7 day free trial will automatically continue with the pro monthly subscription plan unless they cancel, downgrade to basic or upgrade to an annual pro plan at any point during the trial.
When customers cancel their Foodie-Fi service – they will have a churn plan record with a null price but their plan will continue until the end of the billing period.

![image](https://user-images.githubusercontent.com/77920592/192091081-c32b48c4-a6bf-40be-9e61-e1824f719e3d.png)

**Table 2: subscriptions**

Customer subscriptions show the exact date where their specific plan_id starts.
If customers downgrade from a pro plan or cancel their subscription – the higher plan will remain in place until the period is over – the start_date in the subscriptions table will reflect the date that the actual plan changes.
When customers upgrade their account from a basic plan to a pro or annual pro plan – the higher plan will take effect straightaway.
When customers churn – they will keep their access until the end of their current billing period but the start_date will be technically the day they decided to cancel their service.

![image](https://user-images.githubusercontent.com/77920592/192091102-0255bb8c-1f7f-41e6-9047-be0c4c6d3e75.png)

# SQL Schema #
*Please refer to the Schema file in the folder.*

# Case Study Questions #
This case study is split into an initial data understanding question before diving straight into data analysis questions before finishing with 1 single extension challenge.

## B. Data Analysis Questions ##

### 1. How many customers has Foodie-Fi ever had? ###
```sql
select count(distinct customer_id) from subscriptions
```

### 2. What is the monthly distribution of trial plan start_date values for our dataset - use the start of the month as the group by value ###
```sql
select count(plan_id), date_part(‘month’, start_date) as month from subscriptions
where plan_id = 0
group by month
order by month
```

![image](https://user-images.githubusercontent.com/77920592/192091352-2331fbc8-4249-4f32-9904-2c6ab65c648f.png)


### 3. What plan start_date values occur after the year 2020 for our dataset? Show the breakdown by count of events for each plan_name ###
```sql
select count(plan_name), plan_name
from subscriptions s join plans p on s.plan_id = p.plan_id
where start_date > ‘2020-12-31’
group by plan_name
```
![image](https://user-images.githubusercontent.com/77920592/192091363-ba57e74f-24ba-4c6f-8aef-f53600d0ac76.png)

### 4. What is the customer count and percentage of customers who have churned rounded to 1 decimal place? ###
```sql
select count(customer_id) as churn_count,
round (100* count (*)/
(select count(distinct customer_id) from subscriptions),1) as pect_churn
from subscriptions
where plan_id = 4
```
![image](https://user-images.githubusercontent.com/77920592/192091372-e411a545-f64f-41e1-a757-e8074625870a.png)


### 5. How many customers have churned straight after their initial free trial - what percentage is this rounded to the nearest whole number? ###
```sql
with rank_cte as
(
select *, dense_rank() over (partition by customer_id order by plan_id) as plan_rank
from subscriptions
)

select count(customer_id) as churn_count,
round (100* count (*)/
(select count(distinct customer_id) from subscriptions),0) as pect_churn
from rank_cte
where plan_id = 4 and plan_rank = 2
```
![image](https://user-images.githubusercontent.com/77920592/192091378-0f0ba71c-1db0-46cf-8e0f-4d2e700d249b.png)


### 6. What is the number and percentage of customer plans after their initial free trial? ###
```sql
with plan_cte as
(
select *, lead(plan_id, 1) over (partition by customer_id order by plan_id) as plan_new
from subscriptions
)

select plan_new, count(*) as conversions,
round (100* count (*)/
(select count(distinct customer_id) from subscriptions),1) as pect_conversion
from plan_cte
where plan_new is not null and plan_id = 0
group by plan_new
order by plan_new
```
![image](https://user-images.githubusercontent.com/77920592/192091386-bc0934ee-9eea-4703-9866-4f746f0095b9.png)


### 7. What is the customer count and percentage breakdown of all 5 plan_name values at 2020-12-31? ###
```sql
with next_plan as(
select
customer_id,
plan_id,
start_date,
lead(start_date, 1) over(partition by customer_id order by start_date) as next_date
from foodie_fi.subscriptions
where start_date <= ‘2020-12-31’
),
customer_breakdown as (
select
plan_id,
count(distinct customer_id) as customers
from next_plan
where
(next_date is not null and (start_date < ‘2020-12-31’
and next_date > ‘2020-12-31’))
or (next_date is null and start_date < ‘2020-12-31’)
group by plan_id
)

select plan_id, customers,
round(100 * customers::numeric / (
select count(distinct customer_id)
from foodie_fi.subscriptions),1) as percentage
from customer_breakdown
group by plan_id, customers
order by plan_id;
```
![image](https://user-images.githubusercontent.com/77920592/192091401-41ed8d3a-eb5b-4b84-b817-f1a39fb86271.png)


### 8. How many customers have upgraded to an annual plan in 2020? ###
```sql
select count(distinct customer_id) from subscriptions
where plan_id = 3 and
start_date <= ‘2020-12-31’
```
![image](https://user-images.githubusercontent.com/77920592/192091407-fb5e0c8c-d59e-43f3-98d6-6f4acdd8f238.png)


### 9. How many days on average does it take for a customer to an annual plan from the day they join Foodie-Fi? ###
```sql
with trial_date_cte as
(
select customer_id, start_date as trial_date
from subscriptions
where plan_id = 0
),
annual_date_cte as
(
select customer_id, start_date as annual_date
from subscriptions
where plan_id = 3
)

select round(avg(annual_date – trial_date),0) as avg_days
from trial_date_cte td join annual_date_cte ad
on td.customer_id = ad.customer_id;
```
![image](https://user-images.githubusercontent.com/77920592/192091423-d262bdb0-2e4f-46c1-aeec-08ad09556855.png)


### 10. Can you further breakdown this average value into 30 day periods (i.e. 0-30 days, 31-60 days etc) ###
```sql
with trial_date_cte as
(
select customer_id, start_date as trial_date
from subscriptions
where plan_id = 0
),
annual_date_cte as
(
select customer_id, start_date as annual_date
from subscriptions
where plan_id = 3
),
interval_cte as
(
select width_bucket(ad.annual_date – td.trial_date, 0, 360, 12) as avg_days
from trial_date_cte td join annual_date_cte ad
on td.customer_id = ad.customer_id
)
select ((avg_days – 1) * 30 || ‘ – ‘ ||
(avg_days) * 30) || ‘ days’ as breakdown,
count(*) as customers
from interval_cte
group by avg_days
order by avg_days
```
![image](https://user-images.githubusercontent.com/77920592/192091427-4536faeb-43e7-46e8-ac89-c64a4fb455f0.png)


### 11. How many customers downgraded from a pro monthly to a basic monthly plan in 2020? ###
```sql
with downgrade_cte as
(
select *, lead(plan_id, 1) over (partition by customer_id order by plan_id) as plan_new
from subscriptions
)

select count(plan_new)
from downgrade_cte
where plan_new is not null and
plan_id = 2 and plan_new = 1 and —current plan is 2, new plan is 1
start_date < ‘2020-12-31’
```
![image](https://user-images.githubusercontent.com/77920592/192091429-a46da952-e070-4896-badd-8e0af216c2c7.png)

