# Case Study #6 - Clique Bait #

![image](https://user-images.githubusercontent.com/77920592/199336817-b98b58f0-9142-427f-97ba-0faa30926224.png)

# Introduction #

Clique Bait is not like your regular online seafood store - the founder and CEO Danny, was also a part of a digital data analytics team and wanted to expand his knowledge into the seafood industry!

In this case study - you are required to support Danny’s vision and analyse his dataset and come up with creative solutions to calculate funnel fallout rates for the Clique Bait online store.

## A. Digital Analysis ##

### How many users are there? ###
```sql
select count(distinct user_id) as Count from users
```
![image](https://user-images.githubusercontent.com/77920592/198260869-b185a4c1-52c0-41a0-addc-ef59452e977a.png)

### How many cookies does each user have on average? ###
```sql
with cte as
(
select count(distinct user_id) as CountUser,
count(cookie_id) as CountCookie
from users)
select round((countcookie / countuser),0) as AvgCookie from cte
```
![image](https://user-images.githubusercontent.com/77920592/198260944-a8404f58-49ae-41bc-beec-712a18bd2149.png)

### What is the unique number of visits by all users per month? ###
```sql
select datepart(month, event_time) as month,
count (distinct visit_id) as Count from events
group by datepart(month, event_time)
order by datepart(month, event_time)
```
![image](https://user-images.githubusercontent.com/77920592/198261259-132601cb-9300-40e8-b8e0-f2fad038f7fb.png)

### What is the number of events for each event type? ###
```sql
select e.event_type, ei.event_name, count(*) as Count from events e 
join event_identifier ei on e.event_type = ei.event_type
group by e.event_type, ei.event_name
order by e.event_type
```
![image](https://user-images.githubusercontent.com/77920592/198261315-02576abd-124f-44bc-af75-f8e48e3a26de.png)

### What is the percentage of visits which have a purchase event? ###
```sql
select 
round(count(distinct visit_id)*100.0/(select count(distinct visit_id) from events),2) as percentage
from events e 
join event_identifier ei on e.event_type = ei.event_type
where e.event_type = 3
```
![image](https://user-images.githubusercontent.com/77920592/198261415-3c14f919-4b59-4543-b2f7-768caec82fc2.png)

### What is the percentage of visits which view the checkout page but do not have a purchase event? ###
```sql
with cte as
(
select visit_id,
max(case when event_type <> 3 and page_id = 12 then 1 else 0 end) as checkout,
max(case when event_type = 3 then 1 else 0 end) as purchase
from events
group by visit_id
)
select sum(checkout) as Sum_checkout, sum(purchase) as Sum_purchase,
1 - (sum(purchase)*1.0/sum(checkout)) as Percentage
from cte
```
![image](https://user-images.githubusercontent.com/77920592/198261639-de9ae7cd-707b-497b-95de-6e67777bb096.png)

### What are the top 3 pages by number of views? ###
```sql
select top 3 e.page_id, page_name, count(*) as Count
from events e join page_hierarchy ph
on e.page_id = ph.page_id
group by e.page_id, page_name
order by count(*) desc 
```
![image](https://user-images.githubusercontent.com/77920592/198261714-68c5b154-a636-4945-91c1-fddf478281ed.png)

### What is the number of views and cart adds for each product category? ###
```sql
select ph.product_category, 
sum(case when event_type = 1 then 1 else 0 end) as NumberofViews,
sum(case when event_type = 2 then 1 else 0 end) as CartAdds
from events e join page_hierarchy ph
on e.page_id = ph.page_id
where product_category <> 'null'
group by ph.product_category
```
![image](https://user-images.githubusercontent.com/77920592/198261797-7dc99c66-091c-4d6e-8474-825141f07c96.png)

## B. Product Funnel Analysis ##

### Using a single SQL query - create a new output table which has the following details: ###

How many times was each product viewed?

How many times was each product added to cart?

How many times was each product added to a cart but not purchased (abandoned)?

How many times was each product purchased?

```sql
create table #individual_pf
(
page_name varchar(50),
pageviews int,
cartsadd int,
cartsaddnotpurchase int,
cartsaddpurchase int
)

with cte as(
select e.visit_id, page_name,
sum(case when event_type = 1 then 1 else 0 end) as PageViews,
sum(case when event_type = 2 then 1 else 0 end) as CartsAdd
from events e join page_hierarchy ph
on e.page_id = ph.page_id
where product_category is not null
group by e.visit_id, page_name),

cte2 as(
select distinct(visit_id) as Purchaseid
from events where event_type = 3),

cte3 as(
select *, 
(case when purchaseid is not null then 1 else 0 end) as Purchase
from cte left join cte2
on visit_id = purchaseid),

cte4 as(
select page_name, sum(pageviews) as PageViews, sum(cartsadd) as CartsAdd, 
sum(case when cartsadd = 1 and purchase = 0 then 1 else 0
	end) as CartsAddNotPurchase,
sum(case when cartsadd = 1 and purchase = 1 then 1 else 0
	end) as CartsAddPurchase
from cte3
group by page_name)

insert into #individual_pf (page_name, pageviews, cartsadd, cartsaddnotpurchase, cartsaddpurchase)
select page_name, pageviews, cartsadd, cartsaddnotpurchase, cartsaddpurchase
from cte4

select * from #individual_pf
```
![image](https://user-images.githubusercontent.com/77920592/198271139-904b1a83-9938-4182-96c1-afc970cc54c2.png)

### Additionally, create another table which further aggregates the data for the above points but this time for each product category instead of individual products. ###
```sql
create table #category_pf
(
product_category varchar(50),
pageviews int,
cartsadd int,
cartsaddnotpurchase int,
cartsaddpurchase int
)

with cte as(
select e.visit_id, page_name, product_category,
sum(case when event_type = 1 then 1 else 0 end) as PageViews,
sum(case when event_type = 2 then 1 else 0 end) as CartsAdd
from events e join page_hierarchy ph
on e.page_id = ph.page_id
where product_category is not null
group by e.visit_id, product_category, page_name),

cte2 as(
select distinct(visit_id) as Purchaseid
from events where event_type = 3),

cte3 as(
select *, 
(case when purchaseid is not null then 1 else 0 end) as Purchase
from cte left join cte2
on visit_id = purchaseid),

cte4 as(
select product_category, sum(pageviews) as PageViews, sum(cartsadd) as CartsAdd, 
sum(case when cartsadd = 1 and purchase = 0 then 1 else 0
	end) as CartsAddNotPurchase,
sum(case when cartsadd = 1 and purchase = 1 then 1 else 0
	end) as CartsAddPurchase
from cte3
group by product_category)

insert into #category_pf (product_category, pageviews, cartsadd, cartsaddnotpurchase, cartsaddpurchase)
select product_category, pageviews, cartsadd, cartsaddnotpurchase, cartsaddpurchase
from cte4

select * from #category_pf
```
![image](https://user-images.githubusercontent.com/77920592/198273216-d09d07e9-fe45-4cef-a12c-00d461a7581e.png)

Use your 2 new output tables - answer the following questions:

### Which product had the most views, cart adds and purchases? ###

Most views: Oyster

Most cart adds: Lobster

Most purchases: Lobster

### Which product was most likely to be abandoned? ###
Russian Caviar

### Which product had the highest view to purchase percentage? ###
```sql
select page_name, round(cartsaddpurchase * 100.0/pageviews,2) as ViewtoPurchase
from #individual_pf
order by round(cartsaddpurchase * 100.0/pageviews,2) desc
```
![image](https://user-images.githubusercontent.com/77920592/198313810-c8d48261-5a5c-4503-aa84-ac7a03706a73.png)

### What is the average conversion rate from view to cart add? ###
```sql
select avg(round(cartsadd * 100.0/ pageviews,2)) as ConversionRate
from #individual_pf
```
![image](https://user-images.githubusercontent.com/77920592/198313897-849c7335-fed4-4530-b888-a839405b56d3.png)

### What is the average conversion rate from cart add to purchase? ###
```sql
select avg(round(cartsaddpurchase * 100.0/ cartsadd,2)) as ConversionRate
from #individual_pf
```
![image](https://user-images.githubusercontent.com/77920592/198313979-023d3350-e30b-49a0-b2d7-27c46ab9cabf.png)

## C. Campaigns Analysis ##

### Generate a table that has 1 single row for every unique visit_id record and has the following columns: ###

- user_id
- visit_id
- visit_start_time: the earliest event_time for each visit
- page_views: count of page views for each visit
- cart_adds: count of product cart add events for each visit
- purchase: 1/0 flag if a purchase event exists for each visit
- campaign_name: map the visit to a campaign if the visit_start_time falls between the start_date and end_date
- impression: count of ad impressions for each visit
- click: count of ad clicks for each visit
- (Optional column) cart_products: a comma separated text value with products added to the cart sorted by the order they were added to the cart (hint: use the sequence_number)

```sql
create table campaign_analysis
(
user_id int,
visit_id varchar(20),
start_time datetime2(3),
page_views int,
cart_adds int,
purchase int,
impressions int, 
click int, 
Campaign varchar(200),
cart_products varchar(200)
);

with cte as
(
select distinct user_id, visit_id, min(event_time) as start_time,
sum(case when event_type = 1 then 1 else 0 end) as page_views,
sum(case when event_type = 2 then 1 else 0 end) as cart_adds,
sum(case when event_type = 3 then 1 else 0 end) as purchase,
sum(case when event_type = 4 then 1 else 0 end) as impressions,
sum(case when event_type = 5 then 1 else 0 end) as click,
case
when min(event_time) > '2020-01-01 00:00:00' and min(event_time) < '2020-01-14 00:00:00'
		then 'BOGOF - Fishing For Compliments'
when min(event_time) > '2020-01-15 00:00:00' and min(event_time) < '2020-01-28 00:00:00'
		then '25% Off - Living The Lux Life'
when min(event_time) > '2020-02-01 00:00:00' and min(event_time) < '2020-03-31 00:00:00'
		then 'Half Off - Treat Your Shellf(ish)' 
else NULL
end as Campaign,
string_agg(case when product_id IS NOT NULL AND event_type = 2 
			then page_name ELSE NULL END, ', ') AS cart_products
from events e join users u on e.cookie_id = u.cookie_id
join page_hierarchy ph on e.page_id = ph.page_id
group by visit_id, user_id
)

insert into campaign_analysis 
(user_id, visit_id, start_time, page_views, cart_adds, purchase, impressions, click, Campaign, cart_products)
select user_id, visit_id, start_time, page_views, cart_adds, purchase, impressions, click, Campaign, cart_products
from cte;

select * from campaign_analysis
```

![image](https://user-images.githubusercontent.com/77920592/198987379-19f9de53-5708-4500-9a0e-79f3ff0b3dd8.png)

### What is the percentage of each campaign being participated? ###
```sql
select campaign, count(*) as count,
round(count(*)*100.0/(select count(*) from campaign_analysis),2) as Percentage
from campaign_analysis
group by campaign
```

![image](https://user-images.githubusercontent.com/77920592/201328154-2612e386-5b56-4cc4-9b14-a7bbe6f86e99.png)
