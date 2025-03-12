from score import Score

class ScoreTrait(Score):
    def __init__(self, score = 0):
        super().__init__(score, min=-3, max=3)

class Trait():
    def __init__(self, nom: str, score:ScoreTrait=ScoreTrait()):
        self._nom = nom
        self._score = score

    @property
    def nom(self) -> str:
        return self._nom
    
    @property
    def score(self)-> int:
        return self._score.value
    
    def upgradeScore(self):
        self._score.upgrade_score()
    
    def downgradeScore(self)
        self._score.downgrade_score()
