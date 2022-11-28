## Description ##

This is a demo of the SQL server developed for a sanitary company, Bathworld based in Singapore.
It contains of 12 tables consisting of data from different departments.
Constraints and triggers are developed. 

## Database Highlights: ##

### Create Table ###
#### A. Employee ####
```sql
create table emp(
	emp_id integer,
	emp_name varchar(100),
	emp_title varchar(100),
	emp_type varchar(100), --- office/delivery
	bday date,
	join_date date,
	nationality varchar(100),
	status varchar(100), --- whether still in employment or resigned 
	special_note text,
	primary key (emp_id)
);


create table resigned_emp(
	emp_id integer,
	date_of_resignation date,
	reason text,
	salary_cleared varchar(100),
	special_note text,
	primary key (emp_id),
	foreign key (emp_id) references emp (emp_id)
);


--- update status of a specific emp_id on employee will trigger resigned_employee to update
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

#### B. Salary Change ####
```sql
create table salary_change(
	emp_id integer,
	increment_date date,
	increment_salary integer,
	default_comms decimal,
	special_note text,
);

--- insert on new employee update the salary_change table
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

#### C. Interior Designer ####
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

#### D. Supplier ####
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

#### E. Customer ####
```sql
create table customer(
	cus_id integer,
	cus_name varchar(100),
	int_id integer,
	emp_id integer,
	whatsapp varchar(100),
	address_house_no varchar(100),
	address_street varchar(100),
	address_postal_code integer,
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

#### F. Quotation and Order ####
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

CREATE TRIGGER insert_into_quotation
ON customer FOR UPDATE
AS
BEGIN 
	INSERT INTO quotation(cus_id, emp_id, int_id)
	SELECT DISTINCT customer.cus_id, customer.emp_id, customer.int_id 
	FROM INSERTED customer
	LEFT JOIN quotation
	ON customer.cus_id = quotation.cus_id
	WHERE customer.order_placed = 'Yes'
END
GO

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

create table cancelled_order(
	order_id integer,
	date_of_cancellation date,
	amount_purchase integer,
	refund_required varchar(100),
	reason varchar(100),
	special_note text
);
```

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

### Dependencies ###

![image](https://user-images.githubusercontent.com/77920592/204134784-01641b5a-658c-4777-8a31-542bcb4124a7.png)



### Create Views ###
```sql
--- TOP MANAGEMENT LEVEL

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



--- SALES LEVEL

--- check which quotation is still pending for followup
select distinct(quotation.cus_id), cus_name, whatsapp from quotation join customer
on quotation.cus_id = customer.cus_id
where status like 'pending';



--- MARKETING LEVEL

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



--- OPERATION LEVEL

--- check what items to be order before a certain date
create view ordered_items_view as
select ordered_items.order_id, ordered_items.sku, ordered_items.special_note, 
ordered_items.date_of_delivery, status from ordered_items
join product_sku
on ordered_items.sku = product_sku.sku

select * from ordered_items_view
```

### Insert Demo Data ###

Demo database are created using Mockaroo and imported to SQL Server using SSIS Package.
![image](https://user-images.githubusercontent.com/77920592/204137567-92e0763d-edc5-448d-affb-5131cc3862f7.png)
![image](https://user-images.githubusercontent.com/77920592/204137525-28df013a-9984-46d3-953a-9f9264fe6d5c.png)


### Function Testing ###
#### Update status of a specific emp_id on employee will trigger resigned_employee to update ####
update emp
set status = 'Resigned'
where emp_id = 18;

select * from emp;

#### Insert on new employee update the salary_change table ####
