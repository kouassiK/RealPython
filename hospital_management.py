import sqlite3
import datetime
from dateutil.relativedelta import relativedelta

conn = sqlite3.connect('Hospital.db')

c = conn.cursor()

def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS Hospital(Hospital_Id INTEGER, Hospital_Name TEXT, BedCount INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS Doctor(Doctor_Id INTEGER, Doctor_Name TEXT, Hospital_Id INTEGER, Joining_Date TEXT, Speciality TEXT, Salary INTEGER, Experience TEXT)')
    conn.close()

def data_entry():

    c.execute("INSERT INTO Hospital VALUES (1, 'Mayo Clinic', 200)")
    c.execute("INSERT INTO Hospital VALUES (2, 'Cleveland Clinic', 400)")
    c.execute("INSERT INTO Hospital VALUES (3, 'Johns Hopkins', 1000)")
    c.execute("INSERT INTO Hospital VALUES (4, 'UCLA Medical Center', 1500)")


    c.execute("INSERT INTO Doctor VALUES(101, 'David', 1, '2005-02-10', 'Pediatric', 40000, 'NULL')")
    c.execute("INSERT INTO Doctor VALUES(102, 'Michael', 1, '2018-07-23', 'Oncologist', 20000, 'NULL')")
    c.execute("INSERT INTO Doctor VALUES(103, 'Susan' ,2, '2016-05-19', 'Garnacologist', 25000, 'NULL')")
    c.execute("INSERT INTO Doctor VALUES(104, 'Robert', 2,  '2017-12-28', 'Pediatric', 28000, 'NULL')")
    c.execute("INSERT INTO Doctor VALUES(105, 'Linda', 3,  '2004-06-04', 'Garnacologist', 42000, 'NULL')")
    c.execute("INSERT INTO Doctor VALUES(106, 'William' ,3, '2012-09-11', 'Dermatologist', 30000, 'NULL')")
    c.execute("INSERT INTO Doctor VALUES(107, 'Richard', 4,  '2014-08-21', 'Garnacologist', 32000, 'NULL')")
    c.execute("INSERT INTO Doctor VALUES(108, 'Karen', 4,  '2011-10-17', 'Radiologist', 30000, 'NULL')")

    conn.commit()
    c.close()
    conn.close()

#create_tables()
#data_entry()

def get_connection():
    connection = sqlite3.connect('Hospital.db')
    return connection

def close_connection(connection):
    if connection:
        connection.close()


def read_database_version():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("select sqlite_version();")
        db_version = cursor.fetchone()
        print("You are connected to SQLite version: ", db_version)
        close_connection(connection)
    except (Exception, sqlite3.Error) as error:
        print("Error while getting data", error)

#print("Question 1: Print Database version")
#read_database_version()

    
def get_doctor_detail(doctor_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """ SELECT * From Doctor WHERE Doctor_Id = ? """
        cursor.execute(query, (doctor_id,))
        records = cursor.fetchall()
        for row in records:
            print("Doctor_Id", row[0])
            print("Doctor_Name", row[1])
            print("Hospital_Id", row[2])
            print("Joining_Date", row[3])
            print("Speciality", row[4])
            print("Salary", row[5])
            print("Experience", row[6])

        close_connection(connection)
    except (Exception, sqlite3.Error) as error:
        print("Error while getting data", error)

def get_hospital_detail(hospital_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        select_query = """select * from Hospital where Hospital_Id = ?"""
        cursor.execute(select_query, (hospital_id,))
        records = cursor.fetchall()
        print("Printing Hospital record")
        for row in records:
            print("Hospital Id:", row[0], )
            print("Hospital Name:", row[1])
            print("Bed Count:", row[2])
        close_connection(connection)
    except (Exception, sqlite3.Error) as error:
        print("Error while getting data", error)

#get_hospital_detail(2)
#get_doctor_detail(105)


def get_hospital_name(hospital_id):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "SELECT *  FROM Hospital WHERE Hospital_Id = ?"
        cursor.execute(query, (hospital_id,))
        records = cursor.fetchone()
        return records[1]
        
    except (Exception, sqlite3.Error) as error:
        print("Error while getting data", error) 

#print(get_hospital_name(2))

def get_doctors(hospital_id):
    #Fetch All doctors within given Hospital
    print('Printing Doctors of ' + get_hospital_name(hospital_id))
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """ SELECT * FROM Doctor WHERE Hospital_Id = ?"""
        cursor.execute(query, (hospital_id,))
        records = cursor.fetchall()
        for row in records:
            print("Doctor Id: ",row[0])
            print("Doctor Name: ", row[1])
            print("Hospital Id: ", row[2])
            print("Hospital Name: ", get_hospital_name(hospital_id))
            print("Joining Date: ", row[3])
            print("Speciality: ", row[4])
            print("Salary:", row[5])
            print("Experience:", row[6], "\n")

        close_connection(connection)
    except (Exception, sqlite3.Error) as error:
        print("Error while getting data", error)
        
#get_doctors(2)

def update_doctor_experience(doctor_id):
    # Update Doctor Experience in Years
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """ SELECT Joining_Date FROM Doctor WHERE Doctor_Id = ?"""
        cursor.execute(query, (doctor_id,))
        joining_date = cursor.fetchone()

        # calculate Experience in years
        joining_date_1 = datetime.datetime.strptime(''.join(map(str, joining_date)), '%Y-%m-%d')
        today_date = datetime.datetime.now()
        experience = relativedelta(today_date, joining_date_1).years


        # Update doctor's Experience now
        connection = get_connection()
        cursor = connection.cursor()
        sql_select_query = """update Doctor set Experience = ? where Doctor_Id = ?"""
        cursor.execute(sql_select_query, (experience, doctor_id))
        connection.commit()
        print("Doctor Id:", doctor_id, " Experience updated to ", experience, " years")
        close_connection(connection)

    except (Exception, sqlite3.Error) as error:
        print("Error while getting doctor's data", error)

update_doctor_experience(101)
