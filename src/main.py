from load_to_db import main as load_to_db_main
from create_views import main as create_views_main
from unload_results import main as unload_results_main

def main():
    load_to_db_main()
    create_views_main()
    unload_results_main()


if __name__ == "__main__":
  main()
