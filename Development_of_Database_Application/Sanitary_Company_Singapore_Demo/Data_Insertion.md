# Data Insertion #

**Bulk update columns in quotation table by importing flat files and merge tables**
```sql
--- Import flat file to a table named quotation_temp
update quotation
set amount_purchase = amount
from quotation q join quotation_temp t
on q.quotation_number = t.quotation_number;

select * from quotation;
```
![image](https://user-images.githubusercontent.com/77920592/204562101-78a0b24a-7dcd-4193-95a6-4e1e26ee69c4.png)

**Bulk update columns in confirmed_orders table by importing flat files and merge tables**
```sql
--- Import flat file to a table named confirmed_table_temp
update confirmed_order
set comms = t.comms, payment_method = t.payment_method, payment_cleared =  t.payment_cleared
from confirmed_order co join confirmed_order_temp t
on co.quotation_number = t.quotation_number;

select * from confirmed_order
```
![image](https://user-images.githubusercontent.com/77920592/204562202-dfb8e12c-025f-4fa1-a32b-cb76f723f39c.png)

**Bulk update columns in ordered_items table by selecting the data from flat files into the table**
```sql
insert into ordered_items (quotation_number, quantity, sku)
select quotation_number, quantity, sku
from ordered_items_temp

select * from ordered_items;
```
![image](https://user-images.githubusercontent.com/77920592/204562317-cb5e4297-4a24-4ae6-b9c2-f202ffe4d757.png)