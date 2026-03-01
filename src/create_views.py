import psycopg2
from dotenv import load_dotenv
from logs import create_views_log
import os

load_dotenv()
logger =  create_views_log()

class CreateViews:
  def __init__(self,con,cu,sql):
     self.con = con
     self.cu = cu
     self.sql = sql
  def create_views(self) -> None:
     try:
          self.cu.execute(self.sql)
          self.con.commit()
     except Exception as e:
         logger.error("Could not Create views in DataBase!, alter1", exc_info=True)
  
class NumberOfStudentsInRoomsView(CreateViews):
   def create_views(self) -> None:
      super().create_views()

class RoomsWithSmallestAvgAgeView(CreateViews):
   def create_views(self) -> None:
       super().create_views()

class RoomsWithLargestAgeDiffView(CreateViews):
   def create_views(self) -> None:
       super().create_views()

class RoomsWithDiffSexStudentsView(CreateViews):
   def create_views(self)->None:
      super().create_views()

def main()-> None:
   logger.info("Starting to Create views...")   
   # Named the following sql queries according to their chronological order above, could not come-up with any simple name :(
   sql_1: str = """                                     
              
              CREATE OR REPLACE VIEW NumberOfStudentsInRooms AS
              SELECT DISTINCT room_id AS room,
                    count(student_id) AS students_count
              FROM students
              GROUP BY room
              ORDER BY students_count DESC;
            """
   
   sql_2:str = """
                      CREATE OR REPLACE VIEW RoomsWithSmallestAvgAGe AS
                      SELECT DISTINCT room_id AS room,
                            ROUND(AVG(EXTRACT(YEAR FROM NOW())-(EXTRACT(YEAR FROM birthday))),2) as avg_student_age
                      FROM students
                      GROUP BY room
                      ORDER BY avg_student_age ASC;
                """
   sql_3: str = """
                     CREATE OR REPLACE VIEW RoomsWithTheLargestAgeDiff AS
                      SELECT room_id AS room,
                            MAX(EXTRACT(YEAR FROM NOW())-EXTRACT(YEAR FROM birthday))
							-MIN(EXTRACT(YEAR FROM NOW())-EXTRACT(YEAR FROM birthday))
							AS student_age_diff
                      FROM students
                      GROUP BY room
                      ORDER BY student_age_diff DESC
                """
   sql_4: str = """
                   CREATE OR REPLACE VIEW RoomsWithDiffSexStudents AS
                   WITH cte AS(
                   SELECT room_id as diff_sex_rooms,
                           COUNT(DISTINCT sex)
                   FROM students
                   GROUP BY room_id
                   having COUNT(DISTINCT sex)>1
                     )
                   SELECT diff_sex_rooms from cte;

                  """
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
    
   NumberOfStudentsInRoomsView(conn,cur,sql_1).create_views()
   RoomsWithSmallestAvgAgeView(conn,cur,sql_2).create_views()
   RoomsWithLargestAgeDiffView(conn,cur,sql_3).create_views()
   RoomsWithDiffSexStudentsView(conn,cur,sql_4).create_views()  

   cur.close()
   conn.close()
   logger.info("Views created successfully✅")


if __name__ == "__main__":
   main()
