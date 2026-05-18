from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class MillimeterSecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.Speed

class KilometerHour(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.27777777777778
        self._unitGroup = UnitGroups.Speed

class MeterSecond(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Speed
        self._isDefault = True

class MillimeterMinute(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.00001666666667
        self._unitGroup = UnitGroups.Speed
        
class MeterMinute(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.01666666666667
        self._unitGroup = UnitGroups.Speed
        
class InchSecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.0254
        self._unitGroup = UnitGroups.Speed
        
class FeetSecond(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.3047999902464
        self._unitGroup = UnitGroups.Speed
                
class MileHour(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.44704
        self._unitGroup = UnitGroups.Speed
        
class InchMinute(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.0004233333333
        self._unitGroup = UnitGroups.Speed
        
class FeetMinute(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.00508
        self._unitGroup = UnitGroups.Speed