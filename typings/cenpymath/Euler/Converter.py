import math
from cenpymath.Euler.Notations import Notations
from cenpymath.Geo.Matrix import Matrix

class Converter():

### public Methods

   def GetMatrixFromEuler(self, rotZ : float, rotY : float, rotX : float, x : float, y : float, z : float) -> Matrix:
      """ Generates a cenpymath>Matrix from the given Euler angles and position

      Args:
         rotZ: rotation around Z-axis
         rotY: rotation around Y-axis
         rotX: rotation around X-axis
         X: X-coordinate
         Y: Y-coordinate
         Z: Z-coordinate
      
      Returns:
         returns resulting matrix
      """
      matrixArray = self._getMatrixArrayFromEuler((rotX, rotY, rotZ), Notations.Euler_XYZs)
      matrixArray[3] = x
      matrixArray[7] = y
      matrixArray[11] = z
      return Matrix(matrixArray)

   def ConvertEuler(self, rotX : float, rotY : float, rotZ : float, notationTo : Notations, notationFrom : Notations) -> list:
      """ Converts Euler angle from notationFrom to notationTo

      Args:
         rotX: rotation around X-axis
         rotY: rotation around Y-axis
         rotZ: rotation around Z-axis
         notationTo: target notation
         notationFrom: source notation

      Returns:
         returns a tuple with the converted angles in order rotX, rotY, rotZ      
      """
      # convert Euler-angles in "from" notation to matrix 4x4
      matrix = self._getMatrixArrayFromEuler((rotX, rotY, rotZ), self._getEulerOrderNotation(notationFrom))

      #  Convert matrix to Euler-angles in "to" notation
      eulerAngles = self._getEulerFromMatrix(matrix, self._getEulerOrderNotation(notationTo))
      # result in degree
      return [round(math.degrees(eulerAngles[0]), 6), round(math.degrees(eulerAngles[1]), 6), round(math.degrees(eulerAngles[2]), 6)]
   
   def ConvertEulerToMatrix(self, rotX : float, rotY : float, rotZ : float, notationFrom : Notations) -> Matrix:
      """ Converts the given Euler angles into a rotation matrix.

      Args:
         rotX: rotation around X-axis
         rotY: rotation around Y-axis
         rotZ: rotation around Z-axis
         notationFrom: source notation
         
      Returns:
         returns resulting rotation matrix
      """
      matrixArray = self._getMatrixArrayFromEuler((rotX, rotY, rotZ), self._getEulerOrderNotation(notationFrom))
      return Matrix(matrixArray)
   
   def ConvertMatrixToEuler(self, matrix : Matrix, notationTo : Notations) -> tuple:
      """ Converts the given matrix into Euler angles of the given notation
      
      Args:
         matrix: matrix to convert
         notationFrom: target notation
         
      Returns:
         returns resulting Euler angles in order rotX, rotY, rotZ
      """
      eulerAngles = self._getEulerFromMatrix(matrix.GetArray(), self._getEulerOrderNotation(notationTo))
      return (round(math.degrees(eulerAngles[0]), 6), round(math.degrees(eulerAngles[1]), 6), round(math.degrees(eulerAngles[2]), 6))
   
