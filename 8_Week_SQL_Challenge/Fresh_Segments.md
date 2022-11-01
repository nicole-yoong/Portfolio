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

### What do you think we should do with these null values in the fresh_segments.interest_metrics  ###
### How many interest_id values exist in the fresh_segments.interest_metrics table but not in the fresh_segments.interest_map table? What about the other way around?  ###
### Summarise the id values in the fresh_segments.interest_map by its total record count in this table  ###
### What sort of table join should we perform for our analysis and why? Check your logic by checking the rows where interest_id = 21246 in your joined output and include all columns from fresh_segments.interest_metrics and all columns from fresh_segments.interest_map except from the id column.  ###
### Are there any records in your joined table where the month_year value is before the created_at value from the fresh_segments.interest_map table? Do you think these values are valid and why?  ###

## Interest Analysis ##

### Which interests have been present in all month_year dates in our dataset?  ###
### Using this same total_months measure - calculate the cumulative percentage of all records starting at 14 months - which total_months value passes the 90% cumulative percentage value?  ###
### If we were to remove all interest_id values which are lower than the total_months value we found in the previous question - how many total data points would we be removing?  ###
### Does this decision make sense to remove these data points from a business perspective? Use an example where there are all 14 months present to a removed interest example for your arguments - think about what it means to have less months present from a segment perspective.  ###
### After removing these interests - how many unique interests are there for each month?  ###

## Segment Analysis ##

### Using our filtered dataset by removing the interests with less than 6 months worth of data, which are the top 10 and bottom 10 interests which have the largest composition values in any month_year? Only use the maximum composition value for each interest but you must keep the corresponding month_year ###
### Which 5 interests had the lowest average ranking value? ###
### Which 5 interests had the largest standard deviation in their percentile_ranking value? ###
### For the 5 interests found in the previous question - what was minimum and maximum percentile_ranking values for each interest and its corresponding year_month value? Can you describe what is happening for these 5 interests?  ###
### How would you describe our customers in this segment based off their composition and ranking values? What sort of products or services should we show to these customers and what should we avoid?  ###

## Index Analysis ##
The index_value is a measure which can be used to reverse calculate the average composition for Fresh Segments’ clients.

Average composition can be calculated by dividing the composition column by the index_value column rounded to 2 decimal places.

### What is the top 10 interests by the average composition for each month? ###
### For all of these top 10 interests - which interest appears the most often? ###
### What is the average of the average composition for the top 10 interests for each month? ###
### What is the 3 month rolling average of the max average composition value from September 2018 to August 2019 and include the previous top ranking interests in the same output shown below. ###
### Provide a possible reason why the max average composition might change from month to month? Could it signal something is not quite right with the overall business model for Fresh Segments? ###
