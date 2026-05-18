from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Millisecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.Time

class Second(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Time
        self._isDefault = True

class Minute(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 60.0
        self._unitGroup = UnitGroups.Time
        
class Hour(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 3600.0
        self._unitGroup = UnitGroups.Time

class Day(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 86400.0
        self._unitGroup = UnitGroups.Time