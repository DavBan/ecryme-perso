from historique import Action, Validator
from abc import ABC, abstractmethod

class Specialites():
    def __init__(self, name:str):
        pass


class _value_holder():
    def __init__(self, value:int):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, nval:int):
        self._value = nval
        

class _update(_value_holder):
    def __init__(self, value:int):
        super().__init__(value)

    def update(self, update_val:int):
        self._value = self._value + update_val
    



class upgrade(Action):
    def __init__(self, handler:_update, validator:Validator|None):
        super().__init__(handler, validator=validator)
    
    def _get_updater(self) -> _update:
        return self._handler
    
    def do_action(self, *args, **kwargs):
        self._get_updater().update(1)
        super().do_action(*args, **kwargs)
    
    def cancel_action(self):
        self._get_updater().update(-1)

class downgrade(Action):
    def __init__(self, handler:_update, validator:Validator|None):
        super().__init__(handler, validator=validator)
    
    def _get_updater(self) -> _update:
        return self._handler
    
    def do_action(self, *args, **kwargs):
        self._get_updater().update(-1)
        super().do_action(*args, **kwargs)
    
    def cancel_action(self):
        self._get_updater().update(1)

        
class apply_bonus(Action):
    def __init__(self, handler:_update, validator:Validator|None):
        self._bonus_history = []
        super().__init__(handler, validator=validator)
    
    def _get_updater(self) -> _update:
        return self._handler
    
    def do_action(self, *args, **kwargs):
        bonus = 0
        if len(args) == 1:
            if len(kwargs.keys()):
                raise TypeError()
            bonus = args[0]
        elif len(kwargs) == 1 and "bonus" in kwargs:
            bonus= kwargs["bonus"]
        else:
            raise TypeError()
        self._bonus_history.append(bonus)
        self._get_updater().update(bonus)
        super().do_action(*args, **kwargs)
    
    def cancel_action(self):
        bonus = self._bonus_history.pop()
        self._get_updater().update(-bonus)
    
class setter(Action):
    def __init__(self, handler:_value_holder, validator:Validator|None):
        self._value_history = []
        super().__init__(handler, validator=validator)
    
    def _get_value_holder(self) -> _value_holder:
        return self._handler
    
    def do_action(self, *args, **kwargs):
        nval = 0
        if len(args) == 1:
            if len(kwargs.keys()) > 0:
                raise TypeError()
            nval = args[0]
        elif len(kwargs) == 1 and "value" in kwargs:
            nval= kwargs["value"]
        else:
            raise TypeError()
        self._value_history.append(self._get_value_holder().value)
        self._get_value_holder().value = nval
        super().do_action(*args, **kwargs)
    
    def cancel_action(self):
        oldval = self._value_history.pop()
        self._get_value_holder().value = oldval

class IntervalValidator(Validator):
    def __init__(self, handler: _value_holder, min:int, max:int):
        super().__init__(handler)
        self.min = min
        self.max = max
    
    def get_value_holder(self) -> _value_holder:
        return self._handler
    
    def validate(self):
        return self.get_value_holder().value in range(self.min, self.max)

class Score(_update):
    def __init__(self, score:int=0, min:int= 0, max:int=6):
        super().__init__(score)
        self._score=score
        self.score_interval_validator=IntervalValidator(handler=self, min=min, max=max)
        self.upgrade_score=upgrade(self, self.score_interval_validator)
        self.downgrade_score=downgrade(self, self.score_interval_validator)
        self.apply_bonus=apply_bonus(self, self.score_interval_validator)
        self.set_value=setter(self, self.score_interval_validator)

        
