# Trigger Functions #

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

**Update salary to 0 when employee resigns**
```sql
CREATE TRIGGER update_resigned_salary
ON resigned_emp FOR INSERT
AS
BEGIN 
	INSERT INTO salary_change(emp_id, increment_date, increment_salary, special_note)
	SELECT DISTINCT emp.emp_id, getdate(), 0, 'Resigned' FROM INSERTED emp
	LEFT JOIN salary_change
	ON salary_change.emp_id = emp.emp_id
END
GO
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
	and quotation.quotation_number not in (select quotation_number from confirmed_order)
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
