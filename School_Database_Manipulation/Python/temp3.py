import psycopg2
import os

def getConn():
    #function to retrieve the password, construct
    #the connection string, make a connection and return it.
    pwFile = open("pw.txt", "r")
    pw = pwFile.read();
    pwFile.close()
    connStr = "host='cmpstudb-01.cmp.uea.ac.uk' \
               dbname= 'wgq21ryu' user='wgq21ryu' password = " + pw
    #connStr=("dbname='studentdb' user='dbuser' password= 'dbPassword' " )
    conn=psycopg2.connect(connStr)      
    return  conn

def clearOutput():
    outputfile = open("output.txt", "w")
    outputfile.write('')
        
def writeOutput(output):
    outputfile = open("output.txt", "a")
    outputfile.write('')

conn=None   
conn=getConn()
cur = conn.cursor()
    
inputfile = open("testpart3.txt", "r")
filedata = [x.strip('\n') for x in inputfile]
inputfile.close()

cur.execute("SET SEARCH_PATH to demo;")

print (filedata)
for index in range(0,len(filedata)):
    
    
        if filedata[index] == 'D':
            
            excode = filedata[index+1]
            sql = "DELETE FROM exam WHERE excode = '{}'".format(excode)
            
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute("SELECT * FROM exam;")
                rows = cur.fetchall()
                print ("\n<< Table: Exam >>\n")
                for row in rows:
                    print(str(row).strip())
                    
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error  {err}")
    
        if filedata[index] == 'A':
            
            sno = filedata[index+1]
            sname = filedata[index+2]
            semail = filedata[index+3]
            sql = "INSERT INTO student VALUES  ('{}', '{}', '{}')".format(sno,sname,semail)
            
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute("SELECT * FROM student;")
                rows = cur.fetchall()
                print ("\n<< Table: Student >>\n")
                for row in rows:
                    print(str(row).strip())
                    
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}")

        if filedata[index] == 'B':
            
            excode = filedata[index+1]
            extitle = filedata[index+2]
            exlocation = filedata[index+3]
            exdate = filedata[index+4]
            extime = filedata[index+5]
            sql = "INSERT INTO exam VALUES  ('{}', '{}', '{}', '{}', '{}')".format(excode,extitle,exlocation,exdate,extime)
            
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                sd
                cur.execute("SELECT * FROM exam;")
                rows = cur.fetchall()
                print ("\n<< Table: Exam >>\n")
                for row in rows:
                    print(str(row).strip())
                    
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}")
                       
   
        if filedata[index] == 'E':
            excode = filedata[index+1]
            sno = filedata[index+2]
            sql = "INSERT INTO entry (excode, sno) VALUES  ('{}', '{}')".format(excode,sno)
          
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute("SELECT * FROM entry;")
                rows = cur.fetchall()
                print ("\n<< Table: Entry >>\n")
                for row in rows:
                    print(str(row).strip())
                    
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}")

                
                
        if filedata[index] == 'F':
            eno = filedata[index+1]
            egrade = filedata[index+2]
            sql = "UPDATE entry SET egrade = '{}' where eno = {};".format(egrade,eno)
          
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute("SELECT * FROM entry;")
                rows = cur.fetchall()
                print ("\n<< Table: Entry >>\n")
                for row in rows:
                    print(str(row).strip())
                    
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}")


        if filedata[index] == 'P':
            
            sno = filedata[index+1]
            sql = "SELECT * FROM retrieve_student_timetable({})".format(sno)
            
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute(sql)
                rows = cur.fetchall()
                print ("\n<< Table: Timetable >>\n")
                for row in rows:
                    print(str(row).strip())
                cur.execute("COMMIT;")
                
                
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}")   
                
                
                
