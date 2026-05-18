class Point3D():
    """
        Simple point in 3D space used to inforce correct position input on Matrix
    """

    def __init__(self, xyz : tuple = None) -> None:
        """ Constructor

            If the input postion is None, a point at 0.0, 0.0, 0.0 will be created.
            If an input is given, it must be a tuple of float with exactly 3 items
        
        """
        if xyz is None or len(xyz) != 3:
            xyz = (0.0, 0.0, 0.0)
        self.SetXYZ(xyz)

    def GetX(self) -> float:
        """ Gets the X-coordinate

        Returns:
            returns X-coordinate as float
        
        """
        return self._x

    def GetY(self) -> float:
        """ Gets the Y-coordinate

        Returns:
            returns Y-coordinate as float
        
        """
        return self._y
    
    def GetZ(self) -> float:
        """ Gets the Z-coordinate

        Returns:
            returns Z-coordinate as float
        
        """
        return self._z

    def GetXYZ(self) -> tuple:
        """ Gets the point coordinates as tuple of float
        
        Returns:
            returns x, y, z as tuple of float
        """
        return (self._x, self._y, self._z)
    
    def SetXYZ(self, xyz : tuple) -> None:
        """ Sets the point coordinates

        Args:
            xyz: tuple containing the new coordinates in order x, y, z

        Raises:
            TypeError: raised when input is not a tuple of float
            IndexError: raise when length of xyz is not 3
        
        """
        if (not isinstance(xyz, tuple)):
            raise TypeError("Expected tuple")
        
        if len(xyz) != 3:
            raise IndexError("Tuple length must be 3!")
        
        if (not isinstance(xyz[0], float)) or (not isinstance(xyz[1], float)) or (not isinstance(xyz[2], float)):
            raise TypeError("Expected tuple of float")
        
        self._x = xyz[0]
        self._y = xyz[1]
        self._z = xyz[2]
