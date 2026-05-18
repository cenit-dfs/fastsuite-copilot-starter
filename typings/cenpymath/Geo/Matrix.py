from . import Point3D
from cenpymath.Euler.Notations import Notations

class Matrix():
    """ Class defining a simple 4x4 matrix where x,y,z is stored in the last colomn:
            a1  b1  c1  x
            a2  b2  c2  y
            a3  b3  c3  z
            0.0 0.0 0.0 1.0
    
    """

    def __init__(self, array: list = None) -> None:
        """ Constructor
        
            This will create a unit matrix
        """
        if array is None:
            self._array = [ 1.0, 0.0, 0.0, 0.0, \
                            0.0, 1.0, 0.0, 0.0, \
                            0.0, 0.0, 1.0, 0.0, \
                            0.0, 0.0, 0.0, 1.0 ]
        else:
            self.SetArray(array)

    def GetPosition(self) -> Point3D.Point3D:
        """ Gets the position part of the matrix
        
        Returns:
            returns position as Point3D
        """
        return Point3D.Point3D((self._array[3], self._array[7], self._array[11]))

    def GetOrientation(self) -> tuple:
        """ Gets the Rotation angles as Euler angles in notation XYZs
        
        Returns:
            rotation angles as tuple with (rotX, rotY, rotZ)
        """
        import cenpymath
        converter = cenpymath.Converter.Converter()
        result = converter.ConvertMatrixToEuler(self, Notations.Euler_XYZs)
        return tuple(result)

    def SetArray(self, array : list) -> None:
        """ Sets the matrix array. The array most be provided as:
            a1  b1  c1  x
            a2  b2  c2  y
            a3  b3  c3  z
            0.0 0.0 0.0 1.0
        
        Args:
            array: new array to set (length must be 16)
        
        """
        if len(array) != 16:
            return
        
        self._array = array

    def GetArray(self) -> list:
        """ Gets the array of this 4x4 matrix

        Returns:
            returns the array as list of float
        
        """
        return self._array

    def SetPosition(self, xyz : Point3D.Point3D) -> None:
        """ Sets the position for this matrix

        Args:
            xyz: new matrix position        
        """   
        self._array[3] = xyz.GetX()
        self._array[7] = xyz.GetY()
        self._array[11] = xyz.GetZ()

    def SetOrientation(self, rpy : tuple) -> None:
        """ Sets the orientation for this matrix. Values given as 
            roll, pitch, yaw (rotX, rotY, rotZ)

        Args:
            rpy: new matrix orientation in roll, pitch, yaw
        
        """

        if len(rpy) != 3:
            return
        import cenpymath
        converter = cenpymath.Converter.Converter()
        matrix = converter.GetMatrixFromEuler(rpy[2], rpy[1], rpy[0], self._array[3], self._array[7], self._array[11])

        self.SetArray(matrix.GetArray())

    