# Customer Behavior Analysis #
![image](https://user-images.githubusercontent.com/77920592/193347472-dc64e721-1abf-41f6-b42d-233789b02945.png)

## Customer Registration ##

### Registration over time report ###
Find the registration count for each week in each year. Show the following columns: RegistrationYear, RegistrationWeek, and RegistrationCount. Order the results by the year and week.
```sql
select datepart(week, registrationdate) as RegistrationWeek,
datepart(year, registrationdate) as RegistrationYear,
count(customerid) as RegistrationCount,
min(registrationDate) AS WeekLabel
from customers
group by datepart(year, registrationdate), datepart(week, registrationdate)
order by datepart(year, registrationdate), datepart(week, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193341384-c5422360-928b-4ec5-bff1-ba5b400772d9.png)

### Customer cohort report ###
Create an extended version of the report shown in the explanation. Instead of annual customer cohorts per channel, show weekly customer cohorts per channel in each year. Show the following columns: RegistrationYear, RegistrationWeek, ChannelName, and RegistrationCount. Order the results by year and week.
```sql
select ch.channelname, 
  datepart(year, registrationdate) as registrationyear,
  datepart(week, registrationdate) as registrationweek,
  count(customerid) as registrationcount
from customers cu 
join channels ch on cu.channelid = ch.id
group by ch.id, ch.channelname, datepart(year, registrationdate), datepart(week, registrationdate)
order by datepart(year, registrationdate), datepart(week, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193341584-16d49822-fa72-4e84-b018-1f457e5dc67a.png)

## Conversion Rates ##

### Conversion rates in weekly cohorts ###
**Global lifetime conversion rate** is the percentage of registered customers who've made at least one purchase. This is a good indicator of the general condition of our business.
Create a similar report showing conversion rates in monthly cohorts. Display the conversion rates as ratios rounded to three decimal places. Show the following columns: Year, Month, and ConversionRate. Order the results by year and month.
```sql
select datepart(year, registrationdate) as Year,
datepart(month, registrationdate) as Month,
round(count(firstorderid) / cast(count(*) as float), 3) as ConversionRate
from customers
group by datepart(year, registrationdate), datepart(month, registrationdate)
order by datepart(year, registrationdate), datepart(month, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193341920-ab7bce6d-cc3b-4aef-a644-4a382dc2f4f8.png)

### Average time to first order in weekly cohorts ###
Calculate the average number of days that passed between registration and first order in quarterly registration cohorts. Show the following columns: Year, Quarter, and AvgDaysToFirstOrder. Order the results by year and quarter.
```sql
select avg(1.0 * datediff(day, registrationdate, firstorderdate)) as AvgDaysToFirstOrder,
datepart(quarter, registrationdate) as Quarter,
datepart(year, registrationdate) as Year
from customers 
group by datepart(year, registrationdate), datepart(quarter, registrationdate)
order by datepart(year, registrationdate), datepart(quarter, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193342291-5c0ba86e-a0e0-4aff-a7c6-2b14811add2a.png)

### Conversion charts ###
Our e-store has used three versions of the registration form:
1. 'ver1' – introduced when the e-store started.
2. 'ver2' – introduced on March 14, 2017.
3. 'ver3' – introduced on January 1, 2018.
For each customer, select the CustomerId, RegistrationDate, and the form version the user filled in at the time of registration. Name this third column RegistrationForm.
```sql
select customerid, registrationdate, 
case
when registrationdate < '2017-03-14' then 'ver1'
when registrationdate < '2018-01-01' then 'ver2'
else 'ver3'
end as RegistrationForm
from customers
```
![image](https://user-images.githubusercontent.com/77920592/193342632-4c7653d1-8a63-4bec-a370-958f17647ce4.png)

Show two metrics in two different columns:
OrderOnRegistrationDate – the number of people who made their first order on their registration date.
OrderAfterRegistrationDate – the number of people who made their first order after their registration date.
```sql
select 
count(case 
      when datediff(day, registrationdate, firstorderdate) = 0
      then customerid end) as OrderOnRegistrationDate, 
count(case 
      when datediff(day, registrationdate, firstorderdate) >= 1
      then customerid end) as OrderAfterRegistrationDate
from customers
```
![image](https://user-images.githubusercontent.com/77920592/193342833-26182dce-622b-4ceb-bfc4-e0a73eca4b09.png)

Create a conversion chart for monthly registration cohorts. Show the following columns:
- Year
- Month
- RegisteredCount
- NoSale
- ThreeDays – the number of customers who made a purchase within 3 days from registration.
- FirstWeek – the number of customers who made a purchase during the first week but not within first three days.
- AfterFirstWeek – the number of customers who made a purchase after the 7th day.
Order the results by year and month.
```sql
select
datepart (year, registrationdate) as Year,
datepart (month, registrationdate) as Month, 
count(*) as RegisteredCount,
count (case
      when firstorderdate is null then customerid end) as NoSale,
count (case
      when datediff(day, registrationdate, firstorderdate) < 3 then customerid end) as ThreeDays,
count (case
      when datediff(day, registrationdate, firstorderdate) >= 3 and 
       datediff(day, registrationdate, firstorderdate) < 7 then customerid end) as FirstWeek,
count (case
      when datediff(day, registrationdate, firstorderdate) >= 7 then customerid end) as AfterFirstWeek
from customers
group by datepart (year, registrationdate), datepart (month, registrationdate)
order by datepart (year, registrationdate), datepart (month, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193342973-b176b72d-a0e8-4eb2-8c2a-9d61376d316b.png)

Create a conversion chart for monthly registration cohorts from 2017 for each channel. Show the following columns:
- Month – The registration month.
- ChannelName – The registration channel.
- RegisteredCount – The number of users registered.
- NoSale – The number of users who never made a purchase.
- OneWeek – The number of users who made a purchase within 7 days.
- AfterOneWeek – The numbers of users who made a purchase after the first week.
Order the results by month.
```sql
select
datepart (month, registrationdate) as Month, channelname,
count(*) as RegisteredCount,
count (case
      when firstorderdate is null then customerid end) as NoSale,
count (case
      when datediff(day, registrationdate, firstorderdate) < 7 then customerid end) as OneWeek,
count (case
      when datediff(day, registrationdate, firstorderdate) >= 7 then customerid end) as AfterOneWeek
from customers cu 
join channels ch on cu.channelid = ch.id
where registrationdate >= '2017-01-01' and registrationdate <= '2017-12-31' 
group by datepart (month, registrationdate), ch.id, channelname
order by datepart (month, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193343064-70271e56-10be-4e2a-9364-cc6b77e1e916.png)

## Customer Activity ##
### Number of active customers ###
For an e-store the definition of an "active customer" is not as straightforward. There are some customers who place orders every now and then, but there are also some who haven't been active for a long time. In our online supermarket, regular customers typically place one order a week, but we'll define "active customers" as all customers who've placed an order within the last 30 days. 
Find the number of active customers in each country. Show two columns: Country and ActiveCustomers. 
```sql
select country, count(customerid) as ActiveCustomers
from customers
where datediff(day, lastorderdate, getdate()) < 30
group by country
```
![image](https://user-images.githubusercontent.com/77920592/193419360-44981113-eaa3-450d-baba-7227e90c6102.png)

### Average order value ###
It's equally important to understand how much revenue our customers generate. We now want to know the average order value for each weekly registration cohort.
```sql
select datepart(week, registrationdate) as Week,
avg(totalamount) as AverageOrderValue
from customers cu
join orders o on cu.customerid = o.customerid
where registrationdate >= '2017-01-01' and registrationdate <= '2017-12-31'
and country = 'Germany'
group by datepart(week, registrationdate)
order by datepart(week, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193419656-16b97fe8-c9d8-48cf-88cc-2f07ea2f2a71.png)

### Average order values by customers ###
Each business will use its own definition of a good customer that is based on their business model. In our e-store, we'll define a "good customer" as a customer whose average order value is above the general average order value for all customers. Analyzing such customers may help us understand what makes customers spend more. This, in turn, can help us decide which marketing campaigns we should focus on.
```sql
select
  c.customerid,
  avg(totalamount) as AverageOrderValue
from customers c
join orders o
  on c.customerid = o.customerid
group by c.customerid
order by avg(totalamount);
```
![image](https://user-images.githubusercontent.com/77920592/193419724-df24e17e-8e51-4fc3-acc4-fa45e079b60c.png)

### Average order value per customer ###
Find each country's average order value per customer. Show two columns: Country and AvgOrderValue. Sort the results by average order value, in ascending order.
```sql
with TotalValue_cte as 
(
  select c.customerid, country, avg(totalamount) as TotalValue
  from orders o 
  join customers c on o.customerid = c.customerid
  group by c.customerid, country
)
select country, avg(TotalValue) as AvgOrderValue
from TotalValue_cte
group by Country
order by avg(TotalValue) asc
```
![image](https://user-images.githubusercontent.com/77920592/193420073-423d4df1-d4be-4c45-91e6-42ad680c9784.png)

Find out the average number of orders placed in the last 180 days by customers who have been active (made a purchase) in the last 30 days. Name the column AvgOrders180. Make sure that your average isn't integer.
```sql
with TotalOrders_cte as 
(
  select customerid, count(orderid) as TotalOrders from orders o
  where datediff(day, orderdate, getdate()) < 180
  group by customerid
)
select avg(1.0 * TotalOrders) as AvgOrders180
from TotalOrders_cte toc
join customers c on toc.customerid = c.customerid
where datediff(day, lastorderdate, getdate()) < 30
```
![image](https://user-images.githubusercontent.com/77920592/193420304-c6c6b08e-1557-4dab-86db-b78d81fe7117.png)

### Above average order values ###
The average order value per customer in Italy is 1905.9063. Now, for each Italian customer with an average order value above that, show the following columns: CustomerID, FullName, and AvgOrderValue. Order the results by average order value, in descending order.
```sql
select  c.customerid, c.fullname, avg(totalamount) as AvgOrderValue
from orders o 
join customers c on c.customerid = o.customerid
where country = 'Italy'
group by c.customerid, c.fullname
having avg(totalamount) > 1905.9063
order by avg(totalamount) desc
```
![image](https://user-images.githubusercontent.com/77920592/193420578-acfe4183-504b-43b6-b505-487516006a37.png)

### Good customers in weekly cohorts ###
Show the number of good customers in quarterly registration cohorts. Display the following columns: Year, Quarter, and GoodCustomers. Order the results by year and quarter.
```sql
with AvgOrderValue_cte as
(  
  select  c.customerid, c.fullname, c.registrationdate, c.country, avg(totalamount) as AvgOrderValue
  from orders o 
  join customers c on c.customerid = o.customerid
  group by c.customerid, c.fullname, c.registrationdate, c.country
  having avg(totalamount) > 1905.9063
)
select  
datepart(year, registrationdate) as Year,
datepart(quarter, registrationdate) as Quarter, count(*) as GoodCustomers, country
from AvgOrderValue_cte
group by datepart(year, registrationdate), datepart(quarter, registrationdate), country
order by datepart(year, registrationdate), datepart(quarter, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193421012-36574f34-c788-4d4c-9502-6eaa4e9a26bd.png)

### Finding good customers ###
Find the number of good customers (defined as those with an average order value greater than 1500.00) in weekly registration and city cohorts (i.e., cohorts defined by both weekly registration and the customer's city). Show the following columns: Year, Week, City, and GoodCustomers. Order the results by year and week
```sql
with AvgOrderValue_cte as
(  
  select  c.customerid, c.fullname, c.registrationdate, c.city, avg(totalamount) as AvgOrderValue
  from orders o 
  join customers c on c.customerid = o.customerid
  group by c.customerid, c.fullname, c.registrationdate, c.city
  having avg(totalamount) > 1500.00
)
select  
datepart(year, registrationdate) as Year,
datepart(week, registrationdate) as Week, count(*) as GoodCustomers, city
from AvgOrderValue_cte
group by datepart(year, registrationdate), datepart(week, registrationdate), city
order by datepart(year, registrationdate), datepart(week, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193421295-75f27bd8-f79d-48f9-99d0-ffcaef8c68e3.png)

For each month of 2017, show the number of active customers in monthly registration cohorts. Define an active customer as a customer that has placed an order in the last 60 days. Show two columns: Month and ActiveCustomers. Order the results by month.
```sql
select datepart(month, registrationdate) as Month, 
count (customerid) as ActiveCustomers
from customers
where datediff(day, lastorderdate, getdate()) < 60 and
registrationdate > '2017-01-01' and registrationdate < '2017-12-31'
group by datepart(month, registrationdate)
order by datepart(month, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193421698-f2734f48-5251-4c5d-bcb8-843235412c9d.png)

## Customer Churn ##
Inevitably, customers will stop using our services at some point. There can be many reasons for this: they may want to go to our competitors, or they may simply no longer need our services. This phenomenon is called "customer churn." On the other hand, "customer retention" is when we've succeeded in keeping a customer active during a given period.

### Churned customers in weekly cohorts ###
Find the number of churned customers in monthly registration cohorts from 2017. In this exercise, churned customers are those who haven't placed an order in more than 45 days. Show the following columns: Month and ChurnedCustomers. Order the results by month.
```sql
select datepart(month, registrationdate) as Month,
count(*) as ChurnedCustomers
from customers
where datediff(day, lastorderdate, getdate()) > 45 and
registrationdate >= '2017-01-01' and registrationdate <= '2017-12-31'
group by datepart(month, registrationdate)
order by datepart(month, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193423913-111c884e-ebf4-457a-b379-4d2ead281583.png)

### Percentage of churned customers in weekly cohorts ###
Calculate the percentage of churned customers in the cohort by dividing the number of churned customers by the number of all customers. 
```sql
select datepart(month, registrationdate) as Month,
count(customerid) as AllCustomers,
count(case when datediff(day, lastorderdate, getdate()) > 45 then customerid end) as ChurnedCustomers,
count(case when datediff(day, lastorderdate, getdate()) > 45 then customerid end) * 100.0 / count(customerid) as ChurnedPercentage 
from customers
where registrationdate >= '2017-01-01' and registrationdate <= '2017-12-31'
group by datepart(month, registrationdate)
order by datepart(month, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193424098-7ede32d0-80e6-41a9-ae11-3d9d6f293919.png)

### The customer retention chart ###
Create a customer retention chart for weekly signup cohorts from 2017. Show the following columns: Week, PercentActive10d, PercentActive30d, and PercentActive60d. For each weekly registration cohort, we want to see the percentage of customers still active 30, 60, and 90 days after the registration date. Order the results by week.
```sql
select
  datepart(week, registrationdate) as Week,
  count(case when datediff(day, registrationdate, lastorderdate) > 10 then customerid end) * 100.0 / count(customerid) as PercentActive10d,
  count(case when datediff(day, registrationdate, lastorderdate) > 30 then customerid end) * 100.0 / count(customerid) as PercentActive30d,
  count(case when datediff(day, registrationdate, lastorderdate) > 60 then customerid end) * 100.0 / count(customerid) as PercentActive60d
from customers
where registrationdate >= '2017-01-01' and registrationdate <= '2017-12-31'
group by datepart(week, registrationdate)
order by datepart(week, registrationdate)
```
![image](https://user-images.githubusercontent.com/77920592/193424212-be228748-f2dd-4966-95ab-c406449c3bf9.png)

###  ###
```sql
```

###  ###
```sql
```

###  ###
```sql
```

###  ###
```sql
```
