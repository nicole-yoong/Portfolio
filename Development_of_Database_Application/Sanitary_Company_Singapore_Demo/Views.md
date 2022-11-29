# Views #

### Top Management Level ###

**Rolling sales**
```sql

```

**Monthly sales**
```sql
drop view monthly_total_sales_view;

create view monthly_total_sales_view as
select year(quotation_date) as year, month(quotation_date) as month,
sum (amount_purchase) over (partition by year(quotation_date), month(quotation_date) order by quotation_date) as rolling_sales 
from confirmed_order co join quotation q on co.quotation_number = q.quotation_number;

select * from monthly_total_sales_view;
```

**Performance of sales personnel**
```sql
select emp_id, sum(amount_purchase) as Sales_figure
from quotation
where status = 'Confirmed'
--- and month(quotation_date) = 11
group by emp_id
order by sum(amount_purchase) desc;
```

**Commissions for sales personnel**
```sql
select emp_id, sum(amount_purchase*comms) as comms_amount
from confirmed_order co join quotation q on co.quotation_number = q.quotation_number
---where month(quotation_date) = 11
group by emp_id;
```

**Bonus for sales personnel if hit certain target**
```sql
select emp_id, 
case when sum(amount_purchase)> 100000 then (0.015*sum(amount_purchase))
when sum(amount_purchase)< 100000 then 0
end as bonus
from confirmed_order co join quotation q on co.quotation_number = q.quotation_number
---where month(quotation_date) = 11
group by emp_id
```

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

### Sales Level ###
```sql
--- check which quotation is still pending for followup
select distinct(quotation.cus_id), cus_name, whatsapp from quotation join customer
on quotation.cus_id = customer.cus_id
where status like 'pending';
```

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
group by int_id;

select * from id_loyalty_prog_view
```

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
```

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