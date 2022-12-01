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

## Insert entry: Insert an examination entry ##

**Insert an entry with values:  Exam code : ‘VB03’ Exam title : Student number : ‘1’**

```sql
INSERT INTO entry (excode, sno)
VALUES ('VB03', '1')

SELECT * FROM entry
```

## Update an entry: record the grade awarded to an entry. ##

**Update an entry with Entry number: ‘10’,  for ‘VB03’ and student number ‘100, (i.e.  the last entry you entered) with a grade ‘60’.**

```sql
UPDATE entry
SET egrade = 60 WHERE eno = 28 AND excode = 'VB03'

SELECT * FROM entry
```

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

**Produce timetable for student number: 2**
```sql
SELECT * FROM retrieve_student_timetable (2)
```

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

**Display membership status for student number: ‘2’**

![image](https://user-images.githubusercontent.com/77920592/202194707-c74e1185-d9a9-431d-b2b6-3151da26fbfb.png)

## Delete selected student: This happens if a student withdraws from the society.  All the examination entries for the student must be cancelled. ##

Delete student number: ‘200’

![image](https://user-images.githubusercontent.com/77920592/202194763-5f7b6bfe-a20a-478b-aa16-545b1305dd2d.png)

Show the cancel table.

![image](https://user-images.githubusercontent.com/77920592/202194820-06e3ad9d-2a80-49a4-a243-ae35ef32bb3a.png)

Delete selected examination: 

Delete exam code : ‘VB01’

![image](https://user-images.githubusercontent.com/77920592/202194858-220794fd-20d6-488e-9616-3d8d8ebbffc2.png)

Delete exam code : ‘SQL1’

![image](https://user-images.githubusercontent.com/77920592/202194883-1d6a8ab7-3cdd-49e7-8bc7-fd642a12c5c2.png)










