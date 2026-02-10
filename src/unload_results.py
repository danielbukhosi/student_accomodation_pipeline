import json
from dotenv import load_dotenv
import os
import psycopg2
import sys
import logging
import xml.etree.ElementTree as ET
import xml.dom.minidom as md
from pathlib import Path

load_dotenv()
logger = logging.getLogger("UnloadToDb")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class UnloadToJsonXml(): 
  """This is the parent class where all 
     the other child classes(subclasses), 
     will inherit and extend from.
  """         
  def __init__(self,con,cu):
    self.con = con
    self.cu = cu
  def unload_to_json(self)->None:
    pass
  def unload_to_xml(self)->None:
    pass

# THE FOLLOWING CLASSES WILL UNLOAD RESULTS AS JSON FORMAT... APIs APIs where are you?
class RoomsWithDiffSexStudentsJ(UnloadToJsonXml):
  def unload_to_json(self)->None:
    try:
      sql = """
            SELECT DISTINCT diff_sex_rooms FROM RoomsWithDiffSexStudents

          """
      self.cu.execute(sql)
      self.con.commit()
    except Exception as e:
      logger.error(f"Could not execute query because of: {e}",exc_info=True)
    try:
      new_data = {"Room":1}
      new_data_list = []
      rows = 0
      for new_row in self.cu:
        new_data["Room"]=new_row[0]
        new_data_list.append({"Room":new_row[0]})
        rows += 1
      json.dump(new_data_list,sys.stdout,ensure_ascii=False,indent=4) # ensure_ascii makes sure that Non-Ascii values are readable
      print()
      logger.info(f"Number of rows:{rows}")
      #print(f"List of rooms with diff sex students: {new_data_list}")  NOT NECCESSARY IF sys.stdout is implemented
    except Exception as e:
      logger.error(f"Could not unload data because of:{e}",exc_info=True)
      
   

class NumberOfStudentsInRoomsJ(UnloadToJsonXml):
  def unload_to_json(self)->None:
    try:
      sql = """
            SELECT * FROM NumberOfStudentsInRooms

          """
      self.cu.execute(sql)
      self.con.commit() 
    except Exception as e:
      logger.error(f"Could not execute query because of: {e}",exc_infor=True)
    try:
      new_data = {"Room":1,"Student Count":1}
      new_data_list = []
      rows = 0
      for new_row in self.cu:
        new_data["Room"]=new_row[0]
        new_data["Student Count"]=new_row[1]
        new_data_list.append({"Room":new_row[0],"Student Count":new_row[1]})
        rows += 1
      json.dump(new_data_list,sys.stdout,ensure_ascii=False,indent=4)   # ensure_ascii makes sure that Non-Ascii values are readable
      print()
      logger.info(f"Number of rows:{rows}")
      #print(f"List of rooms and num of students in each room: {new_data_list}") NOT neccessary since sys.stdout is implemented
    except Exception as e:
      logger.error(f"Could not unload data because of: {e}",exc_info=True)
    

class RoomsWithSmallestAvgAgeJ(UnloadToJsonXml):
  def unload_to_json(self)->None:
    try:
      sql = """
            SELECT * FROM RoomsWithSmallestAvgAge
            LIMIT 5

          """
      self.cu.execute(sql)
      self.con.commit()
    except Exception as e:
      logger.error(f"Could not execute query because of: {e}",exc_info=True)
    try:
      new_data = {"Room":1,"AvgStudentAge":1.00}
      new_data_list = []
      rows = 0
      for new_row in self.cu:
        new_data["Room"]=new_row[0]
        avg_student_age = float(new_row[1])
        new_data["AvgStudentAge"]=avg_student_age
        new_data_list.append({"Room":new_row[0],"AvgStudentAge":avg_student_age})
        rows += 1
      json.dump(new_data_list,sys.stdout,ensure_ascii=False,indent=4)   # ensure_ascii makes sure that Non-Ascii values are readable
      print()
      #print(f"Rooms with smallest avg age: {new_data_list}") NOT neccessary since sys.stdout is implemented
      logger.info(f"Number of rows:{rows}")
    except Exception as e:
      logger.error(f"Could not unload data because of: {e}",exc_info=True)
      
class RoomsWithLargestAgeDiffJ(UnloadToJsonXml):
  def unload_to_json(self)->None:
    try:
      sql = """
            SELECT * FROM RoomsWithTheLargestAgeDiff
            LIMIT 5

          """
      self.cu.execute(sql)
      self.con.commit()
    except Exception as e:
      logger.error(f"Could not execute query becuase of {e}",exc_info=True)
    try:
      new_data = {"Room":1,"StudentAgeDiff":1.00}
      new_data_list = []
      rows = 0
      for new_row in self.cu:
        new_data["Room"]=new_row[0]
        student_age_diif = float(new_row[1])
        new_data["StudentAgeDiff"]=student_age_diif
        new_data_list.append({"Room":new_row[0],"StudentAgeDiff":student_age_diif})
        rows += 1
      json.dump(new_data_list,sys.stdout,ensure_ascii=False,indent=4)   # ensure_ascii makes sure that Non-Ascii values are readable
      print()
      logger.info(f"Number of rows:{rows}")
      #print(f"Rooms with largest diff in student age: {new_data_list}") NOT neccessary since sys.stdout is implemented
    except Exception as e:
      logger.error(f"Could not unload data becuase of: {e}",exc_info=True)

