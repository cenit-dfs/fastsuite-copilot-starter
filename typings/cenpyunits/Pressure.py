from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Pascal(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Pressure
        self._isDefault = True

class Kilopascal(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1000.0
        self._unitGroup = UnitGroups.Pressure

class Megapascal(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1000000.0
        self._unitGroup = UnitGroups.Pressure

class Millipascal(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.Pressure
        
class Bar(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 100000.0
        self._unitGroup = UnitGroups.Pressure
        
class Poundpersquareinch(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 6896.5517
        self._unitGroup = UnitGroups.Pressure
        
class Ouncepersquareinch(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 430.8488
        self._unitGroup = UnitGroups.Pressure