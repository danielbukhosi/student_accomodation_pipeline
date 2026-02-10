import pytest
from src.unload_results import NumberOfStudentsInRoomsJ,RoomsWithDiffSexStudentsJ,RoomsWithLargestAgeDiffJ,RoomsWithSmallestAvgAgeJ
from src.unload_results import NumberOfStudentsInRoomsX,RoomsWithDiffSexStudentsX,RoomsWithLargestAgeDiffX,RoomsWithSmallestAvgAgeX
from src.unload_results import main

@pytest.fixture
def mock_conn(mocker):
    yield mocker.MagicMock()

@pytest.fixture
def mock_cur(mocker, mock_conn):
    mock_cur = mocker.MagicMock()
    mock_conn.cursor.return_value = mock_cur
    yield mock_cur

@pytest.fixture
def mock_NumberOfStudentsInRoomsJ(mock_conn,mock_cur):
    return NumberOfStudentsInRoomsJ(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_RoomsWithDiffSexStudentsJ(mock_conn,mock_cur):
    return RoomsWithDiffSexStudentsJ(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_RoomsWithLargestAgeDiffJ(mock_conn,mock_cur):
    return RoomsWithLargestAgeDiffJ(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_RoomsWithSmallestAvgAgeJ(mock_conn,mock_cur):
    return RoomsWithSmallestAvgAgeJ(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_NumberOfStudentsInRoomsX(mock_conn,mock_cur):
    return NumberOfStudentsInRoomsX(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_RoomsWithDiffSexStudentsX(mock_conn,mock_cur):
    return RoomsWithDiffSexStudentsX(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_RoomsWithLargestAgeDiffX(mock_conn,mock_cur):
    return RoomsWithLargestAgeDiffX(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_RoomsWithSmallestAvgAgeX(mock_conn,mock_cur):
    return RoomsWithSmallestAvgAgeX(con=mock_conn,cu=mock_cur)

@pytest.fixture
def mock_logger(mocker):
    return mocker.patch("src.unload_results.logger")

@pytest.fixture
def mock_json(mocker):
    return mocker.patch("src.unload_results.json")

@pytest.fixture
def mock_sys(mocker):
    return mocker.patch("src.unload_results.sys")

@pytest.fixture
def mock_db(mocker):
    mock_conn = mocker.MagicMock()
    mock_cur = mocker.MagicMock()
    mocker.patch("src.unload_results.psycopg2.connect", return_value=mock_conn)
    mock_conn.cursor.return_value = mock_cur
    return mock_conn, mock_cur

def test_NumberOfStudentsInRoomsJ(mock_conn,mock_cur,mock_NumberOfStudentsInRoomsJ,mock_logger,mock_json):
    mock_NumberOfStudentsInRoomsJ.unload_to_json()
    mock_cur.execute.assert_called_once_with(
        
                                                 """
            SELECT * FROM NumberOfStudentsInRooms

          """
    )
    mock_conn.commit.assert_called_once()
    mock_json.dump.assert_called_once()
    mock_logger.info.assert_called_once()
    mock_logger.error.assert_not_called()

def test_NumberOfStudentsInRoomsJ_failure(mock_conn,mock_cur,mock_NumberOfStudentsInRoomsJ,mock_logger,mock_json):
    mock_cur.execute.side_effect = Exception("DB ERROR")    # FORCING AN ERROR
    mock_json.dump.side_effect = Exception("Type Error")    # FORCING AN ERROR
    mock_NumberOfStudentsInRoomsJ.unload_to_json()
    mock_conn.commit.assert_not_called()
    mock_logger.info.assert_not_called()
    assert mock_logger.error.call_count == 2

def test_RoomsWithLargestAgeDiffJ(mock_conn,mock_cur,mock_RoomsWithLargestAgeDiffJ,mock_logger,mock_json):
    mock_RoomsWithLargestAgeDiffJ.unload_to_json()
    mock_cur.execute.assert_called_once_with(
        
                                               """
            SELECT * FROM RoomsWithTheLargestAgeDiff
            LIMIT 5

          """
    )
    mock_conn.commit.assert_called_once()
    mock_json.dump.assert_called_once()
    mock_logger.info.assert_called_once()
    mock_logger.error.assert_not_called()

def test_RoomsWithLargestAgeDiffJ_failure(mock_conn,mock_cur,mock_RoomsWithLargestAgeDiffJ,mock_logger,mock_json):
    mock_cur.execute.side_effect = Exception("DB ERROR")    # FORCING AN ERROR
    mock_json.dump.side_effect = Exception("Type Error")    # FORCING AN ERROR
    mock_RoomsWithLargestAgeDiffJ.unload_to_json()
    mock_conn.commit.assert_not_called()
    mock_logger.info.assert_not_called()
    assert mock_logger.error.call_count == 2

def test_RoomsWithDiffSexStudentsJ(mock_conn,mock_cur,mock_RoomsWithDiffSexStudentsJ,mock_logger,mock_json):
    mock_RoomsWithDiffSexStudentsJ.unload_to_json()
    mock_cur.execute.assert_called_once_with(
        
                                  """
            SELECT DISTINCT diff_sex_rooms FROM RoomsWithDiffSexStudents

          """
    )
    mock_conn.commit.assert_called_once()
    mock_json.dump.assert_called_once()
    mock_logger.info.assert_called_once()
    mock_logger.error.assert_not_called()

def test_RoomsWithDiffSexStudentsJ_failure(mock_conn,mock_cur,mock_RoomsWithDiffSexStudentsJ,mock_logger,mock_json):
    mock_cur.execute.side_effect = Exception("DB ERROR")    # FORCING AN ERROR
    mock_json.dump.side_effect = Exception("Type Error")    # FORCING AN ERROR
    mock_RoomsWithDiffSexStudentsJ.unload_to_json()
    mock_conn.commit.assert_not_called()
    mock_logger.info.assert_not_called()
    assert mock_logger.error.call_count == 2

def test_RoomsWithSmallestAvgAgeJ(mock_conn,mock_cur,mock_RoomsWithSmallestAvgAgeJ,mock_logger,mock_json):
    mock_RoomsWithSmallestAvgAgeJ.unload_to_json()
    mock_cur.execute.assert_called_once_with(
        
            """
            SELECT * FROM RoomsWithSmallestAvgAge
            LIMIT 5

          """
    )
    mock_conn.commit.assert_called_once()
    mock_json.dump.assert_called_once()
    mock_logger.info.assert_called_once()
    mock_logger.error.assert_not_called()

def test_RoomsWithSmallestAvgAgeJ_failure(mock_conn,mock_cur,mock_RoomsWithSmallestAvgAgeJ,mock_logger,mock_json):
    mock_cur.execute.side_effect = Exception("DB ERROR")    # FORCING AN ERROR
    mock_json.dump.side_effect = Exception("Type Error")    # FORCING AN ERROR
    mock_RoomsWithSmallestAvgAgeJ.unload_to_json()
    mock_conn.commit.assert_not_called()
    mock_logger.info.assert_not_called()
    assert mock_logger.error.call_count == 2

def test_NumberOfStudentsInRoomsX(mock_conn,mock_cur,mock_NumberOfStudentsInRoomsX,mock_logger,mock_sys):
    mock_NumberOfStudentsInRoomsX.unload_to_xml()
    mock_cur.execute.assert_called_once_with(
        
             """
            SELECT * FROM NumberOfStudentsInRooms
          """
    )
    mock_conn.commit.assert_called_once()
    mock_sys.stdout.write.assert_called_once()
    mock_logger.info.assert_called_once()
    mock_logger.error.assert_not_called()

def test_NumberOfStudentsInRoomsX_failure(mock_conn,mock_cur,mock_NumberOfStudentsInRoomsX,mock_logger,mock_sys):
    mock_cur.execute.side_effect = Exception("DB ERROR")    # FORCING AN ERROR
    mock_sys.stdout.write.side_effect = Exception("Type Error")    # FORCING AN ERROR
    mock_NumberOfStudentsInRoomsX.unload_to_xml()
    mock_conn.commit.assert_not_called()
    mock_logger.info.assert_not_called()
    assert mock_logger.error.call_count == 2

def test_RoomWithLargestAgeDiffsX(mock_conn,mock_cur,mock_RoomsWithLargestAgeDiffX,mock_logger,mock_sys):
    mock_RoomsWithLargestAgeDiffX.unload_to_xml()
    mock_cur.execute.assert_called_once_with(
                                                """
            SELECT * FROM RoomsWithTheLargestAgeDiff
            LIMIT 5
           """
    )
    mock_conn.commit.assert_called_once()
    mock_sys.stdout.write.assert_called_once()
    mock_logger.info.assert_called_once()
    mock_logger.error.assert_not_called()

def test_RoomsWithLargestAgeDiffX_failure(mock_conn,mock_cur,mock_RoomsWithLargestAgeDiffX,mock_logger,mock_sys):
    mock_cur.execute.side_effect = Exception("DB ERROR")    # FORCING AN ERROR
    mock_sys.stdout.write.side_effect = Exception("Type Error")    # FORCING AN ERROR
    mock_RoomsWithLargestAgeDiffX.unload_to_xml()
    mock_conn.commit.assert_not_called()
    mock_logger.info.assert_not_called()
    assert mock_logger.error.call_count == 2


def test_RoomWithDiffSexStudentsX(mock_conn,mock_cur,mock_RoomsWithDiffSexStudentsX,mock_logger,mock_sys):
    mock_RoomsWithDiffSexStudentsX.unload_to_xml()
    mock_cur.execute.assert_called_once_with(
                                                   """
            SELECT DISTINCT diff_sex_rooms FROM RoomsWithDiffSexStudents
           """
    )
    mock_conn.commit.assert_called_once()
    mock_sys.stdout.write.assert_called_once()
    mock_logger.info.assert_called_once()
    mock_logger.error.assert_not_called()

def test_RoomsWithDiffSexStudentsX_failure(mock_conn,mock_cur,mock_RoomsWithDiffSexStudentsX,mock_logger,mock_sys):
    mock_cur.execute.side_effect = Exception("DB ERROR")    # FORCING AN ERROR
    mock_sys.stdout.write.side_effect = Exception("Type Error")    # FORCING AN ERROR
    mock_RoomsWithDiffSexStudentsX.unload_to_xml()
    mock_conn.commit.assert_not_called()
    mock_logger.info.assert_not_called()
    assert mock_logger.error.call_count == 2

def test_RoomWithSmallestAvgAgeX(mock_conn,mock_cur,mock_RoomsWithSmallestAvgAgeX,mock_logger,mock_sys):
    mock_RoomsWithSmallestAvgAgeX.unload_to_xml()
    mock_cur.execute.assert_called_once_with(
                                                """
            SELECT * FROM RoomsWithSmallestAvgAge
            LIMIT 5
           """
    )
    mock_conn.commit.assert_called_once()
    mock_sys.stdout.write.assert_called_once()
    mock_logger.info.assert_called_once()
    mock_logger.error.assert_not_called()

def test_RoomsWithSmallestAvgAgeX_failure(mock_conn,mock_cur,mock_RoomsWithSmallestAvgAgeX,mock_logger,mock_sys):
    mock_cur.execute.side_effect = Exception("DB ERROR")    # FORCING AN ERROR
    mock_sys.stdout.write.side_effect = Exception("Type Error")    # FORCING AN ERROR
    mock_RoomsWithSmallestAvgAgeX.unload_to_xml()
    mock_conn.commit.assert_not_called()
    mock_logger.info.assert_not_called()
    assert mock_logger.error.call_count == 2

# ---------------------------------------------------------
# Test 1: JSON mode, dataset 1 selected
# ---------------------------------------------------------
def test_main_json_dataset_1(mocker, mock_db):
    mock_conn, mock_cur = mock_db

    # Mock dataset class
    mock_num = mocker.patch("src.unload_results.NumberOfStudentsInRoomsJ")

    # Silence print()
    mocker.patch("src.unload_results.print")

    # Provide enough inputs to avoid StopIteration
    mocker.patch(
        "src.unload_results.input",
        side_effect=[
            "json",   # choose JSON mode
            "1",      # dataset 1
            "x",      # dataset 2
            "x",      # dataset 3
            "x",      # dataset 4
            "x",      # all datasets
            "exit",   # exit loop
            "exit"    # extra exit for safety
        ]
    )

    main()

    # Assert dataset 1 JSON class was used
    mock_num.assert_called_once_with(mock_conn, mock_cur)
    mock_num.return_value.unload_to_json.assert_called_once()


# ---------------------------------------------------------
# Test 2: XML mode, dataset 2 selected
# ---------------------------------------------------------
def test_main_xml_dataset_2(mocker, mock_db):
    mock_conn, mock_cur = mock_db

    mock_diffsexX = mocker.patch("src.unload_results.RoomsWithDiffSexStudentsX")
    mocker.patch("src.unload_results.print")

    mocker.patch(
        "src.unload_results.input",
        side_effect=[
            # LOOP 1
            "x",       # JSON prompt → skip JSON
            "xml",     # XML prompt → enter XML mode
            "x",       # dataset 1
            "2",       # dataset 2
            "x",       # dataset 3
            "x",       # dataset 4

            # LOOP 2 (clean exit)
            "exit",    # Xml prompt
            "exit"  
                 # exit prompt
        ]
    )

    main()

    mock_diffsexX.assert_called_once_with(mock_conn, mock_cur)
    mock_diffsexX.return_value.unload_to_xml.assert_called_once()


# ---------------------------------------------------------
# Test 3: DB connection failure logs an error
# ---------------------------------------------------------
def test_main_connection_failure(mocker):
    mock_logger = mocker.patch("src.unload_results.logger")

    # Force connection failure
    mocker.patch("src.unload_results.psycopg2.connect", side_effect=Exception("DB DOWN"))

    # Ensure loop exits immediately
    mocker.patch("src.unload_results.input", return_value="exit")

    main()

    mock_logger.error.assert_called()


# ---------------------------------------------------------
# Test 4: Immediate exit (no datasets called)
# ---------------------------------------------------------
def test_main_exit_immediately(mocker, mock_db):
    mock_conn, mock_cur = mock_db

    mocker.patch("src.unload_results.print")
    mocker.patch("src.unload_results.input", return_value="exit")

    main()

    # Cursor created once, no dataset classes called
    mock_conn.cursor.assert_called_once()

  