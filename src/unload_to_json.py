import json
from dotenv import load_dotenv
import os
import psycopg2
from pathlib import Path

load_dotenv()

class UnloadToJson(): 
  """This is the parent class where all 
     the other child classes(subclasses), 
     will inherit and extend from.
  """         
  def __init__(self,con,cu):
    self.con = con
    self.cu = cu
  def unload_to_json(self,output_filepath)->None:
    pass

class RoomsWithDiffSexStudents(UnloadToJson):
  def unload_to_json(self, output_filepath)->None:
    try:
      sql = """
            SELECT * FROM RoomsWithDiffSexStudents

          """
      self.cu.execute(sql)
      self.con.commit()
      new_rows = self.cu.fetchmany(20)
    except Exception as e:
      print(f"Could not execute query because of: {e}")
    try:
      new_data = {"Room":1}
      new_data_list = []
      for new_row in new_rows:
        new_data["Room"]=new_row[0]
        new_data_list.append({"Room":new_row[0]})
        with open(output_filepath,"r",encoding="utf-8") as f:
          old_data=json.load(f)
          if new_data not in old_data:
           old_data.append(new_data)
        with open(output_filepath,"w",encoding="utf-8") as f:
         json.dump(old_data,f,ensure_ascii=False,indent=4)   # ensure_ascii makes sure that Non-Ascii values are readable
      print(f"List of rooms with diff sex students: {new_data_list}")
    except Exception as e:
      print("Could not unload data because of:",e)
      
   

class NumberOfStudentsInRooms(UnloadToJson):
  def unload_to_json(self, output_filepath)->None:
    try:
      sql = """
            SELECT * FROM NumberOfStudentsInRooms

          """
      self.cu.execute(sql)
      self.con.commit()
      new_rows = self.cu.fetchmany(20) 
    except Exception as e:
      print(f"Could not execute query because of: {e}")
    try:
      new_data = {"Room":1,"Student Count":1}
      new_data_list = []
      for new_row in new_rows:
        new_data["Room"]=new_row[0]
        new_data["Student Count"]=new_row[1]
        new_data_list.append({"Room":new_row[0],"Student Count":new_row[1]})
        with open(output_filepath,"r",encoding="utf-8") as f:
          old_data=json.load(f)
          if new_data not in old_data:
           old_data.append(new_data)
        with open(output_filepath,"w",encoding="utf-8") as f:
         json.dump(old_data,f,ensure_ascii=False,indent=4)   # ensure_ascii makes sure that Non-Ascii values are readable
      print(f"List of rooms and num of students in each room: {new_data_list}")
    except Exception as e:
      print("Could not unload data because of:",e)
    

class RoomsWithSmallestAvgAge(UnloadToJson):
  def unload_to_json(self, output_filepath)->None:
    try:
      sql = """
            SELECT * FROM RoomsWithSmallestAvgAge
            LIMIT 5

          """
      self.cu.execute(sql)
      self.con.commit()
      new_rows = self.cu.fetchmany(20)
    except Exception as e:
      print(f"Could not execute query because of: {e}")
    try:
      new_data = {"Room":1,"AvgStudentAge":1.00}
      new_data_list = []
      for new_row in new_rows:
        new_data["Room"]=new_row[0]
        avg_student_age = float(new_row[1])
        new_data["AvgStudentAge"]=avg_student_age
        new_data_list.append({"Room":new_row[0],"AvgStudentAge":avg_student_age})
        with open(output_filepath,"r",encoding="utf-8") as f:
          old_data=json.load(f)
          if new_data not in old_data:
           old_data.append(new_data)
        with open(output_filepath,"w",encoding="utf-8") as f:
         json.dump(old_data,f,ensure_ascii=False,indent=4)   # ensure_ascii makes sure that Non-Ascii values are readable
      print(f"Rooms with smallest avg age: {new_data_list}")
    except Exception as e:
      print("Could not unload data because of:",e)
      
