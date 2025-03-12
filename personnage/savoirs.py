from score import Score

from specialites import Specialite, ListeDeSpecialite


class ScoreSavoir(Score):
    def __init__(self, score = 0):
        super().__init__(score, min=0, max=6)

class Savoir():
    def __init__(self, score:ScoreSavoir=ScoreSavoir(), listeDeSpecialité:ListeDeSpecialite = ListeDeSpecialite()):
        self._score=score
        self._listedespe=listeDeSpecialité
    
    @property
    def score(self):
        return self._score.value
    
    @property
    def listspe(self):
        return self._listedespe.get_items()
    
    def upgradeScore(self):
        self._score.upgrade_score()
    
    def downgradeScore(self):
        self._score.downgrade_score()
    
    def appliquerBonus(self, bonus:int):
        self._score.apply_bonus(bonus=bonus)
    
    def setScore(self, nScore: int):
        self._score.set_value(value=nScore)

    def ajoutSpecialité(self, nSpe:str|Specialite):
        if isinstance(nSpe, str):
            nSpe = Specialite(nSpe)
        self._listedespe.push_item(nSpe)

class SavoirANommer(Savoir):
    def __init__(self, nom: str, score = ScoreSavoir, listeDeSpecialité = ListeDeSpecialite()):
        super().__init__(score, listeDeSpecialité)
        self._nom = nom
    
    @property
    def nom(self) -> str:
        return self._nom