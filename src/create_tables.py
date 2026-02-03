import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class CreateTables:
   def __init__(self,con,cu):
      self.con = con
      self.cu = cu
   def trigger(self) -> None:
      pass
   
class CreateRoomsTable(CreateTables):
    def trigger(self) -> None:
      try:
        rooms_table: str = """
                CREATE TABLE IF NOT EXISTS rooms(
                room_id INT PRIMARY KEY,
                name TEXT NOT NULL,
                inserted_at TIMESTAMP DEFAULT NOW()
                )
            """
        self.cu.execute(rooms_table)
        self.con.commit()
      except:
         print("Could not Create rooms table")
      
class CreateStudentsTable(CreateTables):
  def trigger(self) -> None:
    try:
        students_table: str = """
            CREATE TABLE IF NOT EXISTS students(
            student_id INT PRIMARY KEY,
            name TEXT NOT NULL, 
            room_id INT references rooms(room_id),
            birthday DATE,
            sex TEXT NOT NULL,
            inserted_at TIMESTAMP DEFAULT NOW()
            )
        """

        self.cu.execute(students_table)
        self.con.commit()
    except:
       print("Could not Create students table")

if __name__ == "__main__":
  
  try:
    credentials = {"password":os.getenv("POSTGRES_PASSWORD"),
                "dbname":os.getenv("POSTGRES_DB"),
                "user":os.getenv("POSTGRES_USER"),
                "host":os.getenv("POSTGRES_HOST"),
                "port":os.getenv("POSTGRES_PORT")
                }

    conn = psycopg2.connect(**credentials)
    cur = conn.cursor()
  except:
   print("Could not connect to Database!")

  CreateRoomsTable(conn,cur).trigger()
  CreateStudentsTable(conn,cur).trigger()
  cur.close()
  conn.close()
   