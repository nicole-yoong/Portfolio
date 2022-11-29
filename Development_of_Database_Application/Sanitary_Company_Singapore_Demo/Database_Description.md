## Description ##

This is a demo of the SQL server developed for a sanitary company, Bathworld based in Singapore. 
Demo database are created using Mockaroo and imported to SQL Server using SSIS Package.

It contains of 12 tables consisting of data from different departments.
Constraints and triggers are developed. 

## Tables ##
The database contains 11 tables:
| Table Name| Columns |
| ------------- | ------------- |
| **Emp** | emp_id, emp_name, emp_title, emp_type(office / delivery), bday, join_date, nationality, status (employed / resigned), special_note |
| **Resigned_emp** |emp_id, date_of_resignation, reason, salary_cleared, special_note |
| **Salary_change** |emp_id, increment_date, increment_salary, default_comms, special_note |
| **Interior_designer** | int_id, int-name, whatsapp, address, postal_code, special_note |
| **Supplier** | sup_id, sup_name, company, dept, category, email, phone_number, country, status, special_note |
| **Supplier_billing** | invoice_id, sup_company, billing_date, billing_amount, status, special_note |
| **Customer** | cus_id, cus_name, int_id, emp_id, whatsapp, house_no, street, postal_code, last_visit, order_placed (Yes / No), special_note|
| **Quotation** | cus_id, emp_id, int_id, quotation_number, quotation_date, amount_purchase, status, special_note |
| **Confirmed_order** | order_id, cus_id, quotation_number, comms, payment_method, payment_cleared, special_note |
| **Ordered_items** | order_id, sku, quantity, price, date_of_delivery, special_note |
| **Product_sku** | sku, item_name, description, price, brand, color, status, stock_quantity, pre_order_arrival_date, special_note |

### A. Employee ###

