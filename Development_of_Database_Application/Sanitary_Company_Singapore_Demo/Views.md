# Views #

### Top Management Level ###

**Rolling sales**
```sql
drop view monthly_total_sales_view;

create view rolling_sales_view as
select year(quotation_date) as year, month(quotation_date) as month,
sum(amount_purchase) over (partition by year(quotation_date), month(quotation_date) order by quotation_date) as rolling_sales 
from confirmed_order co join quotation q on co.quotation_number = q.quotation_number;

select * from rolling_sales_view
```
![image](https://user-images.githubusercontent.com/77920592/204571809-e0ff5d37-7eb2-4fb5-bb74-6bf27a6f9783.png)

**Monthly sales**
```sql
drop view monthly_sales_view;

create view monthly_sales_view as
select year(quotation_date) as year, month(quotation_date) as month,
sum(amount_purchase) as monthly_sales 
from confirmed_order co join quotation q on co.quotation_number = q.quotation_number
group by year(quotation_date), month(quotation_date)
order by year(quotation_date), month(quotation_date);

select * from monthly_sales_view
```
![image](https://user-images.githubusercontent.com/77920592/204571645-2fa5fe57-ccac-445a-ac8b-9eef00a5e1ab.png)

**Performance of sales personnel**
```sql
select emp_id, sum(amount_purchase) as Sales_figure
from quotation
where status = 'Confirmed'
--- and month(quotation_date) = 11
group by emp_id
order by sum(amount_purchase) desc;
```
![image](https://user-images.githubusercontent.com/77920592/204579599-397ba3c2-8dd0-4c56-b73d-578c1d3dac31.png)


**Commissions for sales personnel**
```sql
select emp_id, sum(amount_purchase*comms) as comms_amount
from confirmed_order co join quotation q on co.quotation_number = q.quotation_number
---where month(quotation_date) = 11
group by emp_id;
```
![image](https://user-images.githubusercontent.com/77920592/204579665-a3e6ce1a-dc08-42b6-a352-ef40160248e8.png)

**Bonus for sales personnel if hit certain target**
```sql
select emp_id, 
case when sum(amount_purchase)> 100000 then (0.015*sum(amount_purchase))
end as bonus
from confirmed_order co join quotation q on co.quotation_number = q.quotation_number
---where month(quotation_date) = 11
group by emp_id
```
![image](https://user-images.githubusercontent.com/77920592/204579823-4885bd48-5f9a-4ac3-8fd3-23215a16ba51.png)

**Bonus + Salary for sales personnel**
```sql
with cte as
(
select emp_id, amount_purchase, 
case when sum(amount_purchase)> 100000 then (0.015*sum(amount_purchase))
when sum(amount_purchase)< 100000 then 0
end as bonus
from confirmed_order co join quotation q on co.quotation_number = q.quotation_number
---where month(quotation_date) = 11
group by emp_id, amount_purchase
)
select emp_id, bonus, sum(amount_purchase) + bonus as total_salary from cte
group by emp_id, bonus
```
![image](https://user-images.githubusercontent.com/77920592/204579882-d133d4c6-0eda-473c-8a7b-a67226423893.png)

### Sales Level ###
**Pending / Confirmed quotation to follow-up**
```sql
select distinct(quotation.cus_id), cus_name, whatsapp from quotation join customer
on quotation.cus_id = customer.cus_id
where status like 'Confirmed' 
---and month(quotation_date) = 11;
```
![image](https://user-images.githubusercontent.com/77920592/204573088-f325b7a7-9e5c-4921-a18d-fe638426d9f1.png)

### Marketing Level ###
**Contribution of each interior designer**
```sql
drop view id_loyalty_prog_view;

create view id_loyalty_prog_view as 
select int_id, sum(amount_purchase) as amount,
CASE WHEN sum(amount_purchase)> 100000 THEN 'Gold'
WHEN sum(amount_purchase)< 100000 THEN 'Silver'
END tier
from confirmed_order co join quotation q on co.quotation_number = q.quotation_number
---where month(quotation_date) = 11 
group by int_id
order by amount desc;

select * from id_loyalty_prog_view
order by amount desc
```
![image](https://user-images.githubusercontent.com/77920592/204572520-fda48eee-ebc6-4b0f-bae9-a3399faed772.png)

**Customer loyalty programme**
```sql
drop view cus_loyalty_prog_view;

create view cus_loyalty_prog_view as 
select q.cus_id, sum(amount_purchase) as amount,
CASE WHEN sum(amount_purchase)> 100000 THEN 'Gold'
WHEN sum(amount_purchase)< 100000 THEN 'Silver'
END tier
from confirmed_order co join quotation q on co.quotation_number = q.quotation_number
---where month(quotation_date) = 11 
group by q.cus_id;

select * from cus_loyalty_prog_view
order by amount desc
```
![image](https://user-images.githubusercontent.com/77920592/204572680-0eb159fc-670d-415f-ac83-cfa2ecb5bb21.png)

### Operation Level ###
**Items required before certain date**
```sql
drop view ordered_items_view;

create view ordered_items_view as
select ordered_items.quotation_number, ordered_items.sku, ordered_items.special_note, 
ordered_items.date_of_delivery, status from ordered_items
join product_sku
on ordered_items.sku = product_sku.sku

select * from ordered_items_view
```
