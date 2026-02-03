import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path
import load_to_db #import main as LoadToDb
import create_views #import main as CreateViews
import unload_to_json #import main as LoadToJson
load_dotenv()
load_to_db.main()
create_views.main()
unload_to_json.main()