**Create emp table**
```sql
create table emp(
	emp_id integer,
	emp_name varchar(100),
	emp_title varchar(100),
	emp_type varchar(100), --- office/delivery
	bday date,
	join_date date,
	nationality varchar(100),
	status varchar(100), --- employed/resigned 
	special_note text,
	primary key (emp_id)
);
```
![image](https://user-images.githubusercontent.com/77920592/204303806-8b0cc13e-82aa-47c4-8897-2c8b04b05206.png)

**Create resigned_emp table**
```sql
create table resigned_emp(
	emp_id integer,
	date_of_resignation date,
	reason text,
	salary_cleared varchar(100),
	special_note text,
	primary key (emp_id),
	foreign key (emp_id) references emp (emp_id)
);
```
![image](https://user-images.githubusercontent.com/77920592/204305679-28205808-fadc-479b-a872-f1edde0e4aa8.png)

**Update status of a specific employee to 'Resigned' triggers the resigned_employee table to update**
```sql
CREATE TRIGGER update_emp_status 
ON emp FOR UPDATE
AS
BEGIN 
	INSERT INTO resigned_emp(emp_id, date_of_resignation)
	SELECT DISTINCT emp.emp_id, getdate() FROM INSERTED emp
	LEFT JOIN resigned_emp
	ON resigned_emp.emp_id = emp.emp_id
	WHERE emp.status = 'Resigned'
END
GO
```

```sql
--- Function testing 
update emp
set status = 'Resigned'
where emp_id = 18;

update resigned_emp
set reason = 'Resigned to pursue studies abroad',
salary_cleared = 'Yes'

select * from resigned_emp
```
![image](https://user-images.githubusercontent.com/77920592/204304535-e258682f-c41f-4ab9-8028-605728727f5d.png)


### B. Salary Change ###

**Create salary_change table**
```sql
create table salary_change(
	emp_id integer,
	increment_date date,
	increment_salary integer,
	default_comms decimal(6,2),
	special_note text,
);

```
![image](https://user-images.githubusercontent.com/77920592/204307764-92cf8ec8-98d0-48e2-a4ff-aa91b1e17011.png)

**Insert on new employee update the salary_change table by inserting the new emp_id**

```sql
CREATE TRIGGER insert_salary_change
ON emp FOR INSERT
AS
BEGIN 
	INSERT INTO salary_change(emp_id, increment_date)
	SELECT DISTINCT emp.emp_id, getdate() FROM INSERTED emp
	LEFT JOIN salary_change
	ON salary_change.emp_id = emp.emp_id
END
GO
```

```sql
--- Function testing 
insert into emp
values (21, 'Alex Mitchell', 'Junior Sales', 'Office', '1997-06-16', '2020-06-05', 'Malaysia', 'Employed', NULL);

update salary_change
set increment_salary = 2800, default_comms = 0.20, special_note = 'Initial salary'
where emp_id = 21;

select * from salary_change
```

![image](https://user-images.githubusercontent.com/77920592/204308218-ec51472a-249b-45df-b5e9-6cf61b892801.png)

### C. Interior Designer ###

**Create interior_designer table**
```sql
create table interior_designer (
	int_id integer,
	int_name varchar(100),
	whatsapp varchar(100),
	address varchar(100),
	postal_code integer,
	special_note text,
	primary key (int_id)
);
```
![image](https://user-images.githubusercontent.com/77920592/204308552-4b2fc1ee-1d03-4eb3-b1c5-6841ad1258a9.png)

### D. Supplier ###

**Create supplier table**
```sql
create table supplier(
	sup_id int,
	sup_name varchar(100),
	company varchar(100),
	dept varchar(100),
	category varchar(100), --- sanitary/vinyl/lifestyle/marketing
	email varchar(100),
	phone_number varchar(100),
	country varchar(100),
	status varchar(100), 
	special_note text,
	primary key (sup_id)
);
```
![image](https://user-images.githubusercontent.com/77920592/204308775-1cc02fc9-1ac1-42a1-880d-ac2ff673a4a5.png)

**Create supplier_billing table**
```sql
create table supplier_billing(
	invoice_id varchar(100),
	sup_company varchar(100),
	billing_date date,
	billing_amount decimal(6,2),
	status varchar(100),
	special_note text,
	primary key (invoice_id)
);
```
![image](https://user-images.githubusercontent.com/77920592/204308955-5c277ef0-1cf8-43a8-acae-a65cbf7eee5a.png)

### E. Customer ###

**Create customer table**
```sql
create table customer(
	cus_id integer,
	cus_name varchar(100),
	int_id integer,
	emp_id integer,
	whatsapp varchar(100),
	house_no varchar(100),
	street varchar(100),
	postal_code integer,
	last_visit date,
	order_placed varchar(100),
	special_note text,
	primary key (cus_id),
	constraint FK_Customer foreign key (int_id) 
	references interior_designer (int_id) on update cascade,
	constraint FK_Employee foreign key (emp_id) 
	references emp (emp_id) on update cascade
);
```
![image](https://user-images.githubusercontent.com/77920592/204309607-38a4d0f9-fc3c-4d81-a2c9-5c285ceaa67c.png)

### F. Quotation and Order ###

**Create quotation table**
```sql
create table quotation (
	cus_id integer,
	emp_id integer,
	int_id integer,
	quotation_number integer identity(1,1),
	quotation_date date,
	amount_purchase decimal(6,2),
	status varchar (100), --- either pending or confirmed
	special_note text,
	primary key (quotation_number),
	foreign key (cus_id) references customer (cus_id),
	foreign key (int_id) references interior_designer (int_id),
	foreign key (emp_id) references emp (emp_id)
);
```
![image](https://user-images.githubusercontent.com/77920592/204548858-20910e65-a141-4374-bec5-82ab38c51cc9.png)

**Insert customer data into quotation table if orderis placed**
```sql
CREATE TRIGGER insert_into_quotation
ON customer FOR UPDATE
AS
BEGIN 
	INSERT INTO quotation(cus_id, emp_id, int_id, quotation_date)
	SELECT DISTINCT customer.cus_id, customer.emp_id, customer.int_id, getdate()
	FROM INSERTED customer
	LEFT JOIN quotation
	ON customer.cus_id = quotation.cus_id
	WHERE customer.order_placed = 'Yes'
END
GO
```

```sql
--- Function Testing ---
update customer
set order_placed = 'Yes'
where cus_id = 30;

select * from quotation
```
![image](https://user-images.githubusercontent.com/77920592/204311667-8c324b6f-1b17-4e1e-a0a9-df4683e231cc.png)

**Bulk update columns in quotation table by importing flat files and merge tables**
```sql
--- Import flat file to a table named quotation_temp
update quotation
set amount_purchase = amount
from quotation q join quotation_temp t
on q.quotation_number = t.quotation_number;

select * from quotation;
```
![image](https://user-images.githubusercontent.com/77920592/204351511-6ab8d19a-7f70-4d73-87cd-666061cc5023.png)


**Create confirmed_order table**
```sql
create table confirmed_order(
	quotation_number integer,
	comms decimal(6,2),
	payment_method varchar(100),
	payment_cleared varchar(100), --- yes/half/pending
	special_note text,
	primary key (quotation_number),
	foreign key (quotation_number) 
	references quotation (quotation_number)
);
```
![image](https://user-images.githubusercontent.com/77920592/204548943-aa7c63cf-94e3-4900-84a3-a4cc401c9746.png)

**Insert quotation data into the confirmed_order table is the quotation is confirmed**
```sql
CREATE TRIGGER insert_into_confirmed_order
ON quotation FOR UPDATE
AS
BEGIN 
	INSERT INTO confirmed_order(quotation_number)
	SELECT DISTINCT quotation.quotation_number
	FROM INSERTED quotation
	LEFT JOIN confirmed_order
	ON quotation.quotation_number = confirmed_order.quotation_number
	WHERE quotation.status = 'Confirmed'
END
GO
```

```sql
--- Function Testing
update quotation
set status = 'Confirmed'
where quotation_number = 34;

select * from confirmed_order
```
![image](https://user-images.githubusercontent.com/77920592/204338441-95834d3e-f276-4e6c-bae1-c488363b3ee0.png)

**Bulk update columns in confirmed_table table by importing flat files and merge tables**
```sql
--- Import flat file to a table named confirmed_table_temp
update confirmed_order
set comms = t.comms, payment_method = t.payment_method, payment_cleared =  t.payment_cleared
from confirmed_order co join confirmed_order_temp t
on co.quotation_number = t.quotation_number;

select * from confirmed_order
```
![image](https://user-images.githubusercontent.com/77920592/204353814-48c484d6-eec4-4d4a-b2a2-62a5cd196501.png)

**Create ordered_item table**
```sql
create table ordered_items (
	quotation_number integer,
	sku varchar(100),
	quantity integer,
	date_of_delivery date,
	special_note text,
	foreign key (quotation_number) references  confirmed_order (quotation_number) ON DELETE CASCADE,
	foreign key (sku) references product_sku (sku)
);
```
![image](https://user-images.githubusercontent.com/77920592/204549019-d841bfa7-87c8-4825-b43d-85dae046e0bd.png)


**Create cancelled_order table**
```sql
create table cancelled_order(
	order_id integer,
	date_of_cancellation date,
	amount_purchase integer,
	refund_required varchar(100),
	reason varchar(100),
	special_note text
);
```

**Insert confirmed_order data into the cancelled_order table if the order is cancelled**
```sql
CREATE TRIGGER delete_confirmed_order 
ON confirmed_order FOR DELETE
AS
BEGIN 
	DECLARE @order_id INT, @amount_purchase INT, @date_of_cancellation DATE
	SELECT @order_id = DELETED.order_id FROM DELETED
	INSERT INTO cancelled_order(order_id, amount_purchase, date_of_cancellation)
	VALUES (@order_id, @amount_purchase, getdate())
END
GO
```

```sql
--- Function testing
delete from confirmed_order 
where order_id = 6;

select * from cancelled_order
```
![image](https://user-images.githubusercontent.com/77920592/204339966-09104789-7ff4-4551-95e7-1218745c2dd7.png)

#### G. Product SKU ####

**Create product_sku table**
```sql
create table product_sku(
	sku varchar(100),
	item_name text,
	description text,
	price decimal(7,2),
	brand varchar(100),
	color varchar(100),
	status varchar(100),
	stock_quantity integer,
	pre_order_arrival_date date,
	special_note text,
	primary key (sku)
);
```
![image](https://user-images.githubusercontent.com/77920592/204340184-2cbe5986-8b02-4bfc-9835-427b785acd9f.png)

## Views ##

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
select ordered_items.order_id, ordered_items.sku, ordered_items.special_note, 
ordered_items.date_of_delivery, status from ordered_items
join product_sku
on ordered_items.sku = product_sku.sku

select * from ordered_items_view
```
