import json
import os
import sys
from typing import List, Dict, Any

import psycopg2
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import xml.dom.minidom as md

try:
    from .logs import get_logger # when imported as package
except ImportError:
    from logs import get_logger   # when run directly as script

load_dotenv()
logger = get_logger()


# =========================
# DATABASE LAYER
# =========================

class PostgresClient:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            credentials = {
                "dbname": os.getenv("POSTGRES_DB"),
                "user": os.getenv("POSTGRES_USER"),
                "host": os.getenv("POSTGRES_HOST"),
                "port": os.getenv("POSTGRES_PORT"),
                "password": os.getenv("POSTGRES_PASSWORD"),
            }
            self.conn = psycopg2.connect(**credentials)
            self.cur = self.conn.cursor()
            logger.info("Database connection established.")
        except Exception as e:
            logger.error(f"Database connection failed: {e}", exc_info=True)
            raise

    def fetch_all(self, sql: str) -> List[tuple]:
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            logger.error(f"Query execution failed: {e}", exc_info=True)
            raise

    def close(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logger.info("Database connection closed.")


# =========================
# EXPORT LAYER
# =========================

class DataExporter:

    @staticmethod
    def to_json(data: List[Dict[str, Any]]) -> None:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=4)
        print()

    @staticmethod
    def to_xml(data: List[Dict[str, Any]], root_name: str) -> None:
        root = ET.Element(root_name)

        for row in data:
            item = ET.SubElement(root, "row")
            for key, value in row.items():
                ET.SubElement(item, key).text = str(value)

        xml_bytes = ET.tostring(root, encoding="utf-8")
        pretty = md.parseString(xml_bytes).toprettyxml(indent="    ")
        sys.stdout.write(pretty)
        print()


# =========================
# DATA TRANSFORMATION LAYER
# =========================

class RoomAnalyticsService:

    def __init__(self, db: PostgresClient):
        self.db = db

    def number_of_students(self) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM NumberOfStudentsInRooms"
        rows = self.db.fetch_all(sql)
        return [{"Room": r[0], "StudentCount": r[1]} for r in rows]

    def rooms_with_diff_sex(self) -> List[Dict[str, Any]]:
        sql = "SELECT DISTINCT diff_sex_rooms FROM RoomsWithDiffSexStudents"
        rows = self.db.fetch_all(sql)
        return [{"Room": r[0]} for r in rows]

    def rooms_with_largest_age_diff(self) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM RoomsWithTheLargestAgeDiff LIMIT 5"
        rows = self.db.fetch_all(sql)
        return [{"Room": r[0], "StudentAgeDiff": float(r[1])} for r in rows]

    def rooms_with_smallest_avg_age(self) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM RoomsWithSmallestAvgAge LIMIT 5"
        rows = self.db.fetch_all(sql)
        return [{"Room": r[0], "AvgStudentAge": float(r[1])} for r in rows]


# =========================
# APPLICATION LAYER
# =========================

def main():
    logger = get_logger()
    db = PostgresClient()
    db.connect()

    service = RoomAnalyticsService(db)
    exporter = DataExporter()

    datasets = {
        "1": ("NumberOfStudentsInRooms", service.number_of_students),
        "2": ("RoomsWithDiffSexStudents", service.rooms_with_diff_sex),
        "3": ("RoomsWithLargestAgeDiff", service.rooms_with_largest_age_diff),
        "4": ("RoomsWithSmallestAvgAge", service.rooms_with_smallest_avg_age),
    }

    print("""
Available datasets:
1 - Number of students in each room
2 - Rooms with different sex students
3 - 5 Rooms with largest age difference
4 - 5 Rooms with smallest average age
5 - All datasets
""")

    while True:
        fmt = input("Choose format (json/xml) or type exit: ").lower().strip()
        if fmt == "exit":
            break

        if fmt not in ["json", "xml"]:
            print("Invalid format.")
            continue

        choice = input("Choose dataset number (1-5): ").strip()

        if choice == "5":
            selected = datasets.values()
        elif choice in datasets:
            selected = [datasets[choice]]
        else:
            print("Invalid selection.")
            continue

        for name, func in selected:
            data = func()
            logger.info(f"Fetched {len(data)} rows from {name}")

            if fmt == "json":
                exporter.to_json(data)
            else:
                exporter.to_xml(data, root_name=name)

    db.close()
    logger.info("Application terminated successfully.")


if __name__ == "__main__":
    main()
