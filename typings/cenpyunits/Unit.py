from cenpyunits.UnitGroups import UnitGroups


class Unit():

    def __init__(self) -> None:
        self._shift = 0.0
        self._scale = 1.0
        self._unitGroup = UnitGroups.Standard
        self._isDefault = False

    def GetShift(self) -> float:
        """ Gets the constant offset to be applied on convertion

        Returns:
            constant shift value as float        
        """ 
        return self._shift
    
    def GetScale(self) -> float:
        """ Gets the scalar factor for conversion.

        Returns:
            returns the scalar as float
        """
        return self._scale

    def GetUnitGroup(self) -> str:
        """ Gets the unit group for this unit
        
        Returns:
            returns the unit group 
        """
        return self._unitGroup
    
    def IsDefault(self) -> bool:
        return self._isDefault