from cenpyunits.Unit import Unit
from cenpyunits.UnitGroups import UnitGroups

class Milligram(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.000001
        self._unitGroup = UnitGroups.Mass

class Gram(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.001
        self._unitGroup = UnitGroups.Mass

class Kilogram(Unit):

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1
        self._unitGroup = UnitGroups.Mass
        self._isDefault = True
        
class Tonne(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 1000.0
        self._unitGroup = UnitGroups.Mass

class Ounce(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.0283495231
        self._unitGroup = UnitGroups.Mass

class Pound(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 0.45359237
        self._unitGroup = UnitGroups.Mass
        
class Slug(Unit):

    def __init__(self) -> None:
        super().__init__()
        self._shift = 0.0
        self._scale = 14.5939029
        self._unitGroup = UnitGroups.Mass
