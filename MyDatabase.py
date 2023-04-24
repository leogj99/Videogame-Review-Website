import mysql.connector
import re
import random 
from tabulate import tabulate

class MyDatabase:
    def __init__(self, hostname, user_name, mysql_pw, database_name) -> None:
        self.hostname = hostname
        self.username = user_name
        self.mysql_pw = mysql_pw
        self.database_name = database_name
    
    def open_database(self):
        self.connection = mysql.connector.connect(host =self.hostname, user= self.username, password= self.mysql_pw, database= self.database_name)
        self.cursor = self.connection.cursor()


    def printFormat(self, result):
        header = []
        for cd in self.cursor.description:  # get headers
            header.append(cd[0])
        print(tabulate(result, headers=header, tablefmt='fancy_grid', showindex=False, numalign='center', stralign='left'))


    # select and display query
    def executeSelect(self,query):
        self.cursor.execute(query)
        self.printFormat(self.cursor.fetchall())


    def insert(self,table, values):
        query = "INSERT into " + table + " values (" + values + ")" + ';'
        self.cursor.execute(query)
        self.connection.commit()


    def executeUpdate(self, query):  # use this function for delete and update
        self.cursor.execute(query)
        self.connection.commit()
        
    def findProfessor(self):
        self.executeSelect("SELECT DEPT_CODE, DEPT_NAME FROM DEPT")            # Shows all the departments in the dept table
        dept_code = input("Select a DEPARTMENT CODE: ")                        # Asks user to type a dept code
        print("\n")
        
        # Checks if the department exist
        if self.findMatch("DEPT_CODE", "DEPT", dept_code) == False:
            print(f"**ERROR: DEPARTMENT {dept_code.upper()} DOES NOT EXIST**\n")
            return
        
        # Shows professors in the department
        self.executeSelect(f"SELECT * FROM PROFESSOR WHERE DEPT_CODE = '{dept_code.upper()}'")
        print(f"**SHOWING PROFESSORS IN {dept_code.upper()} DEPEPARTMENT**\n")
        
            
    def findSection(self):
        valid_num = False                # Keeps track of the main while loop. 
        all_classes = False              # Keeps track if user want to show all classes or just the open ones
        search_by = 0
        
        while valid_num == False:        # Keeps looping until users chooses 1 or 2
            print("Do you want to see all classes or just open classes?")
            print("1) ALL   2) Open only\n")
            choice = input("Choose a number: ")
            print("\n")
            if int(choice) == 1 or int(choice) == 2:        
                valid_num = True
                if int(choice) == 1:          # If uses picks 1 he wanted to see all classes 
                    all_classes = True
                    
                while int(search_by) < 1 or int(search_by) > 2:       # Keeps looping until 1 or 2 are choosen
                    print("Do you want to search by department or level?")
                    print("1) Department    2) Level\n")
                    search_by = input("Choose by number: ")
                    if int(search_by) == 1 or int(search_by) == 2:
                        #----------------------SEARCH BY DEPARTMENT CODE----------------------
                        if int(search_by) == 1:                     # If we search we department and want to see all classes
                            self.executeSelect(f"SELECT DEPT_CODE, DEPT_NAME FROM DEPT")     # Shows all the departments available
                            dept_code = input("Enter department code: ")
                            print("\n")
                            self.cursor.execute(f"SELECT DEPT_CODE FROM DEPT WHERE DEPT_CODE = '{dept_code.upper()}'") # Selects all departments code matching
                            result = self.cursor.fetchall()      # Fetches the result is there is one
                            
                            if result is not None:
                                if all_classes == True:       # Displays all the classes by department
                                    self.executeSelect(f"SELECT DEPT_CODE, COURSE_NUM, SID, BUILDING, ROOM_NUM, DAYS, START_TIME, END_TIME, "
                                                        f"CASE WHEN MAX_ENROLLMENT - CURRENT_ENROLLMENT < 0 THEN 0 ELSE MAX_ENROLLMENT - CURRENT_ENROLLMENT END AS AVAILABLE_SEATS "
                                                        f"FROM SECTION WHERE DEPT_CODE = '{dept_code.upper()}'")

                                    print(f"**SHOWING ALL CLASSES IN {dept_code.upper()} DEPEPARTMENT**\n")
                                else:                         # Displays only open classes
                                    self.executeSelect(f"SELECT DEPT_CODE, COURSE_NUM, SID, BUILDING, ROOM_NUM, DAYS, START_TIME, END_TIME, "
                                                        f"MAX_ENROLLMENT - CURRENT_ENROLLMENT AS AVAILABLE_SEATS "
                                                        f"FROM SECTION WHERE DEPT_CODE = '{dept_code.upper()}' AND MAX_ENROLLMENT - CURRENT_ENROLLMENT > 0")
                                    print(f"**SHOWING OPEN CLASSES OF {dept_code.upper()} DEPEPARTMENT**\n")
                                    
                            else:
                                print(f"**ERROR: DEPARTMENT CODE {dept_code.upper()} DOES NOT EXISTS**\n")
                            #----------------------SEARCH BY LEVEL NUMBER-------------------------
                        if int(search_by) == 2:
                            level = 0
                            while int(level) < 1000 or int(level) > 6000:  # loops until number between 1000 and 6000 is inputed
                                print("Enter one of the following levels: 1000, 2000, 3000, 4000 or 5000")
                                level = input("Choice: ")
                                # Selects all the courses with course number in the level chosen
                                self.cursor.execute(f"SELECT COURSE_NUM FROM COURSE WHERE COURSE_NUM >= '{int(level)}' AND COURSE_NUM <= '{int(level) + 1000}'")
                                result = self.cursor.fetchall()   # Fetches the result is there is one
                                if result is not None:
                                    if all_classes == True:
                                        self.executeSelect(f"SELECT DEPT_CODE, COURSE_NUM, BUILDING, ROOM_NUM, "
                                                            f"DAYS, START_TIME, END_TIME, CASE WHEN MAX_ENROLLMENT - CURRENT_ENROLLMENT "
                                                            f"< 0 THEN 0 ELSE MAX_ENROLLMENT - CURRENT_ENROLLMENT END AS AVAILABLE_SEATS "
                                                            f"FROM SECTION WHERE COURSE_NUM >= {int(level)} AND COURSE_NUM < {int(level) + 1000}")
                                        print(f"**SHOWING ALL THE CLASSES IN LEVEL {level}**\n")
                                    else:
                                        self.executeSelect(f"SELECT DEPT_CODE, COURSE_NUM, BUILDING, ROOM_NUM, "
                                                            f"DAYS, START_TIME, END_TIME, "
                                                            f"CASE WHEN MAX_ENROLLMENT - CURRENT_ENROLLMENT <= 0 "
                                                            f"THEN 0 ELSE MAX_ENROLLMENT - CURRENT_ENROLLMENT END AS AVAILABLE_SEATS "
                                                            f"FROM (SELECT * FROM SECTION WHERE COURSE_NUM >= {int(level)} AND COURSE_NUM < {int(level) + 1000}) AS S "
                                                            f"WHERE S.MAX_ENROLLMENT - S.CURRENT_ENROLLMENT > 0 ")
                                        print(f"**SHOWING OPEN CLASSES IN LEVEL {level}**\n")
                                else:
                                    print(f"**ERROR: DEPARTMENT CODE {level.upper()} DOES NOT EXIST**\n")
                    else:
                        print("\n")
                        print("**ERROR: PICK NUMBER 1 OR 2 TO CONTINUE**\n")
                #-----------------------------------------------------------------------------       
            else:
                print("\n")
                print("**ERROR: PICK NUMBER 1 OR 2 TO CONTINUE**\n")
            #-------------------------------------SHOWS ALL CLASSES----------------------
    
    def addSection(self):
        # Gets course number
        self.executeSelect("SELECT * FROM SECTION")     
        print("What COURSE NUMBER do you want to add a section to?")
        course_num = input("Choice: ")
        print("\n")
        # Checks if the course number exists in the database
        if self.findMatch("COURSE_NUM", "SECTION", course_num) == False:
            print(f"**ERROR: COURSE NUMBER {course_num.upper()} DOES NOT EXIST**\n")
            return
        
        print("**ENTER THE FIELDS OF THE NEW SECTION**\n")
        
        #Generates the random number for the SECTION ID (SID)
        sid_id = random.randrange(1000, 10000)
        
        # Gets department number
        self.executeSelect("SELECT DEPT_CODE, DEPT_NAME FROM DEPT")
        dept_code = input("Enter DEPARTMENT CODE: ")
        print("\n")
        if self.findMatch("DEPT_CODE", "DEPT", dept_code) == False:
            print(f"**ERROR: DEPARTMENT CODE {dept_code.upper()} DOES NOT EXIST**\n")
            return
        
        # Gets professor id               
        self.executeSelect("SELECT PROF_ID, PROF_NAME FROM PROFESSOR")
        prof_id = input("Enter PROFESSOR ID: ")
        print("\n")
        if self.findMatch("PROF_ID", "PROFESSOR", prof_id) == False:
            print(f"**ERROR: PROFESSOR ID {prof_id.upper()} DOES NOT EXIST**\n")
            return
        
        # Gets room number    
        self.executeSelect("SELECT ROOM_NUM, BUILDING FROM ROOM")
        room_num = input("Enter ROOM NUMBER: ")
        print("\n")
        if self.findMatch("ROOM_NUM", "ROOM", room_num) == False:
            print(f"**ERROR: ROOM NUMBER {room_num.upper()} DOES NOT EXIST**\n")
            return
        
        # Gets building 
        self.executeSelect("SELECT BUILDING FROM DEPT")   
        building = input("Enter BUILDING: ")
        print("\n")
        if self.findMatch("BUILDING", "DEPT", building) == False:
            print(f"**ERROR: BUILDING {building.upper()} DOES NOT EXIST**\n")
            return
        
        # Checks that the inputs for days, start_time, end_time, start_day, end_day are in the correct format
        days_regex = re.compile(r'^[MTWRF]+$', re.IGNORECASE)
        days = input("Enter MEETING DAYS (e.g MTW): ")
        print("\n")
        if not days_regex.match(days) and days != "":
            print(f"**ERROR: WRONG FORMAT FOR MEETING DAYS**\n")
            return

        # Checks inputs for start_time
        time_regex = re.compile(r'^\d{2}:\d{2}:\d{2}$')
        start_time = input("Enter START TIME (hh:mm:ss): ")
        print("\n")
        if not time_regex.match(start_time) and start_time != "":
            print(f"**ERROR: WRONG FORMAT FOR START TIME**\n")
            return
        
        # Checks inputs for end_time    
        end_time = input("Enter END TIME: (hh:mm:ss): ")
        print("\n")
        if not time_regex.match(end_time) and end_time != "":
            print(f"**ERROR: WRONG FORMAT FOR END TIME**\n")
            return
            
        # Checks inputs for start_day. THIS CANNOT BE NULL
        date_regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        start_day = input("Enter START DAY (YYYY-MM-DD): ")
        print("\n")
        if not date_regex.match(start_day):
            print(f"**ERROR: WRONG FORMAT FOR START DAY. FIELD CANNOT BE NULL/EMPTY**\n")
            return

        # Checks inputs for end_day. THIS CANNOT BE NULL
        end_day = input("Enter END (YYYY-MM-DD): ")
        print("\n")
        if not date_regex.match(end_day):
            print(f"**ERROR: WRONG FORMAT FOR END DAY. FIELD CANNOT BE NULL/EMPTY**\n")
            return
        
        # Gets max enrollment
        max_enrollment_str = input("Enter MAX ENROLLMENT: ")
        if max_enrollment_str == "": # If nothing is entered current enrollment is set to default value
            max_enrollment = 0
        else:
            max_enrollment = int(max_enrollment_str)

        # Gets current enrollment
        current_enrollment_str = input("Enter CURRENT ENROLLMENT: ")
        if current_enrollment_str == "": # If nothing is entered current enrollment is set to default value
            current_enrollment = 0
        else:
            current_enrollment = int(current_enrollment_str)
            
        self.cursor.execute(f"INSERT INTO SECTION (SID, DEPT_CODE, COURSE_NUM, PROF_ID, ROOM_NUM, BUILDING, " 
                            f"DAYS, START_TIME, END_TIME, START_DAY, END_DAY, MAX_ENROLLMENT, CURRENT_ENROLLMENT) "
                            f"VALUES ('{sid_id}', '{dept_code.upper()}', '{course_num.upper()}', '{int(prof_id)}', '{int(room_num)}', '{building.upper()}', '{days.upper()}', "
                            f"'{start_time.upper()}', '{end_time.upper()}', '{start_day.upper()}', '{end_day.upper()}', '{max_enrollment}', '{current_enrollment}')")
        
        self.connection.commit()
        print("**NEW SECTION CREATED SUCCESSFULLY**\n")

    def findMatch(self, attribute, table, input_key):
        # Used to see if an input key is a tuple in a table's attribute
        self.cursor.execute(f"SELECT {attribute.upper()} FROM {table.upper()} WHERE {attribute.upper()} = '{input_key.upper()}'")
        result = self.cursor.fetchall()

        if len(result) > 0 or input_key == "":  # If there is a match from the query returns True else returns False
            return True
        else:
            return False

    def updateSection(self):
        print("\n")
        # Gets department number
        self.executeSelect("SELECT DEPT_CODE, DEPT_NAME FROM DEPT")
        dept_code = input("Enter DEPARTMENT CODE: ")
        print("\n")
        # Checks if the dept code exists in the database
        if self.findMatch("DEPT_CODE", "DEPT", dept_code) == False:
            print(f"**ERROR: DEPARTMENT CODE {dept_code.upper()} DOES NOT EXIST**\n")
            return
        
        # Gets course number
        self.executeSelect(f"SELECT COURSE_NUM FROM SECTION WHERE DEPT_CODE = '{dept_code.upper()}'")     
        course_num = input("Enter COURSE NUMBER: ")
        print("\n")
        # Checks if the course number exists in the database
        if self.findMatch("COURSE_NUM", "SECTION", course_num) == False:
            print(f"**ERROR: COURSE NUMBER {course_num.upper()} DOES NOT EXIST**\n")
            return
        
        # Shows all the sections that the matches of dept code and course number
        self.executeSelect(f"SELECT * FROM SECTION WHERE DEPT_CODE = '{dept_code.upper()}' AND COURSE_NUM = '{course_num}'")
        print("\n")
        
        # Asks user for the section id
        section_id = input("Enter SECTION ID(SID) you want to update: ")
        print("\n")
        # Checks that the section id exists
        if self.findMatch("SID", "SECTION", section_id) == False:
            print(f"**ERROR: SECTION ID(SID) {course_num.upper()} DOES NOT EXIST**\n")
            return
        
        # Asks user what fields wants to update
        field = input("Enter field you want to update: ")
 
        # Checks that the field is not a primary key or composite primary key 
        if field.upper() not in ["DEPT_CODE", "COURSE_NUM", "PROF_ID", "ROOM_NUM", "BUILDING", "DAYS", 
                                 "START_TIME", "END_TIME", "START_DATE", "END_DATE", "MAX_ENROLLMENT", "CURRENT_ENROLLMENT"]:
            print("**ERROR: INVALID FIELD ENTERED**\n")
            return
        elif field == "SID":
            print("**ERROR: CANNOT UPDATE PRIMARY KEY**\n")
            return
        elif field in ["DEPT_CODE", "COURSE_NUM"]:
            print("**ERROR: CANNOT UPDATE COMPOSITE PRIMARY KEY**\n")
            return

        new_value = input(f"Enter new value for {field.upper()}: ")
        print("\n")

        # Updates the field with the new value entered
        self.cursor.execute(f"UPDATE SECTION SET {field.upper()} = '{new_value.upper()}' WHERE SID = {section_id}")
        print("**SUCCESSFULLY UPDATED**\n")
        
        
    def report(self):   # Shows all the enrollments by department
        print("\n")
        self.executeSelect("""SELECT d.DEPT_NAME, SUM(s.CURRENT_ENROLLMENT) AS TOTAL_ENROLLMENTS FROM DEPT d
                                INNER JOIN COURSE c ON d.DEPT_CODE = c.DEPT_CODE INNER JOIN SECTION s ON c.COURSE_NUM = 
                                s.COURSE_NUM AND c.DEPT_CODE = s.DEPT_CODE GROUP BY d.DEPT_NAME;""")
        
        print("**SHOWING ALL THE ENROLLMENTS BY DEPARTMENT**\n")

        
    def close_db(self):  # use this function to close db
        self.cursor.close()
        self.connection.close()


