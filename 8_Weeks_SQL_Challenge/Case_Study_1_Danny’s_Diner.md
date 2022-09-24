![image](https://user-images.githubusercontent.com/77920592/192090610-ddc7b214-a946-4317-ade4-7437faf269be.png)

# Introduction #

Danny seriously loves Japanese food so in the beginning of 2021, he decides to embark upon a risky venture and opens up a cute little restaurant that sells his 3 favourite foods: sushi, curry and ramen.
Danny’s Diner is in need of your assistance to help the restaurant stay afloat – the restaurant has captured some very basic data from their few months of operation but have no idea how to use their data to help them run the business.

# Problem Statement #

Danny wants to use the data to answer a few simple questions about his customers, especially about their visiting patterns, how much money they’ve spent and also which menu items are their favourite. Having this deeper connection with his customers will help him deliver a better and more personalised experience for his loyal customers.
He plans on using these insights to help him decide whether he should expand the existing customer loyalty program – additionally he needs help to generate some basic datasets so his team can easily inspect the data without needing to use SQL.
Danny has provided you with a sample of his overall customer data due to privacy issues – but he hopes that these examples are enough for you to write fully functioning SQL queries to help him answer his questions!
Danny has shared with you 3 key datasets for this case study:
- sales
- menu
- members

You can inspect the entity relationship diagram and example data below.

![image](https://user-images.githubusercontent.com/77920592/192090656-593e05c7-2213-4f5c-a714-6d184aaf4ff9.png)

All datasets exist within the case1 database schema – be sure to include this reference within your SQL scripts as you start exploring the data and answering the case study questions.

Table 1: sales
The sales table captures all customer_id level purchases with an corresponding order_date and product_id information for when and what menu items were ordered.

![image](https://user-images.githubusercontent.com/77920592/192090710-138ce6c2-c0f6-4cd3-8f33-78f5e04fa6a4.png)

Table 2: menu
The menu table maps the product_id to the actual product_name and price of each menu item.

![image](https://user-images.githubusercontent.com/77920592/192090713-145deade-e4c3-465d-86bb-1450c719ec57.png)

Table 3: members
The final members table captures the join_date when a customer_id joined the beta version of the Danny’s Diner loyalty program.

![image](https://user-images.githubusercontent.com/77920592/192090724-fbae8786-8335-4e45-8f14-ff87403fc08b.png)

# SQL Scheme #

CREATE SCHEMA dannys_diner;
SET search_path = dannys_diner;

CREATE TABLE sales (
  "customer_id" VARCHAR(1),
  "order_date" DATE,
  "product_id" INTEGER
);

INSERT INTO sales
  ("customer_id", "order_date", "product_id")
VALUES
  ('A', '2021-01-01', '1'),
  ('A', '2021-01-01', '2'),
  ('A', '2021-01-07', '2'),
  ('A', '2021-01-10', '3'),
  ('A', '2021-01-11', '3'),
  ('A', '2021-01-11', '3'),
  ('B', '2021-01-01', '2'),
  ('B', '2021-01-02', '2'),
  ('B', '2021-01-04', '1'),
  ('B', '2021-01-11', '1'),
  ('B', '2021-01-16', '3'),
  ('B', '2021-02-01', '3'),
  ('C', '2021-01-01', '3'),
  ('C', '2021-01-01', '3'),
  ('C', '2021-01-07', '3');
 

CREATE TABLE menu (
  "product_id" INTEGER,
  "product_name" VARCHAR(5),
  "price" INTEGER
);

INSERT INTO menu
  ("product_id", "product_name", "price")
VALUES
  ('1', 'sushi', '10'),
  ('2', 'curry', '15'),
  ('3', 'ramen', '12');
  

CREATE TABLE members (
  "customer_id" VARCHAR(1),
  "join_date" DATE
);

INSERT INTO members
  ("customer_id", "join_date")
VALUES
  ('A', '2021-01-07'),
  ('B', '2021-01-09');
  
# Case Study Questions #

## 1. What is the total amount each customer spent at the restaurant? ##

select customer_id, sum(price) as total_spend
from sales s
join menu m on s.product_id = m.product_id
group by customer_id
order by total_spend

![image](https://user-images.githubusercontent.com/77920592/192090802-855d6a17-49bb-45ed-833c-4ca2be140586.png)


## How many days has each customer visited the restaurant? ## 

select customer_id, count(distinct order_date) as days_visited
from sales
group by customer_id

![image](https://user-images.githubusercontent.com/77920592/192090835-a4b961e9-925b-4d5f-85e0-c9cbefd8806c.png)

## What was the first item from the menu purchased by each customer? ## 

select distinct (customer_id), product_name
from sales s
join menu m on s.product_id = m.product_id
where order_date = any (select min(order_date) from sales group by customer_id)

![image](https://user-images.githubusercontent.com/77920592/192090843-96258555-4780-406e-94d1-6ea48fe34941.png)

## What is the most purchased item on the menu and how many times was it purchased by all customers? ## 

select product_name , max(s.product_id) as product_id, count(s.product_id) as times
from sales s
join menu m on s.product_id = m.product_id
group by product_name , s.product_id
order by times desc limit 1

![image](https://user-images.githubusercontent.com/77920592/192090851-20461034-784c-47ee-80ea-faf04baded6a.png)

## Which item was the most popular for each customer? ## 

with fav_item_cte as
(
select s.customer_id, m.product_name, count(m.product_id) as order_count,
dense_rank() over (partition by s.customer_id
order by count(s.customer_id) desc) as rank
from sales s
join menu m on s.product_id = m.product_id
group by s.customer_id, m.product_name
)

SELECT customer_id, product_name, order_count
FROM fav_item_cte
WHERE rank = 1;

![image](https://user-images.githubusercontent.com/77920592/192090859-895c41a2-c34c-4723-8a3b-0d71c644d8fb.png)

## Which item was purchased first by the customer after they became a member? ## 

with after_member_cte as
(
select s.customer_id, m.product_name, s.product_id, s.order_date,
dense_rank () over (partition by s.customer_id order by s.order_date) as rank
from sales s
join menu m on s.product_id = m.product_id
join members ms on ms.customer_id = s.customer_id
where s.order_date >= ms.join_date
)

select customer_id, product_name, product_id, order_date
from after_member_cte
where rank = 1

![image](https://user-images.githubusercontent.com/77920592/192090870-0bc616ab-18f1-4e75-838d-7554f37c24b7.png)

## Which item was purchased just before the customer became a member? ## 

with before_member_cte as
(
select s.customer_id, m.product_name, s.product_id, s.order_date,
dense_rank () over (partition by s.customer_id order by s.order_date desc) as rank
from sales s
join menu m on s.product_id = m.product_id
join members ms on ms.customer_id = s.customer_id
where s.order_date < ms.join_date
)

select customer_id, product_name, product_id, order_date
from before_member_cte
where rank = 1

![image](https://user-images.githubusercontent.com/77920592/192090885-8ba4fed6-1d1c-4288-9c76-ce2393e1422c.png)

## What is the total items and amount spent for each member before they became a member? ## 

select s.customer_id, count(s.product_id) as total_items, sum(price) as amount_spend
from sales s
join menu m on s.product_id = m.product_id
join members ms on ms.customer_id = s.customer_id
where s.order_date < ms.join_date
group by s.customer_id

![image](https://user-images.githubusercontent.com/77920592/192090896-4fac926b-9e09-4c71-93de-d39e13846ef2.png)

## If each $1 spent equates to 10 points and sushi has a 2x points multiplier - how many points would each customer have? ## 

with points_cte as
(
select customer_id, s.product_id,
case when s.product_id = 1 then price*20
else price*10
end as points
from sales s
join menu m on s.product_id = m.product_id
)

select customer_id,sum(points) as total_points
from points_cte
group by customer_id

![image](https://user-images.githubusercontent.com/77920592/192090905-ca528b3e-8169-4547-9143-e02535307cb8.png)

## In the first week after a customer joins the program (including their join date) they earn 2x points on all items, not just sushi - how many points do customer A and B have at the end of January? ## 

with date_cte as
(
select *,
join_date+ INTERVAL ‘6 day’ as valid_date
from members as ms
)

select s.customer_id,
sum(
case when s.product_id = 1 then price*20 
when s.order_date between d.join_date and d.valid_date then price*20
else price*10 end) as points
from date_cte d
join sales s on s.customer_id = d.customer_id
join menu m on s.product_id = m.product_id
join members ms on ms.customer_id = s.customer_id
where order_date < ‘2021-01-31’
group by s.customer_id

![image](https://user-images.githubusercontent.com/77920592/192090923-847cd809-d445-40cb-993d-01d67f6b29e8.png)

# Join All The Things #
 
The following questions are related creating basic data tables that Danny and his team can use to quickly derive insights without needing to join the underlying tables using SQL.
Recreate the following table output using the available data:

![image](https://user-images.githubusercontent.com/77920592/192090933-65a50578-2284-414e-bd9b-c07514d75aba.png)

select s.customer_id, s.order_date, m.product_name, m.price,
case when s.order_date >= join_date then ‘Yes’
when s.order_date < join_date then ‘No’
else ‘Null’ end as member
from sales s
left join menu m on s.product_id = m.product_id
left join members ms on ms.customer_id = s.customer_id
order by order_date

![image](https://user-images.githubusercontent.com/77920592/192090941-a0d4e08b-caf2-44aa-b2f6-0fd9971a8f73.png)


# Rank All The Things #

Danny also requires further information about the ranking of customer products, but he purposely does not need the ranking for non-member purchases so he expects null ranking values for the records when customers are not yet part of the loyalty program.

![image](https://user-images.githubusercontent.com/77920592/192090946-9c1946e4-3eac-4010-8d8e-a8e81c5fd8d1.png)

with rank_cte as (
select s.customer_id, s.order_date, m.product_name, m.price,
case when s.order_date >= join_date then ‘Yes’
when s.order_date < join_date then ‘No’
else ‘Null’ end as member
from sales s
left join menu m on s.product_id = m.product_id
left join members ms on ms.customer_id = s.customer_id
order by order_date
)

select *,
case when member = ‘No’ then Null
else
rank() over (partition by customer_id, member
order by order_date) end as ranking
from rank_cte

![image](https://user-images.githubusercontent.com/77920592/192090956-f719eff7-e926-4f60-8ae7-6c47f877fa7c.png)


# Findings and Recommendations #
 

- Ramen is the most popular item, followed by curry and sushi. Danny might want to introduce ramen with more varieties/flavours.
- Customer B visited the diner the most and he/she seems to enjoy three dishes equally. 
- Customer A and B’s last ordered items are sushi and curry. These items might be the deciding factors for them to sign up the membership as Customer C is not yet member and he/she has not yet tried these two items!
- There is no confirmed  evidence showing customers visit more after signing up membership. Danny might want to offer a 5% discount for all members, or a system to redeem points. 
- Customers who have signed up the membership seem to spend more at the diner. 
