## Customer Registration ##

### How many customers registered in the first six months of 2017? Name the column RegistrationCount. ###
```sql
select count(customerid) as RegistrationCount 
from customers
where registrationdate >= '20170101' and registrationdate <= '20170630'
```
or
```sql
select count(customerid) as RegistrationCount from customers
where registrationdate >= '20170101' 
and registrationdate < dateadd(month, 6,'20170101')
```

### Show the number of registrations in the current week. Name the column RegistrationsCurrentWeek. ###
```sql
select count(customerid) as RegistrationsCurrentWeek
from customers
where registrationdate >= dateadd(week, datediff(week, 0, getdate()), 0)
```

### We now want to find out how customer acquisition has changed over time. This will help us understand if we're currently attracting more users (or not). ###
### Create a report containing the 2017 monthly registration counts. Show the RegistrationMonth and RegistrationCount columns. Order the results by month. ###
```sql
select datepart(month, registrationdate) as RegistrationMonth,
count(customerid) as RegistrationCount
from customers
where registrationdate >= '2017-01-01' and registrationdate <= '2017-12-31'
group by datepart(month, registrationdate)
order by datepart(month, registrationdate)
```

### Find the registration count for each month in each year. Show the following columns: RegistrationYear, RegistrationMonth, and RegistrationCount. Order the results by year and month. ###
```sql
select datepart(month, registrationdate) as RegistrationMonth,
datepart(year, registrationdate) as RegistrationYear,
count(customerid) as RegistrationCount
from customers
group by datepart(year, registrationdate), datepart(month, registrationdate)
order by datepart(year, registrationdate), datepart(month, registrationdate)
```

### Find the registration count for each week in each year. Show the following columns: RegistrationYear, RegistrationWeek, and RegistrationCount. Order the results by the year and week. ###
```sql
select
  datepart(year, registrationdate) as registrationyear,
  datepart(week, registrationdate) as registrationweek,
  count(customerid) as registrationcount,
  min(registrationdate) as weeklabel
from customers
group by datepart(year, registrationdate), datepart(week, registrationdate)
order by datepart(year, registrationdate), datepart(week, registrationdate);

```

### Create an extended version of the report shown in the explanation. Instead of annual customer cohorts per channel, show weekly customer cohorts per channel in each year. Show the following columns: RegistrationYear, RegistrationWeek, ChannelName, and RegistrationCount. Order the results by year and week. ###
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

###  ###
```sql

```
## Conversion Rates ##

## Customer Activity ##

## Customer Churn ##
