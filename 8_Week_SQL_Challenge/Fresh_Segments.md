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

```sql
with cte as
(
select interest_id, count(distinct _month_year) as Count_month
from interest_metrics
group by interest_id
having count(distinct _month_year) >= 6
)
select * into #filtered_table
from interest_metrics
where interest_id in (select interest_id from cte);

select * from #filtered_table;
```
![image](https://user-images.githubusercontent.com/77920592/200119992-ca53ebcd-a532-4baf-ac53-2749b0669817.png)

```sql
select top 10 _month_year, datepart(month, _month_year) as month, 
interest_id, interest_name, round(max(composition),2) as MaxComp
from #filtered_table ft join interest_map map
on ft.interest_id = map.id
group by _month_year, datepart(month, _month_year), interest_id, interest_name
order by max(composition) desc
```
![image](https://user-images.githubusercontent.com/77920592/200120029-10d9dd1b-df76-488c-b86f-8ba0f9b9472d.png)

```sql
select top 10 _month_year, datepart(month, _month_year) as month, 
interest_id, interest_name, round(max(composition),2) as MaxComp
from #filtered_table ft join interest_map map
on ft.interest_id = map.id
group by _month_year, datepart(month, _month_year), interest_id, interest_name
order by max(composition) asc
```
![image](https://user-images.githubusercontent.com/77920592/200120090-0b3a1024-9474-4fcf-ab1c-d9808a273c55.png)

### Which 5 interests had the lowest average ranking value? ###
```sql
with cte as
(
select interest_id, interest_name, round(avg(ranking),2) as AvgRanking
from #filtered_table ft join interest_map map
on ft.interest_id = map.id
group by interest_id, interest_name
)
select top 5 interest_id, interest_name, min(AvgRanking) as MinRanking
from cte 
group by interest_id, interest_name
order by min(AvgRanking) desc
```
![image](https://user-images.githubusercontent.com/77920592/200120105-b7208896-7306-4df5-96e7-8702dde1be96.png)

### Which 5 interests had the largest standard deviation in their percentile_ranking value? ###
```sql
select top 5 interest_id, interest_name, round(stdev(percentile_ranking),2) as Stdev_Perc
from #filtered_table ft join interest_map map
on ft.interest_id = map.id
group by interest_id, interest_name
order by stdev(percentile_ranking) desc
```
![image](https://user-images.githubusercontent.com/77920592/200120121-8734ee28-1b21-4d48-936e-d4d721dc0c35.png)

### For the 5 interests found in the previous question - what was minimum and maximum percentile_ranking values for each interest and its corresponding year_month value? Can you describe what is happening for these 5 interests? ###
```sql
with cte as
(
select top 5 interest_id, interest_name, round(stdev(percentile_ranking),2) as Stdev_Perc
from #filtered_table ft join interest_map map
on ft.interest_id = map.id
group by interest_id, interest_name
order by stdev(percentile_ranking) desc
),
cte2 as 
(
select met._month_year, cte.interest_id, cte.interest_name, met.percentile_ranking,
rank() over (partition by cte.interest_id, cte.interest_name 
			 order by percentile_ranking asc) as Min_Perc_Rank, 
rank() over (partition by cte.interest_id, cte.interest_name 
			 order by percentile_ranking desc) as Max_Perc_Rank
from cte join interest_metrics met
on cte.interest_id = met.interest_id
group by met._month_year, cte.interest_id, cte.interest_name, percentile_ranking
)
select cte2._month_year, cte2.interest_id, cte2.interest_name, cte2.percentile_ranking,
Min_Perc_Rank, Max_Perc_Rank, Stdev_Perc
from cte2 join cte on cte2.interest_id = cte.interest_id
where Min_Perc_Rank = 1 or Max_Perc_Rank = 1
group by cte2._month_year, cte2.interest_id, cte2.interest_name, 
		 percentile_ranking, Min_Perc_Rank, Max_Perc_Rank, Stdev_Perc
order by cte2.interest_id, cte2.interest_name
```
![image](https://user-images.githubusercontent.com/77920592/200120137-8c9f76fe-e720-44d3-a285-e002ee871d79.png)

### How would you describe our customers in this segment based off their composition and ranking values? What sort of products or services should we show to these customers and what should we avoid?  ###

The composition values tell that majority of the customers might be adults with high interest in travelling based on the content Work Comes First Travelers. 
Travelling content should be shown more to the customers while avoiding the sports and ganes related content. 

## Index Analysis ##

The index_value is a measure which can be used to reverse calculate the average composition for Fresh Segments’ clients.

Average composition can be calculated by dividing the composition column by the index_value column rounded to 2 decimal places.

### What is the top 10 interests by the average composition for each month? ###
```sql
with cte as
(
select _month_year, 
interest_id, interest_name, round((composition/index_value),2) as AvgComp,
rank() over (partition by _month_year 
			 order by (composition/index_value) desc) as Rank
from interest_metrics met join interest_map map
on met.interest_id = map.id
group by _month_year, interest_id, interest_name, composition, index_value
)
select * from cte
where Rank <= 10 
```
![image](https://user-images.githubusercontent.com/77920592/200349206-c27cbb0b-8540-4df6-b3ee-80b359996c8b.png)

### For all of these top 10 interests - which interest appears the most often? ###
```sql
with cte as
(
select _month_year, 
interest_id, interest_name, round((composition/index_value),2) as AvgComp,
rank() over (partition by _month_year 
			 order by (composition/index_value) desc) as Rank
from interest_metrics met join interest_map map
on met.interest_id = map.id
group by _month_year, interest_id, interest_name, composition, index_value
), 
cte2 as
(
select * from cte
where Rank <= 10 
)
select interest_id, interest_name, count(interest_name) as Count
from cte2
group by interest_id, interest_name
order by count desc
```
![image](https://user-images.githubusercontent.com/77920592/200349150-14b1b07d-ccd8-46c9-9d1d-235c4bc3e2c2.png)

### What is the average of the average composition for the top 10 interests for each month? ###
```sql
with cte as
(
select _month_year, 
interest_id, interest_name, round((composition/index_value),2) as AvgComp,
row_number() over (partition by _month_year
			 order by (composition/index_value) desc) as Rank
from interest_metrics met join interest_map map
on met.interest_id = map.id
)
select _month_year, round(avg(AvgComp),2) as AvgAvgComp from cte
where Rank <= 10 
group by _month_year
order by _month_year
```
![image](https://user-images.githubusercontent.com/77920592/200349103-080b70e6-0d83-4c9c-84cf-1f7388a19106.png)

### What is the 3 month rolling average of the max average composition value from September 2018 to August 2019 and include the previous top ranking interests in the same output shown below. ###
```sql
with cte as
(
select _month_year,  
interest_id, interest_name, round((composition/index_value),2) as AvgComp,
row_number() over (partition by _month_year
			 order by (composition/index_value) desc) as Rank
from interest_metrics met join interest_map map
on met.interest_id = map.id
),
cte2 as
(
select _month_year, interest_id, interest_name, AvgComp as MaxComp,
round(avg(AvgComp) over(order by _month_year 
						rows between 2 preceding and current row),2) as [3_mth_rolling]
from cte
where rank = 1 
group by _month_year, interest_id, interest_name, AvgComp
),
cte3 as
(
select *, lag(interest_name, 1) over (order by _month_year) as [int_1_mth_ago],
lag(interest_name, 2) over (order by _month_year) as [int_2_mth_ago],
lag(MaxComp, 1) over (order by _month_year) as [1_mth_ago],
lag(MaxComp, 2) over (order by _month_year) as [2_mth_ago]
from cte2
)
select _month_year, interest_name, MaxComp, [3_mth_rolling],
(int_1_mth_ago + ': ' + cast([1_mth_ago] as varchar)) AS [1_month_ago],
(int_2_mth_ago + ': ' + cast([2_mth_ago] as varchar)) AS [2_month_ago]
from cte3
where _month_year >= '2018-09-01' and _month_year <= '2019-08-31'
```
![image](https://user-images.githubusercontent.com/77920592/200348935-6b4af03a-6ff0-4998-b5a9-c9b52ec6043a.png)

### Provide a possible reason why the max average composition might change from month to month? Could it signal something is not quite right with the overall business model for Fresh Segments? ###

Change of the seasons might be the reasons behind the changing max average composition, proven by the highest interest in the travelling content, where periods before school holidays or any festive seasons might increase the average composition of travelling content significantly, while reducing the rest.  
