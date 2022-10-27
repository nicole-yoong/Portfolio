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
on visit_id = purchaseid)


select page_name, sum(pageviews) as PageViews, sum(cartsadd) as CartsAdd, 
sum(case when cartsadd = 1 and purchase = 0 then 1 else 0
	end) as CartsAddNotPurchase,
sum(case when cartsadd = 1 and purchase = 1 then 1 else 0
	end) as CartsAddPurchase
from cte3
group by page_name
```
![image](https://user-images.githubusercontent.com/77920592/198271139-904b1a83-9938-4182-96c1-afc970cc54c2.png)

Additionally, create another table which further aggregates the data for the above points but this time for each product category instead of individual products.

Use your 2 new output tables - answer the following questions:

Which product had the most views, cart adds and purchases?

Which product was most likely to be abandoned?

Which product had the highest view to purchase percentage?

What is the average conversion rate from view to cart add?

What is the average conversion rate from cart add to purchase?

## C. Campaigns Analysis ##

Generate a table that has 1 single row for every unique visit_id record and has the following columns:

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
Use the subsequent dataset to generate at least 5 insights for the Clique Bait team - bonus: prepare a single A4 infographic that the team can use for their management reporting sessions, be sure to emphasise the most important points from your findings.

Some ideas you might want to investigate further include:

- Identifying users who have received impressions during each campaign period and comparing each metric with other users who did not have an impression event
- Does clicking on an impression lead to higher purchase rates?
- What is the uplift in purchase rate when comparing users who click on a campaign impression versus users who do not receive an impression? What if we compare them with users who just an impression but do not click?
- What metrics can you use to quantify the success or failure of each campaign compared to eachother?
