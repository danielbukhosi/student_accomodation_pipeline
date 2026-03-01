import pytest
from unittest.mock import MagicMock, patch

from src import create_views


# =====================================================
# FIXTURE: Mock connection + cursor
# =====================================================

@pytest.fixture
def mock_db():
    conn = MagicMock()
    cur = MagicMock()
    conn.cursor.return_value = cur
    return conn, cur


# =====================================================
# UNIT TEST: Base class behavior
# =====================================================

def test_create_views_executes_and_commits(mock_db):
    conn, cur = mock_db
    sql = "CREATE VIEW test AS SELECT 1"

    view = create_views.CreateViews(conn, cur, sql)
    view.create_views()

    cur.execute.assert_called_once_with(sql)
    conn.commit.assert_called_once()


def test_create_views_logs_error_on_failure(mock_db):
    conn, cur = mock_db
    sql = "BAD SQL"

    cur.execute.side_effect = Exception("boom")

    with patch.object(create_views.logger, "error") as mock_logger:
        view = create_views.CreateViews(conn, cur, sql)
        view.create_views()

        mock_logger.assert_called_once()


# =====================================================
# CHILD CLASSES (inheritance sanity check)
# =====================================================

@pytest.mark.parametrize(
    "cls",
    [
        create_views.NumberOfStudentsInRoomsView,
        create_views.RoomsWithSmallestAvgAgeView,
        create_views.RoomsWithLargestAgeDiffView,
        create_views.RoomsWithDiffSexStudentsView,
    ],
)
def test_child_classes_delegate_to_parent(cls, mock_db):
    conn, cur = mock_db
    sql = "CREATE VIEW test AS SELECT 1"

    instance = cls(conn, cur, sql)
    instance.create_views()

    cur.execute.assert_called_once_with(sql)
    conn.commit.assert_called_once()


# =====================================================
# MAIN FUNCTION TEST
# =====================================================

@patch("src.create_views.psycopg2.connect")
def test_main_success(mock_connect):
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    mock_connect.return_value = mock_conn

    create_views.main()

    # Should execute 4 SQL statements
    assert mock_cur.execute.call_count == 4
    assert mock_conn.commit.call_count == 4

    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("src.create_views.psycopg2.connect", side_effect=Exception("connection error"))
def test_main_connection_failure(mock_connect):
    with patch.object(create_views.logger, "error") as mock_logger:
        create_views.main()
        mock_logger.assert_called_once()