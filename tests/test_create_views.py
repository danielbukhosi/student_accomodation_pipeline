import pytest
from src.create_views import NumberOfStudentsInRoomsView,RoomsWithDiffSexStudentsView,RoomsWithLargestAgeDiffView,RoomsWithSmallestAvgAgeView,main

@pytest.fixture
def mock_conn(mocker):
    yield mocker.MagicMock()

@pytest.fixture
def mock_cur(mocker, mock_conn):
    mock_cur = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cur
    yield mock_cur

@pytest.fixture
def mock_NumberOfStudentsInRoomsView(mock_conn,mock_cur):
    return NumberOfStudentsInRoomsView(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_RoomsWithDiffSexStudentsView(mock_conn,mock_cur):
    return RoomsWithDiffSexStudentsView(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_RoomsWithLargestAgeDiffView(mock_conn,mock_cur):
    return RoomsWithLargestAgeDiffView(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_RoomsWithSmallestAvgAgeView(mock_conn,mock_cur):
    return RoomsWithSmallestAvgAgeView(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("src.create_views.logger")

def test_NumberOfStudentsInRoomsView(mock_conn,mock_cur,mock_NumberOfStudentsInRoomsView):
    mock_NumberOfStudentsInRoomsView.create_views()
    assert mock_cur.execute.call_count == 1

    mock_cur.execute.assert_called_once_with(
                                                 """
              
              CREATE OR REPLACE VIEW NumberOfStudentsInRooms AS
              SELECT DISTINCT room_id AS room,
                    count(student_id) AS students_count
              FROM students
              GROUP BY room
              ORDER BY students_count DESC;
            """
                                   )
    mock_conn.commit.assert_called_once()
    
def test_NumberOfStudentsInRoomsView_failure(mock_NumberOfStudentsInRoomsView,mock_cur,mock_conn,mock_logger):
    mock_cur.execute.side_effect=Exception("Db Error")
    
    mock_NumberOfStudentsInRoomsView.create_views()
    mock_logger.error.assert_called_once()
    mock_conn.commit.assert_not_called()
    
def test_RoomsWithDiffSexStudentsView(mock_conn,mock_cur,mock_RoomsWithDiffSexStudentsView):
    mock_RoomsWithDiffSexStudentsView.create_views()
    assert mock_cur.execute.call_count == 1

    mock_cur.execute.assert_called_once_with(
                                                 """
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
                                   )
    mock_conn.commit.assert_called_once()
    
def test_RoomsWithDiffSexStudentsView_failure(mock_RoomsWithDiffSexStudentsView,mock_cur,mock_conn,mock_logger):
    mock_cur.execute.side_effect=Exception("Db Error")
    
    mock_RoomsWithDiffSexStudentsView.create_views()
    mock_logger.error.assert_called_once()
    mock_conn.commit.assert_not_called()
    
def test_RoomsWithLargestAgeDiffView(mock_conn,mock_cur,mock_RoomsWithLargestAgeDiffView):
    mock_RoomsWithLargestAgeDiffView.create_views()
    assert mock_cur.execute.call_count == 1

    mock_cur.execute.assert_called_once_with(
                                              """
                      CREATE OR REPLACE VIEW RoomsWithTheLargestAgeDiff AS
                      SELECT DISTINCT room_id AS room,
                            ROUND(STDDEV_POP(2026-EXTRACT(YEAR FROM birthday)),2) AS student_age_diff
                      FROM students
                      GROUP BY room
                      ORDER BY student_age_diff DESC
                  """
                         
                                   )
    mock_conn.commit.assert_called_once()
    
def test_RoomsWithLargestAgeDiffView_failure(mock_RoomsWithLargestAgeDiffView,mock_cur,mock_conn,mock_logger):
    mock_cur.execute.side_effect=Exception("Db Error")
    
    mock_RoomsWithLargestAgeDiffView.create_views()
    mock_logger.error.assert_called_once()
    mock_conn.commit.assert_not_called()
    
def test_RoomsWithSmallestAvgAgeView(mock_conn,mock_cur,mock_RoomsWithSmallestAvgAgeView):
    mock_RoomsWithSmallestAvgAgeView.create_views()
    assert mock_cur.execute.call_count == 1

    mock_cur.execute.assert_called_once_with(
                                                 """
                      CREATE OR REPLACE VIEW RoomsWithSmallestAvgAGe AS
                      SELECT DISTINCT room_id AS room,
                            ROUND(AVG(2026-(EXTRACT(YEAR FROM birthday))),2) as avg_student_age
                      FROM students
                      GROUP BY room
                      ORDER BY avg_student_age ASC;
                """
                         
                                   )
    mock_conn.commit.assert_called_once()
    
def test_RoomsWithSmallestAvgAgeView_failure(mock_RoomsWithSmallestAvgAgeView,mock_cur,mock_conn,mock_logger):
    mock_cur.execute.side_effect=Exception("Db Error")
    
    mock_RoomsWithSmallestAvgAgeView.create_views()
    mock_logger.error.assert_called_once()
    mock_conn.commit.assert_not_called()


import pytest
from src.create_views import main


def test_main_creates_all_views(mocker):
    # --- Mock DB connection ---
    mock_conn = mocker.MagicMock()
    mock_cur = mocker.MagicMock()
    mocker.patch("src.create_views.psycopg2.connect", return_value=mock_conn)
    mock_conn.cursor.return_value = mock_cur

    # --- Mock logger ---
    mock_logger = mocker.patch("src.create_views.logger")

    # --- Mock all view classes ---
    mock_v1 = mocker.patch("src.create_views.NumberOfStudentsInRoomsView")
    mock_v2 = mocker.patch("src.create_views.RoomsWithSmallestAvgAgeView")
    mock_v3 = mocker.patch("src.create_views.RoomsWithLargestAgeDiffView")
    mock_v4 = mocker.patch("src.create_views.RoomsWithDiffSexStudentsView")

    # --- Run main() ---
    main()

    # --- Assertions: each view class instantiated correctly ---
    mock_v1.assert_called_once_with(mock_conn, mock_cur)
    mock_v2.assert_called_once_with(mock_conn, mock_cur)
    mock_v3.assert_called_once_with(mock_conn, mock_cur)
    mock_v4.assert_called_once_with(mock_conn, mock_cur)

    # --- Assertions: each .create_views() called ---
    mock_v1.return_value.create_views.assert_called_once()
    mock_v2.return_value.create_views.assert_called_once()
    mock_v3.return_value.create_views.assert_called_once()
    mock_v4.return_value.create_views.assert_called_once()

    # --- Cleanup ---
    mock_cur.close.assert_called_once()
    mock_conn.close.assert_called_once()

    # --- Logging ---
    mock_logger.info.assert_any_call("Views created successfully✅")


def test_main_connection_failure(mocker):
    # --- Mock logger ---
    mock_logger = mocker.patch("src.create_views.logger")

    # --- Force DB connection failure ---
    mocker.patch("src.create_views.psycopg2.connect", side_effect=Exception("DB DOWN"))

    # --- Run main() ---
    main()

    # --- Assert error logged ---
    mock_logger.error.assert_called()

    # --- Ensure no view classes were called ---
    assert not mocker.patch("src.create_views.NumberOfStudentsInRoomsView").called




