from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class RadianSecond(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.AngularSpeed
        self._isDefault = True

class RadianMinute(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1/60
        self._unitGroup = UnitGroups.AngularSpeed

class DegreeSecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.0174532925
        self._unitGroup = UnitGroups.AngularSpeed
        
class DegreeMinute(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.0002908882
        self._unitGroup = UnitGroups.AngularSpeed