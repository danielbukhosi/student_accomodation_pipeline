import os
from dotenv import load_dotenv
import psycopg2
import json
from pathlib import Path

load_dotenv()


class LoadToDb:                      #Parent class
   def __init__(self,file_path,con,cu):
      self.file_path = file_path
      self.conn = con
      self.cu = cu
   def load_data(self) -> None:
      pass
   
class Rooms(LoadToDb):               
      def load_data(self,file_path) -> None:
         if self.file_path == file_path:
            with open(self.file_path,"r",encoding="utf-8") as f:
                  data = json.load(f)
         else:
           raise TypeError("You entered the wrong filename, Try rooms.json")
         
         try:
            rows: list = [(item['id'],item['name']) for item in data]
            for row in rows:
               sql:str = """
                     INSERT INTO rooms(room_id,name)
                     VALUES(%s,%s)
                     ON CONFLICT (room_id) DO UPDATE
                     SET room_id = EXCLUDED.room_id;
                  """
               self.cu.execute(sql,row)
               self.conn.commit()
         except Exception as e:
            print("Insertion or Update into rooms table failed!",e)


class Students(LoadToDb):
      def load_data(self,file_path) -> None:
          if self.file_path == file_path:
            with open(self.file_path,"r",encoding="utf-8") as f:
               data = json.load(f)
          else:
            raise TypeError("You entered the wrong filename, Try students.json")
          try :
            rows: list = [(item['id'],item['name'],item['room'],item['birthday'],item['sex'] ) for item in data]
            for row in rows:
               sql:str = """
                     INSERT INTO students(student_id,name,room_id,birthday,sex)
                     VALUES(%s,%s,%s,%s,%s)
                     ON CONFLICT (student_id) DO UPDATE
                     SET student_id = EXCLUDED.student_id;
                  """
               self.cu.execute(sql,row)
               self.conn.commit()
          except Exception as e :
              print("Insertion or Update into students table failed!",e)

def main() -> None:
  user_name:str = input("Please Register a once-of username$")
  if user_name:
     print(f"Hello {user_name.strip()}!. Welcome to the ETL")
  students_filename:str = " "
  while students_filename != "students.json":
    students_filename:str = input("Enter Students file name with extention(.json)$")
    if students_filename == "students.json":
       break
    else:
       print("You entered the wrong students filename.Try students.json")
    
  rooms_filename:str  = " "
  while rooms_filename != "rooms.json":
     rooms_filename:str  = input("Enter Rooms file name with extention(.json)$")
     if rooms_filename == "rooms.json":
        break
     else:
        print("You entered the wrong rooms filename.Try rooms.json")
  print("Starting to insert/update data....🧑‍💻")   
  BASE_DIR = Path(__file__).parent                                     
  students_filepath = BASE_DIR/"data"/"raw_json"/students_filename.lower().strip()
  rooms_filepath = BASE_DIR/"data"/"raw_json"/ rooms_filename.lower().strip()
  
  try:
   credentials = {"dbname":os.getenv("POSTGRES_DB"),
                  "user":os.getenv("POSTGRES_USER"),
                  "host":os.getenv("POSTGRES_HOST"),
                  "port":os.getenv("POSTGRES_PORT"),
                  "password":os.getenv("POSTGRES_PASSWORD")
                  }

   conn = psycopg2.connect(**credentials)
   cur = conn.cursor()
  except Exception as e:
     print("Driver could not connect to Database!",e)
  
  Rooms(rooms_filepath,conn,cur).load_data(rooms_filepath)
  Students(students_filepath,conn,cur).load_data(students_filepath)
  cur.close()
  conn.close()
  print("Data inserted/updated successfully to rooms and students table!✅")
        


if __name__ == "__main__":
    main()
    

                 
          
