from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Coulomb(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.ElectricCharge
        self._isDefault = True
        
class Kilocoulomb(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1000.0
        self._unitGroup = UnitGroups.ElectricCharge
        
class Millicoulomb(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.ElectricCharge
        
class Statcoulomb(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.000000000333
        self._unitGroup = UnitGroups.ElectricCharge