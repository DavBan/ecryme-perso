import copy
from historique import Action, Validator
class _heap_holder():
    def __init__(self, heap:list=list()):
        self._heap = heap

    def push(self, value):
        self._heap.append(value)
    
    def pop(self):
        return self._heap.pop()
    
    def get_items(self):
        return copy.copy(self._heap)
    
class list_add(Action):
    def __init__(self, handler:_heap_holder, validator:Validator = None):
        super().__init__(handler, validator)
    
    def get_handler(self) -> _heap_holder:
        return self._handler

    def do_action(self, *args, **kwargs):
        nval = 0
        if len(args) == 1:
            if len(kwargs.keys()) > 0 :
                raise TypeError()
            nval = args[0]
        elif len(kwargs) == 1 and "value" in kwargs:
            nval= kwargs["value"]
        else:
            raise TypeError()
        self.get_handler().push(nval)
        super().do_action(*args, **kwargs)
    
    def cancel_action(self):
        self.get_handler().pop()


class existsInHeapValidator(Validator):
    def __init__(self, handler: _heap_holder):
        super().__init__(handler)
    def get_handler(self) -> _heap_holder:
        return self._handler
    def validate(self):
        items = self.get_handler().get_items()[:-1]
        last_val = self.get_handler().get_items()[-1]
        return last_val not in items
        

class Specialite():

        
    def __init__(self, name: str):
        self._name = name
    
    def __eq__(self, value):
        if isinstance(value, str):
            return value == self._name
        elif isinstance(value, Specialite):
            return value.name == self.name
        else:
            return False

    @property
    def name(self):
        return self._name

class ListeDeSpecialite(_heap_holder):
    def __init__(self, heap: list[Specialite] = list()):
        self.push_item = list_add(self, existsInHeapValidator(self))
        super().__init__(heap)