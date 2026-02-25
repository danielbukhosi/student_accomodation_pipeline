import load_to_db #import main as LoadToDb
import create_views #import main as CreateViews
import unload_results #import main as LoadToJson

def main():
  load_to_db.main()
  create_views.main()
  unload_results.main()

if __name__ == "__main__":
  main()
