from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Ampere(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.ElectricCurrent
        self._isDefault = True
        
class Milliampere(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.ElectricCurrent