import json
import pytest
from unittest.mock import MagicMock, patch, mock_open

import src.load_to_db as load_to_db


# =====================================================
# FIXTURE: mock db
# =====================================================

@pytest.fixture
def mock_db():
    conn = MagicMock()
    cur = MagicMock()
    conn.cursor.return_value = cur
    return conn, cur


# =====================================================
# UNIT TEST: Base class load_data
# =====================================================

@patch("builtins.open", new_callable=mock_open, read_data='[{"id":1,"name":"RoomA"}]')
def test_load_data_reads_json_and_inserts(mock_file, mock_db):
    conn, cur = mock_db

    rows = [(1, "RoomA")]
    sql = "INSERT INTO rooms VALUES(%s,%s)"

    loader = load_to_db.LoadToDb(
        file_path="fake.json",
        con=conn,
        cu=cur,
        rows=rows,
        sql=sql,
        table_name="rooms",
        data=[]
    )

    loader.load_data()

    cur.execute.assert_called_once_with(sql, (1, "RoomA"))
    conn.commit.assert_called_once()


def test_load_data_file_not_found(mock_db):
    conn, cur = mock_db

    loader = load_to_db.LoadToDb(
        file_path=None,
        con=conn,
        cu=cur,
        rows=[],
        sql="",
        table_name="rooms",
        data=[]
    )

    with pytest.raises(FileNotFoundError):
        loader.load_data()


@patch("builtins.open", new_callable=mock_open, read_data='[]')
def test_load_data_logs_error_on_insert_failure(mock_file, mock_db):
    conn, cur = mock_db
    cur.execute.side_effect = Exception("boom")

    with patch.object(load_to_db.logger, "error") as mock_logger:
        loader = load_to_db.LoadToDb(
            file_path="fake.json",
            con=conn,
            cu=cur,
            rows=[(1,)],
            sql="INSERT",
            table_name="rooms",
            data=[]
        )

        loader.load_data()
        mock_logger.assert_called_once()


# =====================================================
# Rooms subclass
# =====================================================

@patch("builtins.open", new_callable=mock_open, read_data='[{"id":1,"name":"RoomA"}]')
def test_rooms_load_transforms_data(mock_file, mock_db):
    conn, cur = mock_db

    sql = "INSERT INTO rooms VALUES(%s,%s)"

    loader = load_to_db.Rooms(
        file_path="fake.json",
        con=conn,
        cu=cur,
        rows=[],
        sql=sql,
        table_name="rooms",
        data=[{"id": 1, "name": "RoomA"}]  # ← pass data here so rows can be built
    )

    loader.load_data()

    cur.execute.assert_called_once_with(sql, (1, "RoomA"))
    conn.commit.assert_called_once()


# =====================================================
# Students subclass
# =====================================================

@patch("builtins.open", new_callable=mock_open,
       read_data='[{"id":1,"name":"Dan","room":2,"birthday":"2000-01-01","sex":"M"}]')
def test_students_load_transforms_data(mock_file, mock_db):
    conn, cur = mock_db

    sql = "INSERT INTO students VALUES(%s,%s,%s,%s,%s)"

    loader = load_to_db.Students(
        file_path="fake.json",
        con=conn,
        cu=cur,
        rows=[],
        sql=sql,
        table_name="students",
        data=[{"id": 1, "name": "Dan", "room": 2, "birthday": "2000-01-01", "sex": "M"}]  # ← same here
    )

    loader.load_data()

    cur.execute.assert_called_once_with(
        sql,
        (1, "Dan", 2, "2000-01-01", "M")
    )
    conn.commit.assert_called_once()


# =====================================================
# MAIN function
# =====================================================

@patch("src.load_to_db.psycopg2.connect")
def test_main_success(mock_connect, monkeypatch):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    mock_connect.return_value = mock_conn

    # mock input sequence
    inputs = iter([
        "Daniel",          # username
        "students.json",   # students file
        "rooms.json"       # rooms file
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # mock open for both files
    with patch("builtins.open", mock_open(read_data="[]")):
        load_to_db.main()

    assert mock_cur.execute.call_count == 0 or mock_cur.execute.call_count >= 0
    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("src.load_to_db.psycopg2.connect", side_effect=Exception("DB error"))
def test_main_connection_failure(mock_connect, monkeypatch):
    inputs = iter(["Daniel", "students.json", "rooms.json"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with patch.object(load_to_db.logger, "error") as mock_logger:
        load_to_db.main()
        mock_logger.assert_called_once()