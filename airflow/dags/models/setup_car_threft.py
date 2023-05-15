import logging
from models.config_ssp import CrimeType
import models.extract_file as extract_file
from datetime import date

def start_setup_car_threft():
   logging.basicConfig(level=logging.DEBUG)
   extract_file(date(2005, 5, 5), crime_type=CrimeType.CAR_THEFT)