import psycopg2
from dotenv import load_dotenv
import logging
import sys
import os

load_dotenv()
logger =  logging.getLogger("CreateViews")
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class CreateViews:
  def __init__(self,con,cu):
     self.con = con
     self.cu = cu
  def create_views(self) -> None:
     pass
  
class NumberOfStudentsInRoomsView(CreateViews):
   def create_views(self) -> None:
      try:
          sql: str = """
              
              CREATE OR REPLACE VIEW NumberOfStudentsInRooms AS
              SELECT DISTINCT room_id AS room,
                    count(student_id) AS students_count
              FROM students
              GROUP BY room
              ORDER BY students_count DESC;
            """
          self.cu.execute(sql)
          self.con.commit()
      except Exception as e:
         logger.error("Could not Create views in DataBase!, alter1", exc_info=True)

class RoomsWithSmallestAvgAgeView(CreateViews):
   def create_views(self) -> None:
       try:
            sql:str = """
                      CREATE OR REPLACE VIEW RoomsWithSmallestAvgAGe AS
                      SELECT DISTINCT room_id AS room,
                            ROUND(AVG(2026-(EXTRACT(YEAR FROM birthday))),2) as avg_student_age
                      FROM students
                      GROUP BY room
                      ORDER BY avg_student_age ASC;
                """
            self.cu.execute(sql)
            self.con.commit()
       except Exception  as e:
          logger.error("Could not Create Views in DataBase!, alert2", exc_info=True)

class RoomsWithLargestAgeDiffView(CreateViews):
   def create_views(self) -> None:
       try:
            sql: str = """
                      CREATE OR REPLACE VIEW RoomsWithTheLargestAgeDiff AS
                      SELECT DISTINCT room_id AS room,
                            ROUND(STDDEV_POP(2026-EXTRACT(YEAR FROM birthday)),2) AS student_age_diff
                      FROM students
                      GROUP BY room
                      ORDER BY student_age_diff DESC
                  """
            self.cu.execute(sql)
            self.con.commit()
       except Exception  as e:
          logger.error("Could not Create Views in DataBase!, alert3", exc_info=True)


class RoomsWithDiffSexStudentsView(CreateViews):
   def create_views(self)->None:
       try:
            sql: str = """
                      CREATE OR REPLACE VIEW RoomsWithDiffSexStudents AS
                      WITH cte_1 AS(
                      SELECT room_id  AS rooms_with_F
                      FROM students
                      WHERE sex = 'F'
                      ),
                      cte_2 AS(
                      SELECT rooms_with_F AS diff_sex_rooms
                      from cte_1
                      where rooms_with_F in
                      (SELECT room_id  
                      FROM students
                      WHERE sex = 'M'
                      ))
                      SELECT  diff_sex_rooms
                      FROM cte_2
                  """
            self.cu.execute(sql)
            self.con.commit()
       except Exception  as e:
          logger.error("Could not Create Views in DataBase!, alert4", exc_infor=True)

def main()-> None:
   logger.info("Starting to Create views...")
   try:
      credentials = {"password":os.getenv("POSTGRES_PASSWORD"),
                  "dbname":os.getenv("POSTGRES_DB"),
                  "user":os.getenv("POSTGRES_USER"),
                  "host":os.getenv("POSTGRES_HOST"),
                  "port":os.getenv("POSTGRES_PORT")
                  }

      conn = psycopg2.connect(**credentials)
      cur = conn.cursor()
   except Exception as e:
     logger.error("Could not connect to Database!", exc_info=True)
     return
    
   NumberOfStudentsInRoomsView(conn,cur).create_views()
   RoomsWithSmallestAvgAgeView(conn,cur).create_views()
   RoomsWithLargestAgeDiffView(conn,cur).create_views()
   RoomsWithDiffSexStudentsView(conn,cur).create_views()  

   cur.close()
   conn.close()
   logger.info("Views created successfully✅")


if __name__ == "__main__":
   main()
