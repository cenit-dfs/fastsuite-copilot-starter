from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Ohm(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.ElectricResist
        self._isDefault = True
        
class Milliohm(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.ElectricResist