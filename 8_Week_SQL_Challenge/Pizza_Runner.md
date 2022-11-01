# Case Study #2 - Pizza Runner #

![image](https://user-images.githubusercontent.com/77920592/199072945-1bdf34ab-bc60-49eb-bcf9-0f21fb9dbe5d.png)

# Introduction #

Did you know that over 115 million kilograms of pizza is consumed daily worldwide??? (Well according to Wikipedia anyway…)

Danny was scrolling through his Instagram feed when something really caught his eye - “80s Retro Styling and Pizza Is The Future!”

Danny was sold on the idea, but he knew that pizza alone was not going to help him get seed funding to expand his new Pizza Empire - so he had one more genius idea to combine with it - he was going to Uberize it - and so Pizza Runner was launched!

Danny started by recruiting “runners” to deliver fresh pizza from Pizza Runner Headquarters (otherwise known as Danny’s house) and also maxed out his credit card to pay freelance developers to build a mobile app to accept orders from customers.

# Case Study Questions #

This case study has LOTS of questions - they are broken up by area of focus including:

- Pizza Metrics
- Runner and Customer Experience
- Ingredient Optimisation
- Pricing and Ratings
- Bonus DML Challenges (DML = Data Manipulation Language)

Each of the following case study questions can be answered using a single SQL statement.

Again, there are many questions in this case study - please feel free to pick and choose which ones you’d like to try!

Before you start writing your SQL queries however - you might want to investigate the data, you may want to do something with some of those null values and data types in the customer_orders and runner_orders tables!

## Data Cleaning ##
```sql
--- customer orders table 
select order_id, customer_id, pizza_id, 
case when exclusions = '' or exclusions = 'null' 
	 then null else exclusions end as exclusions,
case when extras = '' or extras = 'null' 
	 then null else extras end as extras, 
order_time
into #customer_orders 
from customer_orders;
```
![image](https://user-images.githubusercontent.com/77920592/199332337-848e02d3-4040-48ff-bfa5-dafcc13ad422.png)

```sql
--- runner orders table
alter table runner_orders
alter column pickup_time datetime2(3)

select order_id, runner_id, pickup_time,
case when distance = 'null' then null
	 when distance like '%km' then trim('km' from distance)
else distance end as distance,
case when duration = 'null' then null
	 when duration like '%mins' then trim('mins' from duration)
	 when duration like '%minute' then trim('minute' from duration)
	 when duration like '%minutes' then trim('minutes' from duration)
else duration end as duration, 
case when cancellation = '' or cancellation = 'null' 
	 then null 
else cancellation end as cancellation
into #runner_orders
from runner_orders;

alter table #runner_orders
alter column distance float;

alter table #runner_orders
alter column duration integer;
```
![image](https://user-images.githubusercontent.com/77920592/199332426-94631448-5e9d-4f91-a444-66159942d0b8.png)

```sql
--- pizza_recipes table
alter table pizza_recipes
alter column toppings varchar(25);

create table #pizza_recipes
(
pizza_id int,
topping_id int
);

insert into #pizza_recipes (pizza_id, topping_id)
select pizza_id, value 
from pizza_recipes 
cross apply string_split(toppings, ',') as toppings
```
![image](https://user-images.githubusercontent.com/77920592/199332542-4421710b-bf16-4706-a820-b634da3c477d.png)

## A. Pizza Metrics ##

### How many pizzas were ordered? ###
```sql
select count(pizza_id) as Count 
from #customer_orders;
```
![image](https://user-images.githubusercontent.com/77920592/199332758-53e55838-2341-47e9-9221-0975a5c9e05f.png)

### How many unique customer orders were made? ###
```sql
select count(distinct order_id) as Count 
from #customer_orders;
```
![image](https://user-images.githubusercontent.com/77920592/199332807-9c7d6111-3653-4991-bed2-374edaafb596.png)

### How many successful orders were delivered by each runner? ###
```sql
select runner_id, count(order_id) as successful_orders
from #runner_orders where cancellation is null
group by runner_id
```
![image](https://user-images.githubusercontent.com/77920592/199332860-e4a4708c-8cd7-482c-b04e-148a3a420cab.png)

### How many of each type of pizza was delivered? ###
```sql
select pizza_id, count(pizza_id) as Count
from #customer_orders co join #runner_orders ro
on co.order_id = ro.order_id
where ro.cancellation is null
group by pizza_id
```
![image](https://user-images.githubusercontent.com/77920592/199332905-f0fc274d-394b-4dbb-aa0e-18553adf77e2.png)

### How many Vegetarian and Meatlovers were ordered by each customer? ###
```sql
select customer_id, pizza_id, count(pizza_id) as Count
from #customer_orders
group by customer_id, pizza_id
order by customer_id
```
![image](https://user-images.githubusercontent.com/77920592/199332958-6569108f-fab9-457d-8c6b-d90e7cf1c1aa.png)

### What was the maximum number of pizzas delivered in a single order? ###
```sql
select count(pizza_id) as Count
from #customer_orders
group by order_id
order by count desc;
```
![image](https://user-images.githubusercontent.com/77920592/199333027-6af6ae8a-2e7a-446d-a688-047b08cca32b.png)

### For each customer, how many delivered pizzas had at least 1 change and how many had no changes? ###
```sql
select customer_id, count(pizza_id) as total_pizza, 
sum (case when exclusions is null and extras is not null 
or exclusions is not null and extras is null  
or exclusions is not null and extras is not null then 1 else 0 end) as at_least_1_change,
sum (case when exclusions is null and extras is null then 1 else 0 end) as no_changes
from #customer_orders co join #runner_orders ro
on co.order_id = ro.order_id
where ro.cancellation is null
group by customer_id
```
![image](https://user-images.githubusercontent.com/77920592/199333080-5a981478-da8a-4b22-8093-b25356e3247c.png)

### How many pizzas were delivered that had both exclusions and extras? ###
```sql
select 
sum (case when exclusions is not null and extras is not null then 1 else 0 end) as both_changes
from #customer_orders co join #runner_orders ro
on co.order_id = ro.order_id
where ro.cancellation is null
```
![image](https://user-images.githubusercontent.com/77920592/199333130-50d77cce-bcfe-4161-91dc-93dbcaa8d85a.png)

### What was the total volume of pizzas ordered for each hour of the day? ###
```sql
select datepart(hour, order_time) as Hour, count(pizza_id) as Count
from #customer_orders
group by datepart(hour, order_time)
```
![image](https://user-images.githubusercontent.com/77920592/199333181-ab181a9a-c887-48b3-8604-43f9e1901d22.png)

### What was the volume of orders for each day of the week? ###
```sql
select datename(weekday, order_time) as Day, count(pizza_id) as Count
from #customer_orders
group by datename(weekday, order_time)
```
![image](https://user-images.githubusercontent.com/77920592/199333231-37acbc94-5f89-4615-a963-5401b4c9d421.png)

## B. Runner and Customer Experience ##

### How many runners signed up for each 1 week period? (i.e. week starts 2021-01-01) ###
```sql
select datepart(week, registration_date) as Week, count(runner_id) as Count
from runners
group by datepart(week, registration_date)
```
![image](https://user-images.githubusercontent.com/77920592/199333311-db8fbda0-9fb4-4db2-bce6-f1260944fb28.png)

### What was the average time in minutes it took for each runner to arrive at the Pizza Runner HQ to pickup the order? ###
```sql
with cte as
(
select co.order_id, 
datediff(minute, order_time, pickup_time) as duration
from #customer_orders co join #runner_orders ro
on co.order_id = ro.order_id
where cancellation is null
group by co.order_id, order_time, pickup_time
)
select avg(duration) as AvgDuration from cte
```
![image](https://user-images.githubusercontent.com/77920592/199333378-3e1376b1-150c-4cf0-ab77-e6045f7f3842.png)

### Is there any relationship between the number of pizzas and how long the order takes to prepare? ###
```sql
with cte as
(
select co.order_id, count(pizza_id) as Count, 
datediff(minute, order_time, pickup_time) as duration
from #customer_orders co join #runner_orders ro
on co.order_id = ro.order_id
where cancellation is null
group by co.order_id, order_time, pickup_time
)
select count, avg(duration) as AvgDuration
from cte 
group by count
```
![image](https://user-images.githubusercontent.com/77920592/199333436-b64ee212-32f6-4c13-a52c-26db091030ec.png)

### What was the average distance travelled for each customer? ###
```sql
select customer_id, sum(distance)/count(co.order_id) as AvgDistance
from #customer_orders co join #runner_orders ro
on co.order_id = ro.order_id
where cancellation is null
group by customer_id
```
![image](https://user-images.githubusercontent.com/77920592/199333511-692ce7a1-16d6-4038-8639-ce0c03d10dd7.png)

### What was the difference between the longest and shortest delivery times for all orders? ###
```sql
select max(duration) - min(duration) as Differences
from #runner_orders
```
![image](https://user-images.githubusercontent.com/77920592/199333575-cdb82ccb-ab52-409a-91ff-d0be6f2fd086.png)

### What was the average speed for each runner for each delivery and do you notice any trend for these values? ###
```sql
with cte as
(
select order_id, runner_id, round((distance/duration*60),2) as Speed
from #runner_orders
)
select runner_id, round(avg(speed),2) as AvgSpeed
from cte
group by runner_id
```
![image](https://user-images.githubusercontent.com/77920592/199333621-c4da978d-1702-4888-bffa-d07140b180c6.png)

### What is the successful delivery percentage for each runner? ###
```sql
select runner_id, 
sum(case when cancellation is null then 1 else 0 end) *100.0 /
					count (*) as Success_rate
from #runner_orders
group by runner_id
```
![image](https://user-images.githubusercontent.com/77920592/199333713-e5599ce6-f7db-4d55-8ce8-694d8b8e4d21.png)

## C. Ingredient Optimisation ##

### What are the standard ingredients for each pizza? ###
```sql
select pizza_id, toppings
from pizza_recipes
```
![image](https://user-images.githubusercontent.com/77920592/199333797-fa9dd035-4073-4dd5-b3c7-ac6bdf69701a.png)

### What was the most commonly added extra? ###
```sql
with cte as
(
select order_id, value 
from #customer_orders 
cross apply string_split(extras, ',') 
)
select value, count(value) as count 
from cte 
group by value
order by count desc
```
![image](https://user-images.githubusercontent.com/77920592/199333852-90145116-6ca0-42b9-b123-acb58a4b3781.png)

### What was the most common exclusion? ###
```sql
with cte as
(
select order_id, value 
from #customer_orders 
cross apply string_split(exclusions, ',') 
)
select value, count(value) as count 
from cte 
group by value
order by count desc
```
![image](https://user-images.githubusercontent.com/77920592/199333904-d5a3f64d-b514-4248-90fa-8b21bdb5f20b.png)

## D. Pricing and Ratings ##
### If a Meat Lovers pizza costs $12 and Vegetarian costs $10 and there were no charges for changes - how much money has Pizza Runner made so far if there are no delivery fees?  ###
```sql
with cte as
(
select co.order_id, pizza_id,
(case when pizza_id = 1 then 12 
		 when pizza_id = 2 then 10 end) as TotalCost
from #customer_orders co join #runner_orders ro
on co.order_id = ro.order_id
where cancellation is null
)
select sum(totalcost) as totalcost
from cte
```
![image](https://user-images.githubusercontent.com/77920592/199333984-5a610a05-eb5b-4f13-b84b-30525b6965b0.png)

### What if there was an additional $1 charge for any pizza extras?  ###
- Add cheese is $1 extra
```sql
declare @basecost int
set @basecost = 138;
select 
@basecost + sum(case when extras like '1%' or extras like '1' then + 1 else 0 end) as TotalCost
from #customer_orders co join #runner_orders ro
on co.order_id = ro.order_id
where cancellation is null
```
![image](https://user-images.githubusercontent.com/77920592/199334572-90d6836a-2976-4b8d-a7f7-c8420a6fd581.png)

### The Pizza Runner team now wants to add an additional ratings system that allows customers to rate their runner, how would you design an additional table for this new dataset - generate a schema for this new table and insert your own data for ratings for each successful customer order between 1 to 5.  ###
```sql
create table #rating_system
(
order_id int,
runner_id int,
rating int
);

insert into #rating_system
values 
(1,1,5), (2,1,4), (3,1,2), (4,2,3), (5,3,5), (7,2,1), (8,2,3), (10,1,4);
```
![image](https://user-images.githubusercontent.com/77920592/199334642-28cfb061-d90a-4c28-97a0-efe86d1fed17.png)

### Using your newly generated table - can you join all of the information together to form a table which has the following information for successful deliveries?  ###
- customer_id
- order_id
- runner_id
- rating
- order_time
- pickup_time
- Time between order and pickup
- Delivery duration
- Average speed
- Total number of pizzas

```sql
select co.customer_id, co.order_id, ro.runner_id, rating, order_time, pickup_time,
datediff(minute, order_time, pickup_time) as pickup_duration,
duration as delivery_duration, 
round((distance/duration*60),2) as speed,
count(pizza_id) as total_pizzas
from #customer_orders co join #runner_orders ro
on co.order_id = ro.order_id
join #rating_system rs on co.order_id = rs.order_id
where cancellation is null
group by co.customer_id, co.order_id, ro.runner_id, rating, 
order_time, pickup_time, duration, distance
```
![image](https://user-images.githubusercontent.com/77920592/199334749-6cfa1e30-7208-468d-932e-86ea3d80e5ea.png)

### If a Meat Lovers pizza was $12 and Vegetarian $10 fixed prices with no cost for extras and each runner is paid $0.30 per kilometre traveled - how much money does Pizza Runner have left over after these deliveries? ###
```sql
declare @basecost int
set @basecost = 138;
select @basecost - 
sum (case when distance is not null then distance*0.30 else null end) as Delivery_Charges
from #runner_orders ro
where cancellation is null
```
![image](https://user-images.githubusercontent.com/77920592/199334822-bb3dd07a-badd-4989-8312-1ea2e628b8e4.png)

