import json
import sys
import pytest
from unittest.mock import MagicMock, patch
from io import StringIO

import src.unload_results


# =====================================================
# FIXTURES
# =====================================================

@pytest.fixture
def mock_db():
    db = MagicMock(spec=src.unload_results.PostgresClient)
    return db


@pytest.fixture
def service(mock_db):
    return src.unload_results.RoomAnalyticsService(mock_db)


# =====================================================
# DATABASE LAYER TESTS
# =====================================================

def test_fetch_all_executes_query():
    db = src.unload_results.PostgresClient()
    db.cur = MagicMock()
    db.cur.fetchall.return_value = [("A", 10)]

    result = db.fetch_all("SELECT 1")

    db.cur.execute.assert_called_once_with("SELECT 1")
    assert result == [("A", 10)]


def test_close_closes_resources():
    db = src.unload_results.PostgresClient()
    db.cur = MagicMock()
    db.conn = MagicMock()

    db.close()

    db.cur.close.assert_called_once()
    db.conn.close.assert_called_once()


# =====================================================
# SERVICE LAYER TESTS
# =====================================================

def test_number_of_students(service, mock_db):
    mock_db.fetch_all.return_value = [("Room1", 3)]

    result = service.number_of_students()

    mock_db.fetch_all.assert_called_once()
    assert result == [{"Room": "Room1", "StudentCount": 3}]


def test_rooms_with_diff_sex(service, mock_db):
    mock_db.fetch_all.return_value = [("Room2",)]

    result = service.rooms_with_diff_sex()

    assert result == [{"Room": "Room2"}]


def test_rooms_with_largest_age_diff(service, mock_db):
    mock_db.fetch_all.return_value = [("Room3", 12)]

    result = service.rooms_with_largest_age_diff()

    assert result == [{"Room": "Room3", "StudentAgeDiff": 12.0}]


def test_rooms_with_smallest_avg_age(service, mock_db):
    mock_db.fetch_all.return_value = [("Room4", 18)]

    result = service.rooms_with_smallest_avg_age()

    assert result == [{"Room": "Room4", "AvgStudentAge": 18.0}]


# =====================================================
# EXPORTER TESTS
# =====================================================

def test_to_json_outputs_valid_json(capsys):
    data = [{"Room": "A", "StudentCount": 2}]

    src.unload_results.DataExporter.to_json(data)

    captured = capsys.readouterr()
    parsed = json.loads(captured.out)

    assert parsed == data


def test_to_xml_outputs_valid_xml(capsys):
    data = [{"Room": "A", "StudentCount": 2}]

    src.unload_results.DataExporter.to_xml(data, root_name="TestRoot")

    captured = capsys.readouterr()

    assert "<TestRoot>" in captured.out
    assert "<Room>A</Room>" in captured.out
    assert "<StudentCount>2</StudentCount>" in captured.out


# =====================================================
# MAIN FLOW TEST
# =====================================================

@patch("src.unload_results.PostgresClient")
@patch("src.unload_results.RoomAnalyticsService")
@patch("src.unload_results.DataExporter")
def test_main_flow(mock_exporter_cls, mock_service_cls, mock_db_cls, monkeypatch):
    """
    Tests:
    - user selects json
    - selects dataset 1
    - then exits
    """

    # Mock input sequence
    inputs = iter(["json", "1", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Mock service behavior
    mock_service = mock_service_cls.return_value
    mock_service.number_of_students.return_value = [{"Room": "A", "StudentCount": 2}]

    src.unload_results.main()

    mock_service.number_of_students.assert_called_once()
    mock_exporter_cls.return_value.to_json.assert_called_once()
    mock_db_cls.return_value.close.assert_called_once()