from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class SquareMeter(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Area
        self._isDefault = True
        
class SquareMillimeter(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.000001
        self._unitGroup = UnitGroups.Area
        
class SquareInch(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.00064516
        self._unitGroup = UnitGroups.Area
        
class SquareFoot(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.09290304
        self._unitGroup = UnitGroups.Area