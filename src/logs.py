import logging
import sys

def load_to_db_log():
  logger = logging.getLogger("LoadToDb")
  handler = logging.StreamHandler(sys.stdout)
  formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)
  return logger

def create_views_log():
  logger =  logging.getLogger("CreateViews")
  handler = logging.StreamHandler(sys.stdout)
  formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)
  return logger

def unload_results_log():
  logger = logging.getLogger("UnloadToDb")
  handler = logging.StreamHandler(sys.stdout)
  formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)
  return logger

def main():
  logger_1 = load_to_db_log()
  logger_2 = create_views_log()
  logger_3 = unload_results_log()

if __name__ == "__main__":
  main()