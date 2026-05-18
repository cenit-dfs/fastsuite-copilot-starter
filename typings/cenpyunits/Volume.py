from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Cubicmeter(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Volume
        self._isDefault = True

class Cubicmillimeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.000000001
        self._unitGroup = UnitGroups.Volume

class Cubicinch(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.000016387
        self._unitGroup = UnitGroups.Volume
        
class Cubicfoot(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.028316844
        self._unitGroup = UnitGroups.Volume