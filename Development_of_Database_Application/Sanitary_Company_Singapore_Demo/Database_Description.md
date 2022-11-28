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
	primary key (cus_id, quotation_number),
	foreign key (cus_id) references customer (cus_id),
	foreign key (int_id) references interior_designer (int_id),
	foreign key (emp_id) references emp (emp_id)
);
```

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

```sql
create table confirmed_order(
	order_id integer identity(1,1),
	cus_id integer,
	quotation_number integer,
	comms decimal,
	payment_method varchar(100),
	payment_cleared varchar(100), --- yes/half/pending
	special_note text,
	primary key (order_id),
	foreign key (cus_id, quotation_number) 
	references quotation (cus_id, quotation_number)
);
```

**Insert quotation data into the confirmed_order table is the quotation is confirmed**
```sql
CREATE TRIGGER insert_into_confirmed_order
ON quotation FOR UPDATE
AS
BEGIN 
	INSERT INTO confirmed_order(cus_id, quotation_number)
	SELECT DISTINCT quotation.cus_id, quotation.quotation_number
	FROM INSERTED quotation
	LEFT JOIN confirmed_order
	ON quotation.cus_id = confirmed_order.cus_id
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


```sql
create table ordered_items (
	order_id integer,
	sku varchar(100),
	quantity integer,
	price varchar(100),
	date_of_delivery date,
	special_note text,
	foreign key (order_id) references  confirmed_order (order_id) ON DELETE CASCADE,
	foreign key (sku) references product_sku (sku)
);
```

**Insert order_id from the confimed_order table into the ordered_item table**
```sql
CREATE TRIGGER insert_ordered_items
ON confirmed_order FOR INSERT
AS
BEGIN 
	INSERT INTO ordered_items(order_id)
	SELECT DISTINCT confirmed_order.order_id FROM INSERTED confirmed_order
	LEFT JOIN ordered_items
	ON ordered_items.order_id = confirmed_order.order_id
END
GO
```

```sql
--- Function Testing
update quotation
set status = 'Confirmed'
where quotation_number = 34;

select * from ordered_items
```
![image](https://user-images.githubusercontent.com/77920592/204339117-278c49be-4c71-4be0-89ba-fc6f0f351878.png)

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

## Dependencies ##

![image](https://user-images.githubusercontent.com/77920592/204134784-01641b5a-658c-4777-8a31-542bcb4124a7.png)

## Views ##

### Top Management Level ###
```sql
--- total sales of a specific month 
drop view temp_total_sales_view;
create view temp_total_sales_view as
select date_of_purchase,
sum (amount_purchase) over (partition by MONTH(date_of_purchase) order by date_of_purchase) as rolling_sales 
from confirmed_order;

select * from temp_total_sales_view;

drop view monthly_sales_view;
create view monthly_sales_view as
select max(rolling_sales) as total_sales, MONTH(date_of_purchase) as month
from temp_total_sales_view
group by MONTH(date_of_purchase);

select * from monthly_sales_view;

--- which sales personnel performs better
select emp_id, sum(amount_purchase) from confirmed_order
group by emp_id
order by sum(amount_purchase) desc;

--- compute commissions for sales personnel
select emp_id, sum(amount_purchase),
CASE WHEN sum(amount_purchase)> 100000 THEN (0.02*sum(amount_purchase))
WHEN sum(amount_purchase)< 100000 THEN (0.01*sum(amount_purchase))
END comms
from confirmed_order
where date_of_purchase between '2021-11-01' and '2021-12-31' 
group by emp_id, comms;
```

### Sales Level ###
```sql
--- check which quotation is still pending for followup
select distinct(quotation.cus_id), cus_name, whatsapp from quotation join customer
on quotation.cus_id = customer.cus_id
where status like 'pending';
```

### Marketing Level ###
```sql
--- loyalty programme for each interior designer 
drop view id_loyalty_prog_view;
create view id_loyalty_prog_view as 
select int_id, sum(amount_purchase) as amount,
CASE WHEN sum(amount_purchase)> 100000 THEN 'Gold'
WHEN sum(amount_purchase)< 100000 THEN 'Silver'
END tier
from confirmed_order
where date_of_purchase between '2021-01-01' and '2021-12-31' 
group by int_id;

select * from id_loyalty_prog_view


--- loyalty programme for customer
drop view cus_loyalty_prog_view;
create view cus_loyalty_prog_view as 
select cus_id, sum(amount_purchase) as amount,
CASE WHEN sum(amount_purchase)> 100000 THEN 'Gold'
WHEN sum(amount_purchase)< 100000 THEN 'Silver'
END tier
from confirmed_order
where date_of_purchase between '2021-01-01' and '2021-12-31' 
group by cus_id;

select * from cus_loyalty_prog_view
```

### Operation Level ###
```sql
--- check what items to be order before a certain date
create view ordered_items_view as
select ordered_items.order_id, ordered_items.sku, ordered_items.special_note, 
ordered_items.date_of_delivery, status from ordered_items
join product_sku
on ordered_items.sku = product_sku.sku

select * from ordered_items_view
```

