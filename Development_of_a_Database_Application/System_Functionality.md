-- Insert tables into schema

```sql
CREATE TABLE exam (
    excode       CHAR(4),
    extitle      VARCHAR(20),
    exlocation   VARCHAR(20),
    exdate       DATE,
    extime       TIME);

CREATE TABLE student (
    sno          INTEGER,
    sname        VARCHAR(20),
    semail       VARCHAR(20));

CREATE TABLE entry (
    eno          INTEGER,
    excode       CHAR(4),
    sno          INTEGER,
    egrade       DECIMAL(5,2));
    
CREATE TABLE cancel (
    eno          INTEGER,
    excode       CHAR(4),
    sno          INTEGER,
    cdate        TIMESTAMP,
cuser        VARCHAR(128));   

CREATE TABLE result (
excode       CHAR(4),
sno          INTEGER,
    grade_title      VARCHAR(20),
    egrade   DECIMAL);

CREATE TABLE exam_details ( 

excode       CHAR(4), 
    extitle      VARCHAR(20), 
    exlocation   VARCHAR(20), 
    exdate       DATE, 
    extime       TIME, 
    sno          INTEGER, 
sname        VARCHAR(20), 
    egrade       DECIMAL(5,2)); 	
```

-- Set Entity Integrity Constraint 
```sql
ALTER TABLE exam
ADD CONSTRAINT PK_exam PRIMARY KEY (excode);

ALTER TABLE student
ADD CONSTRAINT PK_student PRIMARY KEY (sno);

ALTER TABLE entry
ADD CONSTRAINT PK_entry PRIMARY KEY (eno);

ALTER TABLE cancel
ADD CONSTRAINT PK_cancel PRIMARY KEY (eno,cdate);

ALTER TABLE entry 
ALTER COLUMN excode SET NOT NULL;

ALTER TABLE exam_details
ADD CONSTRAINT PK_exam_details PRIMARY KEY (excode,sno);

CREATE SEQUENCE eno_sequence
START 1
INCREMENT 1;

ALTER table entry
ALTER column eno SET DEFAULT nextval('eno_sequence');

CREATE SEQUENCE sno_sequence
START 1
INCREMENT 1;

ALTER table student
ALTER column sno SET DEFAULT nextval('sno_sequence');

ALTER SEQUENCE eno_sequence RESTART WITH 1;
UPDATE entry SET eno=nextval('eno_sequence');
```

-- Set Referential Constraint 
```sql
ALTER TABLE entry
ADD CONSTRAINT FK_exam FOREIGN KEY (excode) REFERENCES exam(excode);

ALTER TABLE entry
ADD CONSTRAINT FK_sno FOREIGN KEY (sno) REFERENCES student(sno) ON DELETE CASCADE;
```

-- Set Domain Constraint
```sql
CREATE DOMAIN domain_exdate AS DATE 
CHECK(value between date '2022-06-01' and date '2022-06-30');

ALTER TABLE exam  
ALTER COLUMN exdate
SET DATA TYPE domain_exdate;

CREATE DOMAIN domain_extime AS TIME
CHECK(value between time '09:00:00' and time '18:00:00');

ALTER TABLE exam  
ALTER COLUMN extime
SET DATA TYPE domain_extime;

CREATE DOMAIN domain_egrade AS DECIMAL
CHECK(value between decimal '0' and decimal '100');

ALTER TABLE entry 
ALTER COLUMN egrade
SET DATA TYPE domain_egrade;
```
-- Set Unique Constraint
```sql
ALTER TABLE student 
ADD CONSTRAINT email_constraint UNIQUE (semail);

ALTER TABLE entry 
ADD CONSTRAINT excode_sno_constraint UNIQUE (excode,sno);
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