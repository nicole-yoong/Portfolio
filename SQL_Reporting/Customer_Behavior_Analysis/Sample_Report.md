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

## Customer Churn ##
