## Description ##

This is a demo of the school database application. It contains of 6 tables consisting of data from different departments.

The tasks include but not limited to:
- Design, develop, and test database and database objects (tables, views, stored procedures, indexes, functions, constraints)
- Build complex queries using T-SQL command
- Extract, transform and load the data from multiple sources and store them inside data warehouse using SSIS packages 

## Tables ##
The database contains 6 tables:
| Table Name| Columns |
| ------------- | ------------- |
|**Exam**|excode, extitle, exlocation, exdate, extime|
|**Student**|sno, sname, semail|
|**Entry**|eno, excode, sno, egrade|
|**Cancel**|sno, excode, sno, cdate, cuser|
|**Result**|excode, sno, grade_title, egrade|
|**Exam Details**|excode, extitle, exlocation, exdate, extime, sno, sname, egrade|
