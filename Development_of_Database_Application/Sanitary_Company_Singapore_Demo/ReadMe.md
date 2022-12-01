## Description ##

This is a demo of the SQL server developed for a sanitary company, Bathworld based in Singapore. It contains of 12 tables consisting of data from different departments.
Demo database are created using Mockaroo and imported to SQL Server using SSIS Package.

The tasks include but not limited to:
- Design, develop, and test database and database objects (tables, views, stored procedures, indexes, functions, constraints)
- Build complex queries using T-SQL command
- Extract, transform and load the data from multiple sources and store them inside data warehouse using SSIS packages 


## Tables ##
The database contains 11 tables:
| Table Name| Columns |
| ------------- | ------------- |
| **Emp** | emp_id, emp_name, emp_title, emp_type(office / delivery), bday, join_date, nationality, status (employed / resigned), special_note |
| **Resigned_emp** |emp_id, date_of_resignation, reason, salary_cleared, special_note |
| **Salary_change** |emp_id, updates_date, updated_salary, default_comms, special_note |
| **Interior_designer** | int_id, int-name, whatsapp, address, postal_code, special_note |
| **Supplier** | sup_id, sup_name, company, dept, category, email, phone_number, country, status, special_note |
| **Supplier_billing** | invoice_id, sup_company, billing_date, billing_amount, status, special_note |
| **Customer** | cus_id, cus_name, int_id, emp_id, whatsapp, house_no, street, postal_code, last_visit, order_placed (Yes / No), special_note|
| **Quotation** | cus_id, emp_id, int_id, quotation_number, quotation_date, amount_purchase, status, special_note |
| **Confirmed_order** | order_id, cus_id, quotation_number, comms, payment_method, payment_cleared, special_note |
| **Ordered_items** | order_id, sku, quantity, price, date_of_delivery, special_note |
| **Product_sku** | sku, item_name, description, price, brand, color, status, stock_quantity, pre_order_arrival_date, special_note |

## Entity Diagram ##
![image](https://user-images.githubusercontent.com/77920592/205033353-c9e68bd6-fe31-4d45-a4dc-c23f6b03bcd1.png)