### private methods

   def _getEulerOrderNotation(self, notation : Notations) -> int:
      EulFrmS = 0
      EulFrmR = 1
      EulRepNo = 0
      EulRepYes = 1
      EulParEven = 0
      EulParOdd = 1
      X = 0
      Y = 1
      Z = 2

      # static axes
      if notation == Notations.Euler_XYZs: 
         return self._getEulerOrderNotationHelper(X, EulParEven, EulRepNo, EulFrmS)
      if notation == Notations.Euler_XYXs:
         return self._getEulerOrderNotationHelper(X, EulParEven, EulRepYes, EulFrmS)
      if notation == Notations.Euler_XZYs:
         return self._getEulerOrderNotationHelper(X, EulParOdd, EulRepNo, EulFrmS)
      if notation == Notations.Euler_XZXs:
         return self._getEulerOrderNotationHelper(X, EulParOdd, EulRepYes, EulFrmS)
      if notation == Notations.Euler_YZXs:
         return self._getEulerOrderNotationHelper(Y, EulParEven, EulRepNo, EulFrmS)
      if notation == Notations.Euler_YZYs:
         return self._getEulerOrderNotationHelper(Y, EulParEven, EulRepYes, EulFrmS)
      if notation == Notations.Euler_YXZs: 
         return self._getEulerOrderNotationHelper(Y, EulParOdd, EulRepNo, EulFrmS)
      if notation == Notations.Euler_YXYs:
         return self._getEulerOrderNotationHelper(Y, EulParOdd, EulRepYes, EulFrmS)
      if notation == Notations.Euler_ZXYs:
         return self._getEulerOrderNotationHelper(Z, EulParEven, EulRepNo, EulFrmS)
      if notation == Notations.Euler_ZXZs:
         return self._getEulerOrderNotationHelper(Z, EulParEven, EulRepYes, EulFrmS)
      if notation == Notations.Euler_ZYXs:
         return self._getEulerOrderNotationHelper(Z, EulParOdd, EulRepNo, EulFrmS)
      if notation == Notations.Euler_ZYZs:
         return self._getEulerOrderNotationHelper(Z, EulParOdd, EulRepYes, EulFrmS)
      # rotating axes
      if notation == Notations.Euler_ZYXr:
         return self._getEulerOrderNotationHelper(X, EulParEven, EulRepNo, EulFrmR)
      if notation == Notations.Euler_XYXr:
         return self._getEulerOrderNotationHelper(X, EulParEven, EulRepYes, EulFrmR)
      if notation == Notations.Euler_YZXr:
         return self._getEulerOrderNotationHelper(X, EulParOdd, EulRepNo, EulFrmR)
      if notation == Notations.Euler_XZXr:
         return self._getEulerOrderNotationHelper(X, EulParOdd, EulRepYes, EulFrmR)
      if notation == Notations.Euler_XZYr:
         return self._getEulerOrderNotationHelper(Y, EulParEven, EulRepNo, EulFrmR)
      if notation == Notations.Euler_YZYr:
         return self._getEulerOrderNotationHelper(Y, EulParEven, EulRepYes, EulFrmR)
      if notation == Notations.Euler_ZXYr:
         return self._getEulerOrderNotationHelper(Y, EulParOdd, EulRepNo, EulFrmR)
      if notation == Notations.Euler_YXYr:
         return self._getEulerOrderNotationHelper(Y, EulParOdd, EulRepYes, EulFrmR)
      if notation == Notations.Euler_YXZr:
         return self._getEulerOrderNotationHelper(Z, EulParEven, EulRepNo, EulFrmR)
      if notation == Notations.Euler_ZXZr:
         return self._getEulerOrderNotationHelper(Z, EulParEven, EulRepYes, EulFrmR)
      if notation == Notations.Euler_XYZr:
         return self._getEulerOrderNotationHelper(Z, EulParOdd, EulRepNo, EulFrmR)
      if notation == Notations.Euler_ZYZr:
         return self._getEulerOrderNotationHelper(Z, EulParOdd, EulRepYes, EulFrmR)

   def _getEulerOrderNotationHelper(self, i : int, p : int, r : int, f : int) -> int:
      return (((((((i) << 1) + (p)) << 1) + (r)) << 1) + (f))
   
   def _getEulerOrder(self, order : int) -> list:
      o = order
      EulSafe = [ 0, 1, 2, 0 ]
      EulNext = [ 1, 2, 0, 1 ]

      f = o & 1
      o >>= 1
      s = o & 1
      o >>= 1
      n = o & 1
      o >>= 1
      i = EulSafe[o & 3]
      j = EulNext[i + n]
      k = EulNext[i + 1 - n]
      if s == 0:
         h = i
      else:
         h = k
      
      return [i, j, k, h, n, s, f]
   
   def _getMatrixArrayFromEuler(self, ea : tuple, order : int) -> list:
      daMatrix = [0.0] * 12

      if len(ea) != 3:
         return daMatrix
      
      ea_x = ea[0]
      ea_y = ea[1]
      ea_z = ea[2]

      i, j, k, h, n, s, f = self._getEulerOrder(order)

      EulFrmR = 1
      EulRepYes = 1
      EulParOdd = 1

      if f == EulFrmR:
         t = ea_x
         ea_x = ea_z
         ea_z = t
      
      if n == EulParOdd:
         ea_x = -ea_x
         ea_y = -ea_y
         ea_z = -ea_z
      
      ti = ea_x
      tj = ea_y
      th = ea_z
      ci = math.cos(math.radians(ti))
      cj = math.cos(math.radians(tj))
      ch = math.cos(math.radians(th))
      si = math.sin(math.radians(ti))
      sj = math.sin(math.radians(tj))
      sh = math.sin(math.radians(th))
      cc = ci * ch
      cs = ci * sh
      sc = si * ch
      ss = si * sh

      if s == EulRepYes:
         daMatrix[i * 3 + i] = cj
         daMatrix[j * 3 + i] = sj * si
         daMatrix[k * 3 + i] = sj * ci
         daMatrix[i * 3 + j] = sj * sh
         daMatrix[j * 3 + j] = -cj * ss + cc
         daMatrix[k * 3 + j] = -cj * cs - sc
         daMatrix[i * 3 + k] = -sj * ch
         daMatrix[j * 3 + k] = cj * sc + cs
         daMatrix[k * 3 + k] = cj * cc - ss
      
      else:
         daMatrix[i * 3 + i] = cj * ch
         daMatrix[j * 3 + i] = sj * sc - cs
         daMatrix[k * 3 + i] = sj * cc + ss
         daMatrix[i * 3 + j] = cj * sh
         daMatrix[j * 3 + j] = sj * ss + cc
         daMatrix[k * 3 + j] = sj * cs - sc
         daMatrix[i * 3 + k] = -sj
         daMatrix[j * 3 + k] = cj * si
         daMatrix[k * 3 + k] = cj * ci
      
      daMatrix[9] = daMatrix[10] = daMatrix[11] = 0.0

      resultArray = [ 1.0, 0.0, 0.0, 0.0, \
                      0.0, 1.0, 0.0, 0.0, \
                      0.0, 0.0, 1.0, 0.0, \
                      0.0, 0.0, 0.0, 1.0 ]
      
      resultArray[0] = daMatrix[0]
      resultArray[4] = daMatrix[1]
      resultArray[8] = daMatrix[2]
      resultArray[1] = daMatrix[3]
      resultArray[5] = daMatrix[4]
      resultArray[9] = daMatrix[5]
      resultArray[2] = daMatrix[6]
      resultArray[6] = daMatrix[7]
      resultArray[10] = daMatrix[8]

      return resultArray

   def _getEulerFromMatrix(self, matrix : list, order: int) -> tuple:
      matrixEntries = [0.0] * 12
      matrixEntries[0] = matrix[0] 
      matrixEntries[1] = matrix[4] 
      matrixEntries[2] = matrix[8] 
      matrixEntries[3] = matrix[1] 
      matrixEntries[4] = matrix[5] 
      matrixEntries[5] = matrix[9]
      matrixEntries[6] = matrix[2]
      matrixEntries[7] = matrix[6]
      matrixEntries[8] = matrix[10]
      matrixEntries[9] = matrix[3]
      matrixEntries[10] = matrix[7]
      matrixEntries[11] = matrix[11]

      i, j, k, h, n, s, f = self._getEulerOrder(order)

      EPS = 0.00001
      EulFrmR = 1
      EulRepYes = 1
      EulParOdd = 1

      ea_x = 0.0
      ea_y = 0.0
      ea_z = 0.0

      if s == EulRepYes:
         sy = math.sqrt(matrixEntries[j * 3 + i] * matrixEntries[j * 3 + i] + matrixEntries[k * 3 + i] * matrixEntries[k * 3 + i])
         if sy > EPS:
            ea_x = math.atan2(matrixEntries[j * 3 + i], matrixEntries[k * 3 + i])
            ea_y = math.atan2(sy, matrixEntries[i * 3 + i])
            ea_z = math.atan2(matrixEntries[i * 3 + j], -matrixEntries[i * 3 + k])
         
         else:
            ea_x = math.atan2(-matrixEntries[k * 3 + j], matrixEntries[j * 3 + j])
            ea_y = math.atan2(sy, matrixEntries[i * 3 + i])
            ea_z = 0
         
      else:
         cy = math.sqrt(matrixEntries[i * 3 + i] * matrixEntries[i * 3 + i] + matrixEntries[i * 3 + j] * matrixEntries[i * 3 + j])
         if cy > 16 * EPS:
            ea_x = math.atan2(matrixEntries[j * 3 + k], matrixEntries[k * 3 + k])
            ea_y = math.atan2(-matrixEntries[i * 3 + k], cy)
            ea_z = math.atan2(matrixEntries[i * 3 + j], matrixEntries[i * 3 + i])
         
         else:
            ea_x = math.atan2(-matrixEntries[k * 3 + j], matrixEntries[j * 3 + j])
            ea_y = math.atan2(-matrixEntries[i * 3 + k], cy)
            ea_z = 0
         
      if n == EulParOdd:
         ea_x = -ea_x
         ea_y = -ea_y
         ea_z = -ea_z

      if f == EulFrmR:
         t = ea_x
         ea_x = ea_z
         ea_z = t
      
      return (ea_x, ea_y, ea_z)