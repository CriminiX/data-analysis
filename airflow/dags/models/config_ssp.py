from enum import Enum

BUTTON_PREFIX = "ctl00$cphBody${}"

def button(id):
    return BUTTON_PREFIX.format(id)

class CrimeType(Enum):
    CAR_THEFT=button("btnFurtoVeiculo")
    CAR_ROBBERY=button("btnRouboVeiculo")
    