class RoomsWithLargestAgeDiff(UnloadToJson):
  def unload_to_json(self, output_filepath)->None:
    try:
      sql = """
            SELECT * FROM RoomsWithTheLargestAgeDiff
            LIMIT 5

          """
      self.cu.execute(sql)
      self.con.commit()
      new_rows = self.cu.fetchmany(20)
    except Exception as e:
      print(f"Could not execute query becuase of {e}")
    try:
      new_data = {"Room":1,"StudentAgeDiff":1.00}
      new_data_list = []
      for new_row in new_rows:
        new_data["Room"]=new_row[0]
        student_age_diif = float(new_row[1])
        new_data["StudentAgeDiff"]=student_age_diif
        new_data_list.append({"Room":new_row[0],"StudentAgeDiff":student_age_diif})
        with open(output_filepath,"r",encoding="utf-8") as f:
          old_data=json.load(f)
          if new_data not in old_data:
           old_data.append(new_data)
        with open(output_filepath,"w",encoding="utf-8") as f:
          json.dump(old_data,f,ensure_ascii=False,indent=4)   # ensure_ascii makes sure that Non-Ascii values are readable
      print(f"Rooms with largest diff in student age: {new_data_list}")
    except Exception as e:
      print("Could not unload data becuase of:",e)
        
def main():
  BASE_DIR_UNLOAD = Path(__file__).parent
  output_filepath01 = BASE_DIR_UNLOAD/"data"/"curated_reporting_json"/"RoomsWithDiffSexStudents.json"
  output_filepath02 = BASE_DIR_UNLOAD/"data"/"curated_reporting_json"/"NumberOfStudentsInRooms.json"
  output_filepath03 = BASE_DIR_UNLOAD/"data"/"curated_reporting_json"/"RoomsWithSmallestAvgAge.json"
  output_filepath04 = BASE_DIR_UNLOAD/"data"/"curated_reporting_json"/"RoomsWithLargestAgeDiff.json"
  
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
    print(f"Could not connect to databse because of {e}")
  print("""Here are the available dataset options to view📊:
           1. Number of students in each rooms, Enter 1 to view it
           2. Rooms with different sex students, Enter 2 to view it
           3. 5 Rooms with the largest age difference, Enter 3 to view it
           4. 5 Rooms with smallest average age, Enter 4 to view it
           5. Enter 5 to view all Datasets
        """)
  dataset_1:str = input("Enter 1 to view NumberOfStudentsInRooms or any character to skip$")
  if dataset_1.strip() == "1":
    NumberOfStudentsInRooms(conn,cur).unload_to_json(output_filepath02) 
  dataset_2:str = input("Enter 2 to view RoomsWithDiffSexStudents or any charcter to skip$")
  if dataset_2.strip() == "2":
     RoomsWithDiffSexStudents(conn,cur).unload_to_json(output_filepath01)
  dataset_3:str = input("Enter 3 to view 5 RoomsWithLargestAgeDiff or any character to skip$")
  if dataset_3.strip() == "3":
     RoomsWithLargestAgeDiff(conn,cur).unload_to_json(output_filepath04)
  dataset_4:str = input("Enter 4 to view 5 RoomsWithSmallestAvgAge or any charcter to skip$")
  if dataset_4.strip() == "4":
    RoomsWithSmallestAvgAge(conn,cur).unload_to_json(output_filepath03)
  all_datasets:str = input("Enter 5 to View all Datasets or any character to skip$")
  if all_datasets.strip() == "5":
    NumberOfStudentsInRooms(conn,cur).unload_to_json(output_filepath02)
    print()
    RoomsWithDiffSexStudents(conn,cur).unload_to_json(output_filepath01)
    print()
    RoomsWithLargestAgeDiff(conn,cur).unload_to_json(output_filepath04)
    print()
    RoomsWithSmallestAvgAge(conn,cur).unload_to_json(output_filepath03)

  cur.close()
  conn.close()
  print("ETL Completed succefully✅, see you soon! 👋")

if __name__ == "__main__":
  main()
