## Insert students: Insert a new student member of the society. ##

**Insert a student with Student number: 600; Name= ‘Peterson, J’; email= ‘PeteJ@myhome.com’**

```sql
INSERT INTO student 
VALUES ('Peterson, J', 'PeteJ@myhome.com')

SELECT * FROM student
```
![image](https://user-images.githubusercontent.com/77920592/205054581-d42a37f1-6e1a-4532-90c3-79cff39fc1fc.png)

## Insert examinations: Insert a new examination for the coming year. ##

**Insert a exam with values:   Exam code : ‘VB03’; Exam title : ‘Visual Basic 3’; Exam location : ‘London’; Exam date : 2022-06-03 Exam time : 09:00**

```sql
INSERT INTO exam
VALUES ('VB03', 'Visual Basic 3', 'London', '2022-06-03', '09:00')

SELECT * FROM exam
```
![image](https://user-images.githubusercontent.com/77920592/205102055-bd2d135b-fe6e-44fa-9095-d58fadf05b79.png)

## Insert entry: Insert an examination entry ##

**Insert an entry with values:  Exam code : ‘VB03’ Exam title : Student number : ‘1’**

```sql
INSERT INTO entry (excode, sno)
VALUES ('VB03', '1')

SELECT * FROM entry
```
![image](https://user-images.githubusercontent.com/77920592/205102124-504189fa-72de-498a-a407-d16f9dc9812e.png)

## Update an entry: record the grade awarded to an entry. ##

**Update an entry with Entry number: ‘10’,  for ‘VB03’ and student number ‘100, (i.e.  the last entry you entered) with a grade ‘60’.**

```sql
UPDATE entry
SET egrade = 60 WHERE eno = 28 AND excode = 'VB03'

SELECT * FROM entry
```
![image](https://user-images.githubusercontent.com/77920592/205102195-3f1790ed-ed1f-4e35-93c4-fcb5603afaea.png)

## Student Examination Timetables: Produce a table showing the examination timetable for a given student. ##

**Produce timetable for student number: 1**

```sql
CREATE FUNCTION retrieve_student_timetable (@sno INTEGER)
RETURNS TABLE
AS
RETURN
	 SELECT sname, excode, extitle, exlocation, exdate, extime
	 FROM student, exam
	 WHERE student.sno =  @sno

SELECT * FROM retrieve_student_timetable (1)
```
![image](https://user-images.githubusercontent.com/77920592/205102287-41240a92-f700-4c0e-b0c3-a11303967c5c.png)

## All examination results: Produce a table showing the result obtained by each student for each examination. ##

```sql
SELECT sno, eno, excode, egrade
FROM entry
GROUP BY sno, eno, excode, egrade
ORDER BY sno
```

## Select examination results: As Q above but for a given examination. ##

**Select results for exam code: ‘VB01’.**

```sql
SELECT sno, eno, excode, egrade
FROM entry
WHERE excode = 'VB01'
GROUP BY sno, eno, excode, egrade
ORDER BY sno
```
![image](https://user-images.githubusercontent.com/77920592/205102379-c925a10f-621c-4796-a09e-1b41fd564cba.png)

## Results for selected student: Produce a table showing details of all examinations taken by a student. ##

**Select results for student number: ‘1’**

```sql
CREATE FUNCTION retrieve_student_examinations(@sno INTEGER)
RETURNS TABLE
AS
RETURN
	 SELECT sname, exam.excode, extitle, exlocation, exdate, extime, egrade
	 FROM student, exam, entry
	 WHERE student.sno = entry.sno 
	 AND exam.excode = entry.excode 
	 AND student.sno = @sno

SELECT * FROM retrieve_student_examinations(1)
```
![image](https://user-images.githubusercontent.com/77920592/205102437-44de0eec-9056-40ec-beb4-e792857f73a9.png)

## Membership status for selected student: Given a specific student membership number, display the name of the student and their membership status in the society. ##

**Display membership status for student number: ‘1’**

```sql
CREATE TRIGGER update_exam_details
ON entry FOR UPDATE
AS
BEGIN
      INSERT INTO exam_details (excode, sno, egrade, extitle, exlocation, exdate, extime) 
      SELECT DISTINCT entry.excode, entry.sno, entry.egrade,
					  exam.extitle, exam.exlocation, exam.exdate, exam.extime
      FROM INSERTED entry join exam on entry.excode = exam.excode 
      WHERE sno = entry.sno
END
GO
```
```sql
CREATE FUNCTION membership (@sno INTEGER)
RETURNS TABLE
AS 
RETURN
	 SELECT s.sname, 
	 CASE WHEN s.sname IS NOT NULL THEN 'Accredited'
	 ELSE 'Pending' END as membership
	 
	 FROM exam_details ed JOIN student s ON ed.sno = s.sno
	 WHERE @sno = s.sno AND egrade IS NOT NULL 
	 AND exdate BETWEEN '2022/01/01' AND '2022/12/31'
	 AND ed.sno = @sno
	 GROUP BY s.sname
	 HAVING COUNT(ed.sno) > 3 AND AVG(egrade) >= 50
```
```sql
SELECT * FROM MEMBERSHIP(1)
```
![image](https://user-images.githubusercontent.com/77920592/205102512-e507a4b7-4508-4f45-8f7e-f61d82fdada2.png)

## Delete selected student: This happens if a student withdraws from the society.  All the examination entries for the student must be cancelled. ##

**Delete student number: ‘200’**

```sql
CREATE TRIGGER delete_entry_update_cancel
ON entry FOR DELETE
AS
BEGIN
	  DECLARE @eno INT, @excode VARCHAR(4), @sno INT, @cdate DATETIME
	  SELECT @eno = D.eno, @excode = D.excode, @sno = D.sno, @cdate = getdate()
	  FROM DELETED D
	  INSERT INTO cancel(eno, excode, sno, cdate)
	  VALUES (@eno, @excode, @sno, @cdate)

END
GO
```
```sql
DELETE FROM student WHERE sno = 2;

SELECT * FROM cancel
```
![image](https://user-images.githubusercontent.com/77920592/205102589-c3bef79c-4cf7-4c2e-b2e2-9d5c47b4f48a.png)

## Delete selected examination: ##

**Delete exam code : ‘VB01’**

```sql
DELETE FROM exam WHERE excode = 'VB01'
```
Msg 547, Level 16, State 0, Line 1
The DELETE statement conflicted with the REFERENCE constraint "FK__entry__excode__32E0915F". The conflict occurred in database "School", table "dbo.entry", column 'excode'.

**Delete exam code : ‘SQL1’**
![image](https://user-images.githubusercontent.com/77920592/205102707-99329f07-9b82-4752-a8c4-aad076f835ce.png)










