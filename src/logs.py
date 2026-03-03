import logging
import sys

def get_logger():
  logger = logging.getLogger("__main__")
  handler = logging.StreamHandler(sys.stdout)
  formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)
  return logger



def main():
  logger = get_logger()

if __name__ == "__main__":
  main()