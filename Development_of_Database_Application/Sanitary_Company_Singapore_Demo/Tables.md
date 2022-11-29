# Tables #

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

### G. Product SKU ###

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
