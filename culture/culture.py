from personnage.traits import Trait
from personnage.specialites import Specialite

class BaseCulturelle():
    def __init__(self, name:str, desc:str):
        self._name = name
        self._desc = desc

class GroupeSocial():
    def __init__(self, 
                 name:str, 
                 desc:str, 
                 Traits:list[list[Trait]], 
                 Specialite:list[list[Sp]]):
        self._name = name
        self._desc = desc