# Case Study #8 - Fresh Segments #

![image](https://user-images.githubusercontent.com/77920592/199337145-c5e9eb60-a03e-41da-922d-184c359c5b3f.png)

# Introduction #

Danny created Fresh Segments, a digital marketing agency that helps other businesses analyse trends in online ad click behaviour for their unique customer base.

Clients share their customer lists with the Fresh Segments team who then aggregate interest metrics and generate a single dataset worth of metrics for further analysis.

In particular - the composition and rankings for different interests are provided for each client showing the proportion of their customer list who interacted with online assets related to each interest for each month.

Danny has asked for your assistance to analyse aggregated metrics for an example client and provide some high level insights about the customer list and their interests.

# Case Study Questions #

The following questions can be considered key business questions that are required to be answered for the Fresh Segments team.

Most questions can be answered using a single query however some questions are more open ended and require additional thought and not just a coded solution!

## Data Exploration and Cleansing ##

### Update the fresh_segments.interest_metrics table by modifying the month_year column to be a date data type with the start of the month ###
```sql
select cast(_year + '-' + _month + '-01' as date) as month_year
from interest_metrics
where month_year <> 'null'

alter table interest_metrics
add _month_year date null;

update interest_metrics
set _month_year = cast(_year + '-' + _month + '-01' as date)
where month_year <> 'null';

alter table interest_metrics
drop column month_year;
```

### What is count of records in the fresh_segments.interest_metrics for each month_year value sorted in chronological order (earliest to latest) with the null values appearing first?  ###
```sql
select _month_year, count(*) as Count
from interest_metrics
group by _month_year
order by _month_year asc
```
![image](https://user-images.githubusercontent.com/77920592/199477446-0b2abf2b-cef3-498f-ac33-ab69bea81d4c.png)

### What do you think we should do with these null values in the fresh_segments.interest_metrics  ###

Drop the rows with null interest_id as the information is not useful. 
```sql
delete from interest_metrics
where interest_id  = 'null';
```

### How many interest_id values exist in the fresh_segments.interest_metrics table but not in the fresh_segments.interest_map table? What about the other way around?  ###
```sql
select count(distinct interest_id) as Count
from interest_metrics
where not exists 
(select id from interest_map where id = interest_id)
```
![image](https://user-images.githubusercontent.com/77920592/199477600-8ee634c8-dd2f-49dd-8afd-7f74a42d74d0.png)

```sql
select count(distinct id) as Count
from interest_map
where not exists 
(select interest_id from interest_metrics where id = interest_id)
```
![image](https://user-images.githubusercontent.com/77920592/199477691-305de677-1d40-4788-be02-3b62c7a8533f.png)

### Summarise the id values in the fresh_segments.interest_map by its total record count in this table  ###
```sql
select id, interest_name, count(*) as Count
from interest_metrics met join interest_map map
on met.interest_id = map.id
group by id, interest_name
order by count desc
```
![image](https://user-images.githubusercontent.com/77920592/199477742-e108cbdd-ac89-493b-8c61-ec286751a905.png)

### What sort of table join should we perform for our analysis and why? Check your logic by checking the rows where interest_id = 21246 in your joined output and include all columns from fresh_segments.interest_metrics and all columns from fresh_segments.interest_map except from the id column.  ###

Inner join

```sql
select _month, _year, interest_id, composition, index_value, ranking, percentile_ranking,
_month_year, interest_name, interest_summary, created_at, last_modified
from interest_metrics met join interest_map map
on met.interest_id = map.id
where interest_id = 21246
```
![image](https://user-images.githubusercontent.com/77920592/199477851-fd4dc65d-69f2-4fbf-ba28-53804298b597.png)

### Are there any records in your joined table where the month_year value is before the created_at value from the fresh_segments.interest_map table? Do you think these values are valid and why?  ###

Make sense because they are of same month and we have set the start date of each _month_year to the first day.

```sql
select count(*) as Count
from interest_metrics met join interest_map map
on met.interest_id = map.id
where _month_year < created_at
```
![image](https://user-images.githubusercontent.com/77920592/199478069-298d01b5-d5b1-4c1c-b362-d36f88653788.png)

```sql
select id, interest_name, _month_year, created_at
from interest_metrics met join interest_map map
on met.interest_id = map.id
where _month_year < created_at
```
![image](https://user-images.githubusercontent.com/77920592/199478172-eb905243-e884-44c7-856d-675f6526f06c.png)

## Interest Analysis ##

### Which interests have been present in all month_year dates in our dataset?  ###
```sql
select count(distinct _month_year) as Count_month,
count (distinct interest_id) as Count_interestid
from interest_metrics;
```
![image](https://user-images.githubusercontent.com/77920592/199478260-08bc131d-21e4-4fc9-a6b8-60f15b42ebf4.png)

```sql
with cte as
(
select interest_id, count(distinct _month_year) as Count_month
from interest_metrics
group by interest_id
)

select count(*) as Count from cte
where count_month = 14
```
![image](https://user-images.githubusercontent.com/77920592/199478316-fa0b9c77-9ccf-4c3f-ba61-fb86a22b1520.png)

### Using this same total_months measure - calculate the cumulative percentage of all records starting at 14 months - which total_months value passes the 90% cumulative percentage value?  ###

Interest below 6 months have a cumulative percentage of over 90%.

```sql
with cte as
(
select interest_id, count(distinct _month_year) as Count_month
from interest_metrics
group by interest_id
),
cte2 as 
(
select count_month, count(*) as Count from cte
group by count_month
)
select count_month, count, 
round(sum(count) over(order by count_month desc) * 100.0/ 
sum(count) over (),2) as cumulative
from cte2
group by count_month, count
```
![image](https://user-images.githubusercontent.com/77920592/200117547-0d582416-10dc-4526-b3c5-2965fefa6c47.png)

### If we were to remove all interest_id values which are lower than the total_months value we found in the previous question - how many total data points would we be removing?  ###
```sql
with cte as
(
select interest_id, count(distinct _month_year) as Count_month
from interest_metrics
group by interest_id
having count(distinct _month_year) < 6
),
cte2 as 
(
select count(interest_id) as count
from interest_metrics
where interest_id in (select interest_id from cte)
)
select count(interest_id) as original, 
(select count from cte2) as to_remove, 
count(interest_id) - (select count from cte2) as to_remain
from interest_metrics
```
![image](https://user-images.githubusercontent.com/77920592/200117534-b06c6f8c-2afa-42b8-a2ec-8b02284222e1.png)

### Does this decision make sense to remove these data points from a business perspective? Use an example where there are all 14 months present to a removed interest example for your arguments - think about what it means to have less months present from a segment perspective.  ###

It makes sense. The percentage of interest_id count to be removed is not that significant and it helps attract more customers. 

```sql
with cte as
(
select interest_id, count(distinct _month_year) as Count_month
from interest_metrics
group by interest_id
having count(distinct _month_year) >= 6
)
select a._month_year, a.to_remain, b.to_remove, 
round((to_remove*100.0/to_remain),2) as to_remove_pct
from 
	(select _month_year, count(interest_id) as to_remain 
	from interest_metrics 
	where interest_id in (select interest_id from cte)
	group by _month_year) as a
join
	(select _month_year, count(interest_id) as to_remove 
	from interest_metrics 
	where interest_id not in (select interest_id from cte)
	group by _month_year) as b
on a._month_year = b._month_year
order by a._month_year
```
![image](https://user-images.githubusercontent.com/77920592/200118229-d24040bd-207d-430e-bad2-a7f9eb6e5ead.png)

### After removing these interests - how many unique interests are there for each month?  ###
```sql
with cte as
(
select interest_id, count(distinct _month_year) as Count_month
from interest_metrics
group by interest_id
having count(distinct _month_year) >= 6
)
select _month_year, count(distinct interest_id) as count
from interest_metrics
where interest_id in (select interest_id from cte)
group by _month_year
order by _month_year
```
![image](https://user-images.githubusercontent.com/77920592/200118321-c93c2a0e-817d-465a-b5f9-126779793f20.png)

## Segment Analysis ##

### Using our filtered dataset by removing the interests with less than 6 months worth of data, which are the top 10 and bottom 10 interests which have the largest composition values in any month_year? Only use the maximum composition value for each interest but you must keep the corresponding month_year ###

### Which 5 interests had the lowest average ranking value? ###

### Which 5 interests had the largest standard deviation in their percentile_ranking value? ###

### For the 5 interests found in the previous question - what was minimum and maximum percentile_ranking values for each interest and its corresponding year_month value? Can you describe what is happening for these 5 interests? ###

### How would you describe our customers in this segment based off their composition and ranking values? What sort of products or services should we show to these customers and what should we avoid?  ###

## Index Analysis ##

The index_value is a measure which can be used to reverse calculate the average composition for Fresh Segments’ clients.

Average composition can be calculated by dividing the composition column by the index_value column rounded to 2 decimal places.

### What is the top 10 interests by the average composition for each month? ###

### For all of these top 10 interests - which interest appears the most often? ###

### What is the average of the average composition for the top 10 interests for each month? ###

### What is the 3 month rolling average of the max average composition value from September 2018 to August 2019 and include the previous top ranking interests in the same output shown below. ###

### Provide a possible reason why the max average composition might change from month to month? Could it signal something is not quite right with the overall business model for Fresh Segments? ###
