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
    cdate        TIMESTAMP,
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

-- Delete entry and update the cancel table 
```sql
CREATE FUNCTION delete_entry_update_cancel() RETURNS TRIGGER AS $delete_entry_update_cancel$
   BEGIN
      INSERT INTO cancel(eno,excode,sno,cdate)VALUES (old.eno, old.excode, old.sno,now());
      RETURN NEW;
   END;
   
$delete_entry_update_cancel$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_delete_entry_update_cancel 
AFTER DELETE ON entry
FOR EACH ROW EXECUTE PROCEDURE delete_entry_update_cancel();
```

-- Retrieve grade_title, distinction, merit or pass  for all examinations
```sql
CREATE FUNCTION update_grade_title() RETURNS TRIGGER AS $update_grade_title$
   BEGIN
      INSERT INTO result(sno,excode,egrade)
	  VALUES (new.sno,new.excode,new.egrade);
      PERFORM egrade FROM entry WHERE sno = new.sno;
      IF FOUND THEN 
		  UPDATE result SET grade_title = 'DISTINCTION' 
		  WHERE egrade > 70 and sno = new.sno;
		  UPDATE result SET grade_title = 'PASS' 
		  WHERE (egrade < 70 and egrade > 50) and sno = new.sno;	
		  UPDATE result SET grade_title = 'FAIL' 
		  WHERE egrade < 50 and sno = new.sno;
	  END IF;
      RETURN NEW;
   END;
   
$update_grade_title$ LANGUAGE plpgsql;

CREATE TRIGGER update_grade_trigger
AFTER UPDATE ON entry
FOR EACH ROW EXECUTE PROCEDURE update_grade_title();
```

-- Retrieve grade_title, distinction, merit or pass based on excode 
```sql
CREATE OR REPLACE FUNCTION retrieve_result_on_excode(_excode CHAR(4))
RETURNS TABLE (
	sno	INTEGER,
    grade_title	VARCHAR(20),
    egrade   DECIMAL)
AS $$
	BEGIN		
		if egrade > 70 then
			grade_title := 'Distinction';
		elsif (egrade < 70 and egrade > 50) then
			grade_title := 'Merit';
		else
			grade_title := 'Fail';
		END IF;
		
		return query select sr.sno, sr.grade_title, sr.egrade from result AS sr where excode = _excode;
	END;
$$ LANGUAGE plpgsql;
```

-- Retrieve membership
```sql
CREATE FUNCTION update_exam_details() RETURNS TRIGGER AS $update_exam_details$ 
   BEGIN 
      INSERT INTO exam_details(excode,sno,egrade) 
  VALUES (new.excode,new.sno,new.egrade); 
      PERFORM extitle,exlocation,exdate,extime FROM exam WHERE excode = new.excode; 
      IF FOUND THEN  
  	UPDATE exam_details SET (extitle,exlocation,exdate,extime) = (select extitle,exlocation,exdate,extime from exam WHERE excode = new.excode) 
  	WHERE excode = new.excode; 
  END IF; 

   
  PERFORM sname FROM student WHERE sno = new.sno; 
      IF FOUND THEN  
  	UPDATE exam_details SET (sname) = (select sname from student WHERE sno = new.sno) 
  	WHERE sno = new.sno; 
  END IF; 

      RETURN NEW; 
   END; 

$update_exam_details$ LANGUAGE plpgsql; 


CREATE TRIGGER update_exam_details_trigger 
AFTER UPDATE ON entry 
FOR EACH ROW EXECUTE PROCEDURE update_exam_details();
```

-- Retrieve cancel based on the sno
```sql
CREATE OR REPLACE FUNCTION retrieve_student_cancel(_sno INTEGER)
RETURNS TABLE (
    eno          INTEGER,
    excode       CHAR(4),
    cdate        TIMESTAMP,
	cuser        VARCHAR(128)) 
AS $$
	BEGIN
		return query select cc.eno, cc.excode, cc.cdate, cc.cuser from cancel AS cc where sno = _sno;
	
	END;
$$ LANGUAGE plpgsql;
```

--- Insert values into tables and update values
```sql
INSERT INTO exam VALUES 
    ('VB01', 'Visual Basic 1', 'London', '2022-06-01', '09:00'),
    ('VB02', 'Visual Basic 2', 'London', '2022-06-02', '18:00'),
    ('SQL1', 'SQL 1', 'Norwich', '2022-06-01', '09:00'),
    ('XQ02', 'Xquery 2', 'Norwich', '2022-06-03', '09:00'),
    ('PMAN', 'Project Management', 'London', '2022-06-04', '09:00');

INSERT INTO student VALUES
    (100, 'Smith, A.', 'bj@myhome.com'),
    (200, 'Brown, B.', 'bb@myhome.com'),
    (300, 'Green, C.', 'cg@myhome.com'),
    (400, 'White, D.', 'dw@myhome.com'),
    (500, 'Young, E.', 'ey@myhome.com');

INSERT INTO entry(eno, excode, sno)
    VALUES ((SELECT COALESCE(MAX(eno),0) FROM entry) + 1, 'VB01', 100);
INSERT INTO entry(eno, excode, sno)
    VALUES ((SELECT COALESCE(MAX(eno),0) FROM entry) + 1, 'VB02', 100);   
INSERT INTO entry(eno, excode, sno)
    VALUES ((SELECT COALESCE(MAX(eno),0) FROM entry) + 1, 'XQ02', 100);
INSERT INTO entry(eno, excode, sno)
    VALUES ((SELECT COALESCE(MAX(eno),0) FROM entry) + 1, 'PMAN', 100);
INSERT INTO entry(eno, excode, sno)
    VALUES ((SELECT COALESCE(MAX(eno),0) FROM entry) + 1, 'SQL1', 200);
INSERT INTO entry(eno, excode, sno)
    VALUES ((SELECT COALESCE(MAX(eno),0) FROM entry) + 1, 'VB02', 200);
INSERT INTO entry(eno, excode, sno)
    VALUES ((SELECT COALESCE(MAX(eno),0) FROM entry) + 1, 'XQ02', 200);
INSERT INTO entry(eno, excode, sno)
    VALUES ((SELECT COALESCE(MAX(eno),0) FROM entry) + 1, 'PMAN', 200);
INSERT INTO entry(eno, excode, sno)
    VALUES ((SELECT COALESCE(MAX(eno),0) FROM entry) + 1, 'VB01', 300);

UPDATE entry SET
    egrade = 50
    WHERE eno = 1;

UPDATE entry SET
    egrade = 55
    WHERE eno = 2;

UPDATE entry SET
    egrade = 45
    WHERE eno = 3;

UPDATE entry SET
    egrade = 50
    WHERE eno = 4;

UPDATE entry SET
    egrade = 90
    WHERE eno = 5;

UPDATE entry SET
    egrade = 20
    WHERE eno = 6;
```