# THE FOLLOWING CLASSES UNLOAD THE RESULTS AS XML FORMAT </>... LETS GO OLD SCHOOL!

class RoomsWithDiffSexStudentsX(UnloadToJsonXml):
  def unload_to_xml(self)->None:
    try:
      sql = """
            SELECT DISTINCT diff_sex_rooms FROM RoomsWithDiffSexStudents
           """
      self.cu.execute(sql)
      self.con.commit()
    except Exception as e:
      logger.error(f"Could not execute query because of: {e}",exc_info=True)
    try:
      root = ET.Element("RoomsWithDiffSexStudents")  # This creates the root element which wrapps the entire XML document contents.
      rows = 0
      for new_row in self.cu: # iterating the cursor directly is advantageous because it behaves like a generator .
        id = str(new_row[0])
        ET.SubElement(root,"room",id=id)
        rows += 1
      xml_bytes = ET.tostring(root,encoding="utf-8")  # Converts ElementTree objects to strings
      pretty = md.parseString(xml_bytes).toprettyxml(indent="    ")  # This displays XML conent just like a DOM
      sys.stdout.write(pretty)  # prints to standard output
      print()
      logger.info(f"number of rows:{rows}")
    except Exception as e:
      logger.error(f"Could not unload data because of:{e}",exc_info=True)  #Opps!

class NumberOfStudentsInRoomsX(UnloadToJsonXml):
  def unload_to_xml(self)->None:
    try:
      sql = """
            SELECT * FROM NumberOfStudentsInRooms
          """
      self.cu.execute(sql)
      self.con.commit()
    except Exception as e:
      logger.error(f"Could not execute query because of: {e}",exc_info=True)
    try:
      root = ET.Element("NumberOfStudentsInRooms")  # This creates the root element which wrapps the entire XML document contents.
      rows = 0
      for new_row in self.cu: # iterating the cursor directly is advantageous because it behaves like a generator .
        id = str(new_row[0])
        student_count = str(new_row[1])
        room = ET.SubElement(root,"room",id=id)
        ET.SubElement(room,"StudentCount").text = student_count
        rows += 1
      xml_bytes = ET.tostring(root,encoding="utf-8")  # Converts ElementTree objects to strings
      pretty = md.parseString(xml_bytes).toprettyxml(indent="    ")  # This displays XML conent just like a DOM
      sys.stdout.write(pretty)  # prints to standard output
      print()
      logger.info(f"number of rows:{rows}")
    except Exception as e:
      logger.error(f"Could not unload data because of:{e}",exc_info=True)  #Opps!

class RoomsWithSmallestAvgAgeX(UnloadToJsonXml):
  def unload_to_xml(self)->None:
    try:
      sql = """
            SELECT * FROM RoomsWithSmallestAvgAge
            LIMIT 5
           """
      self.cu.execute(sql)
      self.con.commit()
    except Exception as e:
      logger.error(f"Could not execute query because of: {e}",exc_info=True)
    try:
      root = ET.Element("RoomsWithSmallestAvgAge")  # This creates the root element which wrapps the entire XML document contents.
      rows = 0
      for new_row in self.cu: # iterating the cursor directly is advantageous because it behaves like a generator .
        id = str(new_row[0])
        avg_student_age = str(new_row[1])
        room = ET.SubElement(root,"room",id=id)
        ET.SubElement(room,"AvgStudentAge").text = avg_student_age
        rows += 1
      xml_bytes = ET.tostring(root,encoding="utf-8")  # Converts ElementTree objects to strings
      pretty = md.parseString(xml_bytes).toprettyxml(indent="    ")  # This displays XML conent just like a DOM
      sys.stdout.write(pretty)  # prints to standard output
      print()
      logger.info(f"number of rows:{rows}")
    except Exception as e:
      logger.error(f"Could not unload data because of:{e}",exc_info=True)  #Opps!

