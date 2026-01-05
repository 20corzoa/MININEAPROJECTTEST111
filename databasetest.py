
import mysql.connector

#to connect database


#creating class for the database allows for neater code because all the code related to opening and closing the database is in one place.
#works better than functions beacause for functions i would have to open and close the database connection each time.

class dataBase:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Junior2014@",
            database="mydb"
        )

        self.cursor = self.db.cursor()
        print(self.cursor)
#        if self.db.is_connected():
#            self.cursor = self.db.cursor()
#            print("connected to database")

    def close(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
            print("database connection closed")


#student create read update delete

    def create_student(self, fName, lNName, gender, dob, year, form, house, sEmail, sPhone, consent, contactID, medicalID):
        try:
            self.cursor = self.db.cursor()
            print(self.cursor)
            query = "INSERT INTO students (fName, lName, gender, dob, year, form, house, sEmail, sPhone, consent, contactID, medicalID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (fName,lNName,gender,dob.year,dob.month,dob.day, year, form, house, sEmail, sPhone, consent, contactID, medicalID)
            self.cursor.execute(query, values)
            self.db.commit()
            print("db: student created")
        except Exception as e:
            print("error creating student :", e)
            self.db.rollback()  

    def read_all_students(self): #read all students from database
        try:
            self.cursor = self.db.cursor()
            print(self.cursor)
            query = "SELECT * FROM students"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print("error reading all students :", e)
            return []


    def read_student_by_id(self, studentID):
        try:
            query = "SELECT * FROM student WHERE studentID = %s"
            values = (studentID)
            self.cursor().execute(query, values)
            result = self.cursor().fetchone() #fetches one result
            return result
        except:
            print("error")
            return None
        

    def update_student(self, studentID, fName, lNName, gender, dob, year, form, house, sEmail, sPhone, consent, contactID, medicalID): #kwargs means any number of parameters 
        fields = []
        values = []
        try:
            self.cursor = self.db.cursor()
            print(self.cursor)
            fields.append("studentID = %s")
            values.append(studentID)
            fields.append("fName = %s")
            values.append(fName)
            fields.append("lName = %s")
            values.append(lNName)
            fields.append("gender = %s")
            values.append(gender)
            fields.append("dob = %s")
            values.append(dob)
            fields.append("year = %s")
            values.append(year)
            fields.append("form = %s")
            values.append(form)
            fields.append("house = %s")
            values.append(house)
            fields.append("email = %s")
            values.append(sEmail)
            fields.append("phone = %s")
            values.append(sPhone)
            fields.append("consent = %s")
            values.append(consent)
            fields.append("contactID = %s")
            values.append(contactID)
            fields.append("medicalID = %s")
            values.append(medicalID)
            #values.append(userid)
            query = f"UPDATE students SET fName = %s, lName = %s, gender = %s, dob = %s, year = %s, form = %s, house = %s, email = %s, phone = %s, consent = %s, contactID = %s, medicalID = %s WHERE studentID = %s"
            values =(fName, lNName, gender, dob.year,dob.month,dob.day, year, form, house, sEmail, sPhone, consent, contactID, medicalID, studentID)
            self.cursor.execute(query, tuple(values))
            self.db.commit()
            print("student updated")
        except Exception as e:
            print("error updating student :", e)
            self.db.rollback()
            print("error")
    
    def delete_student(self, studentID):
        try:
            self.cursor = self.db.cursor()
            print(self.cursor)
            query = "DELETE FROM students WHERE studentID = %s"
            values = list(str(studentID))
            self.cursor.execute(query, values)
            self.db.commit()
            print("Student deleted")
        except Exception as e:
            print("error deleting student :", e)
            self.db.rollback()
            print("error")

    
    #trip create read update delete

    def create_trip(self, destination, date, returnDate, status, leaderID):
        try:
            query = "INSERT INTO trip(destination, date, returnDate, status, leaderID) VALUES(%s, %s, %s, %s, %s)"
            values = (destination, date, returnDate, status, leaderID)
            self.cursor().execute(query, values)
            self.db.commit()
            print("trip created")
        except:
            self.db.rollback()
            print("error")

    def read_all_trips(self):
        try:
            query = "SELECT * FROM trip"
            self.cursor().execute(query)
            results = self.cursor().fetchall()
            return results
        except:
            print("error")
            return []
    
    def read_trip_by_id(self, tripID):
        try:
            query = "SELECT * FROM trip WHERE tripID = %s"
            values = (tripID)
            self.cursor().execute(query, values)
            result = self.cursor().fetchone()
            return result
        except:
            print("error")
            return None
    
    def read_trips_by_leader(self, leaderID):
        try:
            query = "SELECT * FROM trip WHERE leaderID = %s"
            values = (leaderID)
            self.cursor().execute(query, values)
            results = self.cursor().fetchall()
            return results
        except:
            print("error")
            return []
        
    def read_trips_by_destination(self, destination):
        try:
            query = "SELECT * FROM trip WHERE destination = %s"
            values = (destination)
            self.cursor().execute(query, values)
            results = self.cursor().fetchall()
            return results
        except:
            print("error")
            return []
        
    def update_trip(self, tripID, **kwargs):
        fields = []
        values = []
        try:
            for key, value in kwargs.items():
                fields.append(f"{key} = %s")
                values.append(value)
            values.append(tripID)
            query = f"UPDATE trip SET {', '.join(fields)} WHERE tripID = %s"
            self.cursor().execute(query, tuple(values))
            self.db.commit()
            print("trip updated")
        except:
            self.db.rollback()
            print("error")

    def delete_trip(self, tripID):
        try:
            query = "DELETE FROM trip WHERE tripID = %s"
            values = (tripID)
            self.cursor().execute(query, values)
            self.db.commit()
            print("trip deleted")
        except:
            self.db.rollback()
            print("error")
    


    #trip asssign and removing functions


    def assign_student_to_trip(self, tripID, studentID):
        try:
            query = "INSERT INTO trip_students (tripID, studentID) VALUES (%s, %s)"
            values = (tripID, studentID)
            self.cursor().execute(query, values)
            self.db.commit()
            print("student assigned to trip")
        except:
            self.db.rollback()
            print("error")

    def remove_student_from_trip(self, tripID, studentID):
        try:
            query = "DELETE FROM trip_students WHERE tripID = %s AND studentID = %s"
            values = (tripID, studentID)
            self.cursor().execute(query, values)
            self.db.commit()
            print("student removed from trip")
        except:
            self.db.rollback()
            print("error")
    
    def get_trip_students(self, tripID): #get all students assigned to a trip
        try:
            query = "SELECT studentID FROM trip_students WHERE tripID = %s"
            values = (tripID)
            self.cursor().execute(query, values)
            results = self.cursor().fetchall()
            return results
        except:
            print("error")
            return []
    
    def get_student_trips(self, studentID): #get all trips a student is assigned to
        try:
            query = "SELECT tripID FROM trip_students WHERE studentID = %s"
            values = (studentID)
            self.cursor().execute(query, values)
            results = self.cursor().fetchall()
            return results
        except:
            print("error")
            return []


    #USER create read update delete

    def create_user(self, userid, username, password, fname, lname, email, phone, role_id):
        try:
            self.cursor = self.db.cursor()
            print(self.cursor)
            query = "INSERT INTO users (userid, username, password, fName, lName, email, phone, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (str(userid), username, password, fname, lname, email, phone, role_id)
            self.cursor.execute(query, values)
            self.db.commit()
            print("db: user created")
        except Exception as e:
            print("error creating user :", e)
            self.db.rollback()

    def read_user_by_username(self, username):
        try:
            query = "SELECT * FROM user WHERE username = %s"
            values = (username)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            return result
        except:
            print("error")
            return None
        
    def read_all_users(self):
        try:
            self.cursor = self.db.cursor()
            print(self.cursor)
            query = "SELECT * FROM users"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print("error reading all users :", e)
            return []

    def generate_next_id(self):
        try:
            self.cursor = self.db.cursor()
            print(self.cursor)
            query = "SELECT * FROM variables"
            self.cursor.execute(query)
            results = self.cursor.fetchall()[0]
            nextID = results[0] + 1
            updateQuery = "UPDATE variables SET NextID ="+ str(nextID)
            print ("nextID generated:", nextID)
            print("updated querey:", updateQuery)
            self.cursor.execute(updateQuery)
            self.db.commit()
            return nextID
        except Exception as e:
            print("error creating new user ID :", e)
            return -1



    def read_user_by_id(self, userID):
        try:
            query = "SELECT * FROM user WHERE userID = %s"
            values = (userID)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            return result
        except:
            print("error")
            return None

    def update_user(self, userid, username, password, fname, lname, email, phone, role_id):
        fields = []
        values = []
        try:
            self.cursor = self.db.cursor()
            print(self.cursor)
            fields.append("userid = %s")
            values.append(userid)
            fields.append("username = %s")
            values.append(username)
            fields.append("password = %s")
            values.append(password)
            fields.append("fName = %s")
            values.append(fname)
            fields.append("lName = %s")
            values.append(lname)
            fields.append("email = %s")
            values.append(email)
            fields.append("phone = %s")
            values.append(phone)
            fields.append("role = %s")
            values.append(role_id)
            #values.append(userid)
            query = f"UPDATE users SET username = %s, password = %s, fName = %s, lName = %s, email = %s, phone = %s, role = %s WHERE userID = %s"
            values =(username, password, fname, lname, email, phone, role_id, str(userid))
            self.cursor.execute(query, tuple(values))
            self.db.commit()
            print("user updated")
        except Exception as e:
            print("error updating user :", e)
            self.db.rollback()
            print("error")

    def delete_user(self, userID):
        try:
            self.cursor = self.db.cursor()
            print(self.cursor)
            query = "DELETE FROM users WHERE userID = %s"
            values = list(str(userID))
            self.cursor.execute(query, values)
            self.db.commit()
            print("user deleted")
        except Exception as e:
            print("error deleting user :", e)
            self.db.rollback()
            print("error")

    def verify_user(self, username, password):
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            values = (username, password)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result: #if a matching user is found
                return True
            else: #no matching user
                return False
        except:
            print("error")
            return False



    #emergency contact create read update delete

    def create_medical_info(self, dietary_needs, medical, notes, doctors):
        try:
            query = "INSERT INTO medical_information (dietaryneeds, medical, notes, doctors) VALUES (%s, %s, %s, %s)"
            values = (dietary_needs, medical, notes, doctors)
            self.cursor.execute(query, values)
            self.db.commit()
            print("medical information created")
        except:
            print("error")
            self.db.rollback()

    def read_medical_info_by_id(self, medicalID):
        try:
            query = "SELECT * FROM medical_information WHERE medicalID = %s"
            values = (medicalID)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            return result
        except:
            print("error")
            return None
    
    def read_all_medical_info(self):
        try:
            query = "SELECT * FROM medical_information"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except:
            print("error")
            return []

    def read_medical_info_by_trip(self, tripID):
        try:
            query = """SELECT medical_information.* FROM medical_information
                       JOIN student ON medical_information.medicalID = student.medicalID
                       JOIN trip_students ON student.studentID = trip_students.studentID
                       WHERE trip_students.tripID = %s"""
            values = (tripID)
            self.cursor.execute(query, values)
            results = self.cursor.fetchall()
            return results
        except:
            print("error")
            return []
        
    def update_medical_info(self, medicalID, **kwargs):
        fields = []
        values = []
        try:
            for key, value in kwargs.items():
                fields.append(f"{key} = %s")
                values.append(value)
            values.append(medicalID)
            query = f"UPDATE medical_information SET {', '.join(fields)} WHERE medicalID = %s"
            self.cursor.execute(query, tuple(values))
            self.db.commit()
            print("medical information updated")
        except:
            self.db.rollback()
            print("error")

    def delete_medical_info(self, medicalID):
        try:
            query = "DELETE FROM medical_information WHERE medicalID = %s"
            values = (medicalID)
            self.cursor.execute(query, values)
            self.db.commit()
            print("medical information deleted")
        except:
            self.db.rollback()
            print("error")
