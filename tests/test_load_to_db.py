import os
import pytest
from pathlib import Path
from src.load_to_db import Rooms,Students,main

@pytest.fixture
def mock_conn(mocker):
    yield mocker.MagicMock()

@pytest.fixture
def mock_cur(mocker, mock_conn):
    mock_cur = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cur
    yield mock_cur

@pytest.fixture
def base_dir():
    # Reproduce your app's BASE_DIR logic
    return Path(__file__).parent.parent  # tests/ -> project root

@pytest.fixture
def mock_rooms(mock_conn, mock_cur, base_dir):
    # EXACT path your class expects
    file_path = base_dir / "data" / "raw_json" / "rooms.json"
    return Rooms(file_path=str(file_path), con=mock_conn, cu=mock_cur)

@pytest.fixture
def mock_students(mock_conn,mock_cur,base_dir):
     # EXACT path your class expects
    file_path = base_dir / "data" / "raw_json" / "students.json"
    return Students(file_path=str(file_path), con=mock_conn, cu=mock_cur)

@pytest.fixture
def mock_logger_rooms(mocker):
    return mocker.patch("src.load_to_db.logger")

@pytest.fixture
def mock_logger_students(mocker):
    return mocker.patch("src.load_to_db.logger")


def test_insertion_into_rooms(mock_cur, mock_rooms, base_dir,mock_conn):
    # Create the directory structure
    raw_json_dir = base_dir / "data" / "raw_json"
    raw_json_dir.mkdir(parents=True, exist_ok=True)

    # Create the JSON file at the EXACT path your class expects
    file_path = raw_json_dir / "rooms.json"
    file_path.write_text("""
    [
        {"id": 1, "name": "Room A"},
        {"id": 2, "name": "Room B"}
    ]
    """)

    try:
        # Call the method with EXACT SAME STRING as self.file_path
        mock_rooms.load_data(str(file_path))

        # Assert DB calls
        assert mock_cur.execute.call_count == 2

        mock_cur.execute.assert_any_call(
            """
                     INSERT INTO rooms(room_id,name)
                     VALUES(%s,%s)
                     ON CONFLICT (room_id) DO UPDATE
                     SET room_id = EXCLUDED.room_id;
                  """,
            (1, "Room A")
        )

        mock_cur.execute.assert_any_call(
            """
                     INSERT INTO rooms(room_id,name)
                     VALUES(%s,%s)
                     ON CONFLICT (room_id) DO UPDATE
                     SET room_id = EXCLUDED.room_id;
                  """,
            (2, "Room B")
        )
        assert mock_conn.commit.call_count == 2

    finally:
        pass

def test_insertion_into_rooms_failure(mock_cur,mock_rooms,base_dir,mock_logger_rooms):
    raw_json_dir = base_dir / "data" / "raw_json"
    raw_json_dir.mkdir(parents=True,exist_ok=True)

    file_path = raw_json_dir / "rooms.json"
    file_path.write_text("""
                         [
                           {"id":1,"name":"Room A"},
                           {"id":2,"name":"Room B"}
                         ]
                         """)
    mock_cur.execute.side_effect = Exception("DB ERROR") # SET self.cu(sql,row) to fail by default.
        
    try:
        mock_rooms.load_data(str(file_path))

        
        mock_logger_rooms.error.assert_called()
    finally:
        pass

def test_fileError_in_Rooms(mock_rooms):
    with pytest.raises(expected_exception=FileNotFoundError):
        mock_rooms.load_data("students.json")
    
def test_insertion_into_students(mock_cur, mock_students, base_dir,mock_conn):
    # Create the directory structure
    raw_json_dir = base_dir / "data" / "raw_json"
    raw_json_dir.mkdir(parents=True, exist_ok=True)

    # Create the JSON file at the EXACT path your class expects
    file_path = raw_json_dir / "students.json"
    file_path.write_text("""
                         [
                           {"id": 1, "name": "Anhelina","room":122,"birthday":"2004-01-27","sex":"F"},
                           {"id": 2, "name": "Daniel","room":232,"birthday":"2003-10-29","sex":"M"}
                         ]
                       """)

    try:
        # Call the method with EXACT SAME STRING as self.file_path
        mock_students.load_data(str(file_path))

        # Assert DB calls
        assert mock_cur.execute.call_count == 2

        mock_cur.execute.assert_any_call(
                  """
                     INSERT INTO students(student_id,name,room_id,birthday,sex)
                     VALUES(%s,%s,%s,%s,%s)
                     ON CONFLICT (student_id) DO UPDATE
                     SET student_id = EXCLUDED.student_id;
                  """,
            (1, "Anhelina",122,"2004-01-27","F")
        )

        mock_cur.execute.assert_any_call(
                 """
                     INSERT INTO students(student_id,name,room_id,birthday,sex)
                     VALUES(%s,%s,%s,%s,%s)
                     ON CONFLICT (student_id) DO UPDATE
                     SET student_id = EXCLUDED.student_id;
                  """,
            (2, "Daniel",232,"2003-10-29","M")
        )
        assert mock_conn.commit.call_count == 2

    finally:
        pass
def test_insertion_into_students_failure(mock_cur,mock_students,base_dir,mock_logger_students):
    raw_json_dir = base_dir / "data" / "raw_json"
    raw_json_dir.mkdir(parents=True,exist_ok=True)

    file_path = raw_json_dir / "students.json"
    file_path.write_text("""
                         [
                           {"id": 1, "name": "Anhelina","room":122,"birthday":"2004-01-27","sex":"F"},
                           {"id": 2, "name": "Daniel","room":232,"birthday":"2003-10-29","sex":"M"}
                         ]
                         """)
    mock_cur.execute.side_effect = Exception("DB ERROR") # SET self.cu(sql,row) to fail by default.
        
    try:
        mock_students.load_data(str(file_path))

        
        mock_logger_students.error.assert_called()
    finally:
        pass

def test_fileError_in_Students(mock_students):
    with pytest.raises(expected_exception=FileNotFoundError):
        mock_students.load_data("rooms.json")




def test_main(mocker):
    # --- Mock input sequence ---
    # 1. username
    # 2. wrong students filename
    # 3. correct students filename
    # 4. wrong rooms filename
    # 5. correct rooms filename
    mocker.patch(
        "src.load_to_db.input",
        side_effect=[
            "Daniel",          # username
            "wrong.json",      # wrong students filename
            "students.json",   # correct students filename
            "bad.json",        # wrong rooms filename
            "rooms.json"       # correct rooms filename
        ]
    )

    # --- Mock print so nothing prints ---
    mocker.patch("src.load_to_db.print")

    # --- Mock logger ---
    mock_logger = mocker.patch("src.load_to_db.logger")

    # --- Mock DB connection ---
    mock_conn = mocker.MagicMock()
    mock_cur = mocker.MagicMock()
    mocker.patch("src.load_to_db.psycopg2.connect", return_value=mock_conn)
    mock_conn.cursor.return_value = mock_cur

    # --- Mock Rooms + Students classes ---
    mock_rooms = mocker.patch("src.load_to_db.Rooms")
    mock_students = mocker.patch("src.load_to_db.Students")

    # --- Run main() ---
    main()

    # --- Assertions ---
    # Username greeting printed
    mock_logger.info.assert_any_call("Starting to insert/update data....🧑‍💻")

    # Rooms loader called correctly
    mock_rooms.assert_called_once()
    mock_rooms.return_value.load_data.assert_called_once()

    # Students loader called correctly
    mock_students.assert_called_once()
    mock_students.return_value.load_data.assert_called_once()

    # Cursor + connection closed
    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()

    