class RoomsWithLargestAgeDiffX(UnloadToJsonXml):
  def unload_to_xml(self)->None:
    try:
      sql = """
            SELECT * FROM RoomsWithTheLargestAgeDiff
            LIMIT 5
           """
      self.cu.execute(sql)
      self.con.commit()
    except Exception as e:
      logger.error(f"Could not execute query because of: {e}",exc_info=True)
    try:
      root = ET.Element("RoomsWithLargestAgeDiffX")  # This creates the root element which wrapps the entire XML document contents.
      rows = 0
      for new_row in self.cu: # iterating the cursor directly is advantageous because it behaves like a generator .
        id = str(new_row[0])
        student_age_diff =str(new_row[1])
        room = ET.SubElement(root,"room",id=id)
        ET.SubElement(room,"StudentAgeDiff").text = student_age_diff
        rows += 1
      xml_bytes = ET.tostring(root,encoding="utf-8")  # Converts ElementTree objects to strings
      pretty = md.parseString(xml_bytes).toprettyxml(indent="    ")  # This displays XML conent just like a DOM
      sys.stdout.write(pretty)  # prints to standard output
      print()
      logger.info(f"number of rows:{rows}")
    except Exception as e:
      logger.error(f"Could not unload data because of:{e}",exc_info=True)  #Opps!
        
def main():
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
    logger.error(f"Could not connect to databse because of {e}",exc_info=True)
    return
  print("""Here are the available dataset options in 2 different formats to view📊:
           1. Number of students in each rooms, Enter 1 to view it
           2. Rooms with different sex students, Enter 2 to view it
           3. 5 Rooms with the largest age difference, Enter 3 to view it
           4. 5 Rooms with smallest average age, Enter 4 to view it
           5. Enter 5 to view all Datasets
        """)
  exit_key: str = " "
  while exit_key != "exit":
    json_format: str = input("Type json to view data in json format or any key to skip$ ").lower().strip()
    if json_format == "json":
      dataset_1:str = input("Enter 1 to view NumberOfStudentsInRooms or any character to skip$ ")
      if dataset_1.strip() == "1":
        NumberOfStudentsInRoomsJ(conn,cur).unload_to_json() 
      dataset_2:str = input("Enter 2 to view RoomsWithDiffSexStudents or any charcter to skip$ ")
      if dataset_2.strip() == "2":
        RoomsWithDiffSexStudentsJ(conn,cur).unload_to_json()
      dataset_3:str = input("Enter 3 to view 5 RoomsWithLargestAgeDiff or any character to skip$ ")
      if dataset_3.strip() == "3":
        RoomsWithLargestAgeDiffJ(conn,cur).unload_to_json()
      dataset_4:str = input("Enter 4 to view 5 RoomsWithSmallestAvgAge or any charcter to skip$ ")
      if dataset_4.strip() == "4":
        RoomsWithSmallestAvgAgeJ(conn,cur).unload_to_json()
      all_datasets:str = input("Enter 5 to View all Datasets or any character to skip$ ")
      if all_datasets.strip() == "5":
        NumberOfStudentsInRoomsJ(conn,cur).unload_to_json()
        print()
        RoomsWithDiffSexStudentsJ(conn,cur).unload_to_json()
        print()
        RoomsWithLargestAgeDiffJ(conn,cur).unload_to_json()
        print()
        RoomsWithSmallestAvgAgeJ(conn,cur).unload_to_json()
    xml_format: str = input("Type xml to view the data in xml format or any key to skip$ ").lower().strip()
    if xml_format == "xml":
      datasetX_1:str = input("Enter 1 to view NumberOfStudentsInRooms or any character to skip$ ")
      if datasetX_1.strip() == "1":
        NumberOfStudentsInRoomsX(conn,cur).unload_to_xml() 
      datasetX_2:str = input("Enter 2 to view RoomsWithDiffSexStudents or any charcter to skip$ ")
      if datasetX_2.strip() == "2":
        RoomsWithDiffSexStudentsX(conn,cur).unload_to_xml()
      datasetX_3:str = input("Enter 3 to view 5 RoomsWithLargestAgeDiff or any character to skip$ ")
      if datasetX_3.strip() == "3":
        RoomsWithLargestAgeDiffX(conn,cur).unload_to_xml()
      datasetX_4:str = input("Enter 4 to view 5 RoomsWithSmallestAvgAge or any charcter to skip$ ")
      if datasetX_4.strip() == "4":
        RoomsWithSmallestAvgAgeX(conn,cur).unload_to_xml()
      all_datasetsX:str = input("Enter 5 to View all Datasets or any character to skip$ ")
      if all_datasetsX.strip() == "5":
        NumberOfStudentsInRoomsX(conn,cur).unload_to_json()
        print()
        RoomsWithDiffSexStudentsX(conn,cur).unload_to_xml()
        print()
        RoomsWithLargestAgeDiffX(conn,cur).unload_to_xml()
        print()
        RoomsWithSmallestAvgAgeX(conn,cur).unload_to_xml()
    exit_key = input("To excape type exit or any key to continue viewing data!$ ") # DON'T GET STUCK OKAYY??
    if exit_key == "exit":
      break                   #YOU ARE FREE!!
    else:
      continue          #STILL WANT TO SEE MORE INSIGHTS
  
   
  cur.close()
  conn.close()
  logger.info("ETL Completed succefully✅, see you soon! 👋")  # THE END :)

if __name__ == "__main__":
  main()
