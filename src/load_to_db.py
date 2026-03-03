import os
from dotenv import load_dotenv
import psycopg2
import json
from pathlib import Path

try:
    from .logs import get_logger  # when imported as package
except ImportError:
    from logs import get_logger   # when run directly as script


load_dotenv()
logger = get_logger()

class LoadToDb:                      #Parent class
   def __init__(self,file_path,con,cu,rows,sql,table_name,data):
      self.file_path = file_path
      self.conn = con
      self.cu = cu
      self.rows = rows
      self.sql = sql
      self.table_name = table_name
      self.data = data # this is where we are going to unload the contents in the json file to e.g [{"id":122,"name":"Daniel"},{....},..]
   def load_data(self) -> None:
         if self.file_path:
            with open(self.file_path,"r",encoding="utf-8") as f:
                  self.data = json.load(f)
         else:
           raise FileNotFoundError(f"You entered the wrong filename, Try {self.table_name}.json")
         
class Rooms(LoadToDb):               
      def load_data(self) -> None:
         super().load_data()
         self.rows = [(item['id'],item['name']) for item in self.data]
         try:
            for row in self.rows:
               self.cu.execute(self.sql,row)
         except Exception:
            logger.error(f"Insertion or Update into {self.table_name} table failed!",exc_info=True)


class Students(LoadToDb):
      def load_data(self) -> None:
         super().load_data()
         self.rows =  [(item['id'],item['name'],item['room'],item['birthday'],item['sex'] ) for item in self.data]
         try:
            for row in self.rows:
               self.cu.execute(self.sql,row)
         except Exception:
            logger.error(f"Insertion or Update into {self.table_name} table failed!",exc_info=True)


def main() -> None:

  user_name:str = input("Please Register a once-of username$ ")
  if user_name:
     print(f"Hello {user_name.strip()}!. Welcome to the ETL")
  students_filename:str = " "
  while students_filename != "students.json":
    students_filename:str = input("Enter Students file name with extention(.json)$ ")
    if students_filename == "students.json":
       break
    else:
       print("You entered the wrong students filename.Try students.json")
    
  rooms_filename:str  = " "
  while rooms_filename != "rooms.json":
     rooms_filename:str  = input("Enter Rooms file name with extention(.json)$ ")
     if rooms_filename == "rooms.json":
        break
     else:
        print("You entered the wrong rooms filename.Try rooms.json")
  logger.info("Starting to insert/update data....🧑‍💻")   
  BASE_DIR = Path(__file__).parent.parent                                     
  students_filepath = BASE_DIR/"data"/"raw_json"/students_filename.lower().strip()
  rooms_filepath = BASE_DIR/"data"/"raw_json"/ rooms_filename.lower().strip()
  data: list = []
  rooms_rows: list = []
  students_rows:list = []
  rooms_sql:str = """
                     INSERT INTO rooms(room_id,name)
                     VALUES(%s,%s)
                     ON CONFLICT (room_id) DO UPDATE
                     SET room_id = EXCLUDED.room_id;
                  """       
  students_sql:str = """
                     INSERT INTO students(student_id,name,room_id,birthday,sex)
                     VALUES(%s,%s,%s,%s,%s)
                     ON CONFLICT (student_id) DO UPDATE
                     SET student_id = EXCLUDED.student_id;
                  """ 
  rooms_table = "rooms"
  students_table = "students"     
  
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
     logger.error("Driver could not connect to Database!",exc_info=True)
     return
  
  Rooms(rooms_filepath,conn,cur,rooms_rows,rooms_sql,rooms_table,data).load_data()
  Students(students_filepath,conn,cur,students_rows,students_sql,students_table,data).load_data()
  conn.commit()
  cur.close()
  conn.close()
  logger.info("Data inserted/updated successfully to rooms and students table!✅")
        
if __name__ == "__main__":
    main()