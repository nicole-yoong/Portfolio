# Triggers #

**Retrieve student timetable**
```sql
CREATE FUNCTION retrieve_student_timetable (@sno INTEGER)
RETURNS TABLE
AS
RETURN
	 SELECT sname, excode, extitle, exlocation, exdate, extime
	 FROM student, exam
	 WHERE student.sno =  @sno
```

**Delete entry and update the cancel table**
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

**Retrieve grade_title, distinction, merit or pass  for all examinations**
```sql
CREATE TRIGGER update_grade_title
ON entry FOR UPDATE
AS
   BEGIN
      INSERT INTO result (sno, excode, egrade, grade_title)
	    SELECT DISTINCT entry.sno, entry.excode, entry.egrade,
	    CASE WHEN egrade > 70 THEN 'Distinction'
		    WHEN (egrade < 70 and egrade > 50) THEN 'PASS' 
		    WHEN egrade < 50 THEN 'FAIL'
	   END AS grade_title
	   FROM INSERTED entry
	   WHERE sno = entry.sno;

END
GO
```

**Retrieve grade_title, distinction, merit or pass based on excode**
```sql
CREATE FUNCTION retrieve_result_on_excode (
	@sno INTEGER, @egrade DECIMAL
)
RETURNS VARCHAR(20) AS 
BEGIN
	DECLARE @grade_title VARCHAR(20);
	SET @grade_title = NULL
	IF @egrade > 70 SET @grade_title = 'Distinction';
	IF (@egrade < 70 and @egrade > 50) SET @grade_title = 'Merit';
	IF @egrade < 50 SET @grade_title = 'FAIL';

	RETURN @grade_title
END
GO
```

**Update exam details**
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

CREATE TRIGGER update_exam_details_sname
ON exam_details FOR INSERT
AS
BEGIN
	 INSERT INTO exam_details (sname)
	 SELECT DISTINCT student.sname
	 FROM INSERTED student
	 WHERE sname = student.sname
END
GO
```

**Retrieve cancel data based on sno**
```sql
CREATE FUNCTION retrieve_student_cancel (@sno INTEGER)
RETURNS TABLE
AS
RETURN
	SELECT eno, excode, cdate, cuser FROM cancel 
	WHERE sno = @sno
```
