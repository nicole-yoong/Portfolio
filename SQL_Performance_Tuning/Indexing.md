# What is Indexes? #
Indexes are special structures used to quickly locate certain rows. Indexes are most often used when you run SQL queries (SELECT statements) that look for rows matching given criteria.
It helps retrieve data faster, but with slower insertion, modification and deletion because it takes up additional space on the hard drive and reduce the speed
Reading from indexes is very quick. But each time you create, modify, or delete a row, you also need to modify the entire tree structure. This takes time and slows down the operation.

## Basic Syntax for Creating Indexes ##

### B-trees Indexes ###

![image](https://user-images.githubusercontent.com/77920592/193803423-f913f8ed-c4ec-4188-ac68-2a505b894d79.png)

We've got ten players in the player table. Each player has a points total ranging from 1 to 42.

Suppose we've got the following query:
```sql
select * from player
where points = 30;
```
The database first looks at the top level of the tree: there are the numbers 13 and 30. The pink circles are used to move downwards. 
Which route should we take? Since we're looking for players with 30 points, we choose the rightmost circle and go deeper.
We're now at level two and we can see a single number: 38. The circle to the left will take us to players with less than 38 points. The circle to the right will take us to players with at least 38 points. As we're looking for players with 30 points, we're taking the left circle, going deeper... and there we go! 
At the lowest level, we can find a single row with exactly 30 points (a player with the nickname 'shadow'). We can return that row and finish the query.

![image](https://user-images.githubusercontent.com/77920592/193804237-5d7abaca-e303-45fa-bd66-f2f9b5fc5258.png)

### B+trees Indexes ###

B+trees are very similar to B-trees, but they have an additional feature: each row points to the next row and the previous row. This allows us to easily move from one leaf node (one actual row) to another.

![image](https://user-images.githubusercontent.com/77920592/193804367-82576f76-b8b2-4145-b1ab-89cea811e469.png)

Suppose we've got the following query:
```sql
select nick, points from player
where points > 9
order by points;
```

Now we look for a range of values in the points column. We also want to sort the rows. 
In this case, rows are sorted in ascending order by points.
If we want to find the row(s) that satisfy the condition points > 9, we simply need to find the first row with more than nine points.
All we need to do is retrieve the remaining rows and show them in the same order in the result set.

### Indexes on VARCHAR columns ###

An index on VARCHAR columns has limited usage. It can be used with WHERE clause and LIKE operator.

![image](https://user-images.githubusercontent.com/77920592/193806519-93426c28-35bf-4564-a499-388d208292a2.png)

Suppose we've got the following query:
 ```sql
select * from player
where country = 'Portugal';
 ```

Scenario 1: LIKE 'P%' >>> The index can quickly find rows where the country value starts with the letter 'P', since 'P' appears before the wildcard. All such rows where the country name begins with a P are returned because all of them match the criterion.
Scenario 2: LIKE 'P%d' >>> The index can only find rows with countries starting with 'P'. Then, the database needs to manually check these rows and return the ones that end with a 'd'.
Scenario 3: LIKE '%es' >>> The wildcard appears as the first letter, the index on country is of no use. The database has to check every row individually.

### Multi-columns Indexes ###

Example 1:

```sql
create table player (
  id integer primary key,
  first_name varchar(64),
  last_name varchar(64),
  year_born integer,
  country varchar(64),
  current_points integer
);
```

To show the user ranking for each country, we'll need to filter and/or sort rows by two columns: country and current_points.
Creating two indexes – one for country and one for current_points – isn't optimal. What we can do instead is create a multi-column index (aka a composite or concatenated index):

```sql
create index player_multi_country_points_index
on player(country, current_points);
```

The order of index does matter. When this index is created, all rows in the index are sorted first by country and then by current_points.
The image below shows how and when the index is used in the above queries:

![image](https://user-images.githubusercontent.com/77920592/193809300-431051db-1f0d-4719-9978-3e79fd89f1fb.png)

Always think about the order of columns in an index. Start with the column you'll be most likely to use when searching for values or ordering rows.

To deliver rows in a specific order, we can specify ASC or DESC.

```sql
create index player_multi_country_points_index
on player(country asc, current_points desc);
```

![image](https://user-images.githubusercontent.com/77920592/193809596-1a34e45e-e348-49b3-9fea-3f22b1c16d79.png)

### NULLS FIRST and NULLS LAST ###

By default, NULL values appear last when sorting rows in ascending order; they appear first when sorting rows in descending order. 
When we create an index for country and current_points, we can specify where NULL values should appear by adding NULLS FIRST or NULLS LAST:

```sql
create index player_multi_country_points_index
on player(country, current_points desc nulls last);
```
In the index above, NULL values in current_points will appear last, even though the index uses descending order.

### Deleting Indexes ###

```sql
drop index points_index;
```

## When to Create Indexes? ##
Making changes to indexes can take much longer than making changes to the actual data. 
That's why we should never create indexes "in advance." Instead, we should only create them when we see a real performance problem.

### Automatic Indexing on Primary Keys ###

B-tree index will be created automatically on the primary key. 
If the primary key is a single column, we'll get a single-column index. If the primary key is made up of multiple columns, we'll get a multi-column index.

 ```sql
 create table invoice (
  id integer primary key,
  issue_date date,
  customer_id integer,
  amount decimal(10, 2),
  currency char(3)
);
```

To check indexes:
```sql
select indexname
from pg_indexes
where tablename = 'invoice';
```

![image](https://user-images.githubusercontent.com/77920592/193810731-d7191dd7-0dff-4df9-9234-719f0eb5f2e2.png)

### Automatic Indexing on Unique Constraints ###

Besides, B-tree index will be created automatically on the unique constraints. 

```sql
 create table invoice (
  id integer primary key,
  number varchar(18) unique,
  issue_date date,
  customer_id integer,
  amount decimal(10, 2),
  currency char(3)
);
```

To check indexes:
```sql
select indexname
from pg_indexes
where tablename = 'invoice';
```

![image](https://user-images.githubusercontent.com/77920592/193811060-1d698059-e7c6-4123-a997-8597b0414ac2.png)

### Enforcing Unique Constraints ###

A UNIQUE index works just like a UNIQUE constraint – it makes sure no duplicate values are allowed in that column.
We use CREATE UNIQUE INDEX instead of CREATE INDEX.

```sql
create unique index name_unique_index
on subway_station(name);
```

However, enforcing UNIQUEness with UNIQUE indexes isn't recommended. 
Even though this syntax exists, the vast majority of database developers use UNIQUE constraints instead.

### Indexes on Date Columns ###

Even though we shouldn't create too many indexes for performance reasons, we typically consider date columns as good candidates for indexes. 
In many real-life situations, date columns are frequently used to filter rows. 

```sql
create table passenger_count (
  id integer primary key,
  line varchar(3),
  day date,
  count integer
);
```

```sql
create index count_day_index
on passenger_count(day);
```

The table above contains the daily number of passengers travelling on a given subway line. The day column is a good candidate for an index – we'll probably want to filter rows based on time ranges quite often. 

### Deleting and Recreating Indexes ###

Imagine the following situation: You have a table with lots of data and a few indexes. You have to update most of the rows in the table, and you're afraid that updating the indexes will take a really long time. What to do?
A frequent trick used by database developers is to first delete all existing indexes, then update the data, and finally create the indexes again. 
This way, the database will only have to create the indexes once, instead of modifying the structure of existing indexes for each update operation.

For example, we've found an error in the issue dates of most of the invoices in the table invoice:

```sql
 create table invoice (
  id integer primary key,
  number varchar(18) unique,
  issue_date date,
  customer_id integer,
  amount decimal(10, 2),
  currency char(3)
);
```

If we want to update most of the table's rows, we will need to delete all the indexes we created earlier on to avoid time-consuming execution.

### Truncating Tables ###

To delete all data from a table, we usually use DELETE FROM. However, this does not delete the actual table or the indexes.

```sql
delete from passenger_count;
```

Also, it'll be quite slow – the database engine will delete the rows one by one, and it'll have to update the indexes each time. Instead, we can use TRUNCATE FROM.
Just like DELETE FROM, the statement above will delete all data from the table passenger_count and keep the table structure and indexes up to date. However, it'll be much faster, as all rows will be deleted at once and the indexes will become empty.

```sql
truncate table passenger_count;
```

TRUNCATE TABLE is much faster than DELETE FROM, but it has its limitations: You can't use a WHERE clause with TRUNCATE TABLE, and in most databases it won't work if you have foreign keys in your table.

## Indexing Problems ##




