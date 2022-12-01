# Tables #

## A. Exam
**Create exam table**

```sql
CREATE TABLE exam (
    excode       CHAR(4),
    extitle      VARCHAR(20),
    exlocation   VARCHAR(20),
    exdate       DATE CHECK(exdate between '2022-06-01' and '2022-06-30'),
    extime       TIME CHECK(extime between '09:00:00' and '18:00:00'),
    PRIMARY KEY (excode)	
);
```

## B. Student 
**Create student table**

```sql
CREATE TABLE student (
    sno          INTEGER IDENTITY(1,1),
    sname        VARCHAR(20),
    semail       VARCHAR(20),
    PRIMARY KEY (sno),
    UNIQUE (semail)
);
```

## C. Enty
**Create entry table**
```sql
CREATE TABLE entry (
    eno          INTEGER IDENTITY(1,1),
    excode       CHAR(4) not null,
    sno          INTEGER,
    egrade       DECIMAL(5,2) CHECK(egrade between 0 and 100),
    PRIMARY KEY (eno),
    FOREIGN KEY (excode) REFERENCES exam(excode),
    FOREIGN KEY (sno) REFERENCES student(sno) ON DELETE CASCADE,
    UNIQUE (excode,sno)
);
```

## D. Cancel
**Create cancel table**

```sql
CREATE TABLE cancel (
    eno          INTEGER,
    excode       CHAR(4),
    sno          INTEGER,
    cdate        DATETIME,
    cuser        VARCHAR(128)
    PRIMARY KEY (eno, cdate)
);    
```
## E. Result ##
**Create result table**
```sql
CREATE TABLE result (
    excode       CHAR(4),
    sno          INTEGER,
    grade_title  VARCHAR(20),
    egrade		 DECIMAL);
```

## F. Exam Details
**Create exam_details table**

```sql
CREATE TABLE exam_details ( 
    excode       CHAR(4), 
    extitle      VARCHAR(20), 
    exlocation   VARCHAR(20), 
    exdate       DATE, 
    extime       TIME, 
    sno          INTEGER, 
    sname        VARCHAR(20), 
    egrade       DECIMAL(5,2)
    PRIMARY KEY (excode, sno)
); 		
```

