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
    
inputfile = open("testpart2.txt", "r")
filedata = [x.strip('\n') for x in inputfile]
inputfile.close()

cur.execute("SET SEARCH_PATH to demo;")


for index in range(0,len(filedata)):
    
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

        if filedata[index] == 'Q':
            
            sql = "SELECT sno, eno, excode, egrade from entry WHERE entry IS NOT NULL GROUP BY sno, eno, excode, egrade ORDER BY sno"
            
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute(sql)
                rows = cur.fetchall()
                print ("\n<< Table: Result for Exams >>\n")
                for row in rows:
                    print(str(row).strip())
                cur.execute("COMMIT;")
                
                
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}") 
            

        if filedata[index] == 'R':
            
            excode = filedata[index+1]
            sql = "SELECT sno, eno, excode, egrade from entry WHERE entry IS NOT NULL AND excode  = '{}' GROUP BY sno, eno, excode, egrade ORDER BY sno".format(excode)
            
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute(sql)
                rows = cur.fetchall()
                print ("\n<< Table: Result for Exams >>\n")
                for row in rows:
                    print(str(row).strip())
                cur.execute("COMMIT;")
                
                
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}") 
            
            
        if filedata[index] == 'S':
            
            sno = filedata[index+1]
            sql = "SELECT * FROM retrieve_student_examinations('{}')".format(sno)
            
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute(sql)
                rows = cur.fetchall()
                print ("\n<< Table: Exams Details >>\n")
                for row in rows:
                    print(str(row).strip())
                cur.execute("COMMIT;")
                
                
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}")              
            

        if filedata[index] == 'T':
            
            sno = filedata[index+1]
            sql = "SELECT sname, membership(sno) FROM student WHERE sno = '{}'".format(sno)
            
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute(sql)
                rows = cur.fetchall()
                print ("\n<< Table: Membership Status >>\n")
                for row in rows:
                    print(str(row).strip())
                cur.execute("COMMIT;")
                
                
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}")   
                
                
        if filedata[index] == 'V':
            
            sno = filedata[index+1]
            sql = "SELECT * FROM cancel WHERE sno = ('{}')".format(sno)            
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute(sql)
                rows = cur.fetchall()
                print ("\n<< Table: Cancelled Entries >>\n")
                for row in rows:
                    print(str(row).strip())
                cur.execute("COMMIT;")
                
                
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}")  
                

        if filedata[index] == 'C':
            
            sno = filedata[index+1]
            sql = "DELETE FROM student WHERE sno = ('{}')".format(sno)          
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute("SELECT * FROM student;")
                rows = cur.fetchall()
                print ("\n<< Table: Remaining Student >>\n")
                for row in rows:
                    print(str(row).strip())
                cur.execute("COMMIT;")
                
                
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}")  


        if filedata[index] == 'V':
            
            sno = filedata[index+1]
            sql = "SELECT * FROM cancel WHERE sno = ('{}')".format(sno)            
            try:
                cur.execute("BEGIN;")
                cur.execute(sql)
                cur.execute("COMMIT;")
                
                cur.execute(sql)
                rows = cur.fetchall()
                print ("\n<< Table: Cancelled Entries >>\n")
                for row in rows:
                    print(str(row).strip())
                cur.execute("COMMIT;")
                
                
            except Exception as err:
                cur.execute("ROLLBACK")
                print (f"Execute SQL Error {err}")  

