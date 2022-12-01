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

# Sample Data Insertion #

INSERT INTO exam VALUES 
    ('VB01', 'Visual Basic 1', 'London', '2022-06-01', '09:00'),
    ('VB02', 'Visual Basic 2', 'London', '2022-06-02', '18:00'),
    ('SQL1', 'SQL 1', 'Norwich', '2022-06-01', '09:00'),
    ('XQ02', 'Xquery 2', 'Norwich', '2022-06-03', '09:00'),
    ('PMAN', 'Project Management', 'London', '2022-06-04', '09:00');

INSERT INTO student VALUES
    ('Smith, A.', 'bj@myhome.com'),
    ('Brown, B.', 'bb@myhome.com'),
    ('Green, C.', 'cg@myhome.com'),
    ('White, D.', 'dw@myhome.com'),
    ('Young, E.', 'ey@myhome.com');
    
INSERT INTO entry(excode, sno)
    VALUES ('VB01', 1);
INSERT INTO entry(excode, sno)
    VALUES ('VB02', 1);   
INSERT INTO entry(excode, sno)
    VALUES ('XQ02', 1);
INSERT INTO entry(excode, sno)
    VALUES ('PMAN', 1);
INSERT INTO entry(excode, sno)
    VALUES ('SQL1', 2);
INSERT INTO entry(excode, sno)
    VALUES ('VB02', 2);
INSERT INTO entry(excode, sno)
    VALUES ('XQ02', 2);
INSERT INTO entry(excode, sno)
    VALUES ('PMAN', 2);
INSERT INTO entry(excode, sno)
    VALUES ('VB01', 3);
    
UPDATE entry SET egrade = 50
WHERE eno = 19;

UPDATE entry SET egrade = 55
WHERE eno = 20;

UPDATE entry SET egrade = 45
WHERE eno = 21;

UPDATE entry SET egrade = 50
WHERE eno = 22;

UPDATE entry SET egrade = 90
WHERE eno = 23;

UPDATE entry SET egrade = 20
WHERE eno = 24;
