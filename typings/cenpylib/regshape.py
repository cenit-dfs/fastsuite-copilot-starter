from centypes import *
import math

class RegshapeUtil():
   def __init__(self, operator):
      self.op = operator
      self.shift = [0,0,0,0,0,0] 

   def GetRegshapeCircle(self, shiftReference, radius, overrun=0, leadin=0):
      """Create a circle regshape
      Args:
         shiftReference (List): shift of the reference toolpath in this form [x, y, z, x_rotaion, y_rotaion, z_rotaion]
         radius (num): the radius of the regshape
         overrun (num): the overrun of the regshape
         leadin (num): the leadin of the regshape
      Returns:
         List:\\
            0. Reference Matrix\\
            1. Leadin Matrix\\
            2. Start +X Postion Matrix\\
            3. [Start -X Postion Matrix, Via +Y Point Matrix]\\
            4. [Overcut Matrix, Via -Y Point Matrix]
      """

      matrixList = []
      self.shift = shiftReference

      x2, y2 = RegshapeUtil.coordinates_on_circle_given_arc_length(radius, overrun)

      matrixList.append(self._GetReferenceMatrix()) # Reference Matrix

      matrixList.append(self._LinTranslate(radius-leadin, 0, 0)) # Leadin Matrix
   
      matrixList.append(self._LinTranslate(radius, 0, 0)) # Start +X Postion Matrix 
      matrixList.append(self._CirTranslate(0, radius, 0, -radius, 0, 0)) # [Start -X Postion Matrix, Via +Y Point Matrix]   
      matrixList.append(self._CirTranslate(0, -radius, 0, x2, y2, 0)) # [Overcut Matrix, Via -Y Point Matrix]

      self.shift = [0,0,0,0,0,0]

      return matrixList

   def GetRegshapeRectangle(self, shiftReference, length, height, radius=0, overrun=0, leadin=0):
      """Create a rectangle regshape
      Args:
         shiftReference (List): shift of the reference toolpath in this form [x, y, z, x_rotaion, y_rotaion, z_rotaion]
         length (num): the length of the regshape
         hight (num): the hight of the regshape
         radius (num): the corner radius of the regshape
         overrun (num): the overrun of the regshape
         leadin (num): the leadin of the regshape
      Returns:
         List:\\
            0. Reference Matrix\\
            1. Leadin Matrix\\
            2. Start Postion +Y Matrix\\
            3. Feature Point 1 +X+Y Matrix\\
            4. [Feature Point 2 +X+Y Matrix, Via Point +X+Y Matrix]\\
            5. Start Postion +X Matrix\\
            6. Feature Point 1 +X-Y Matrix\\
            7. [Feature Point 2 +X-Y Matrix, Via Point +X-Y Matrix]\\
            8. Start Postion -Y Matrix\\
            9. Feature Point 1 -X-Y Matrix\\
            10. [Feature Point 2 -X-Y Matrix, Via Point -X-Y Matrix]\\
            11. Start Postion -X Matrix\\
            12. Feature Point 1 -X+Y Matrix\\
            13. [Feature Point 2 -X+Y Matrix, Via Point -X+Y Matrix]\\
            14. Overcut Matrix
      """

      matrixList = []
      self.shift = shiftReference

      midRX, midRY = RegshapeUtil.coordinates_on_circle_given_degrees(radius, 30)

      matrixList.append(self._GetReferenceMatrix()) # Reference Matrix
      
      matrixList.append(self._LinTranslate(0, -height/2+leadin, 0)) # Leadin Matrix
      
      matrixList.append(self._LinTranslate(0, -height/2, 0)) # Start Postion +Y Matrix
      matrixList.append(self._LinTranslate(length/2-radius, -height/2, 0)) # Feature Point +X+Y Matrix
      matrixList.append(self._CirTranslate(length/2-radius + midRX, -height/2 + midRY, 0, length/2, -height/2+radius, 0)) # [Feature Point 2 +X+Y Matrix, Via Point +X+Y Matrix]
      
      matrixList.append(self._LinTranslate(length/2, 0, 0))
      matrixList.append(self._LinTranslate(length/2, height/2-radius, 0))
      matrixList.append(self._CirTranslate(length/2-radius + midRX, height/2 - midRY, 0, length/2-radius, height/2, 0))
      
      matrixList.append(self._LinTranslate(0, height/2, 0))
      matrixList.append(self._LinTranslate(-length/2+radius, height/2, 0))
      matrixList.append(self._CirTranslate(-length/2+radius - midRX, height/2 - midRY, 0, -length/2, height/2-radius, 0))

      matrixList.append(self._LinTranslate(-length/2, 0, 0))
      matrixList.append(self._LinTranslate(-length/2, -height/2+radius, 0))
      matrixList.append(self._CirTranslate(-length/2+radius - midRX, -height/2 + midRY, 0, -length/2+radius, -height/2, 0))
   
      matrixList.append(self._LinTranslate(overrun, -height/2, 0))

      self.shift = [0,0,0,0,0,0]
      
      return matrixList

   def GetRegshapeSlot(self, shiftReference, length, height, radius, overrun=0, leadin=0):
      """Create a slot regshape
      Args:
         shiftReference (List): shift of the reference toolpath in this form [x, y, z, x_rotaion, y_rotaion, z_rotaion]
         length (num): the length of the regshape
         hight (num): the hight of the regshape
         radius (num): the corner radius of the regshape
         overrun (num): the overrun of the regshape
         leadin (num): the leadin of the regshape
      Returns:
         List:
            0. Reference Matrix\\
            1. Leadin Matrix\\
            2. Start Postion +Y Matrix\\
            3. Feature Point +X+Y Matrix\\
            4. [Feature Point +X-Y Matrix, Via Point +X Matrix]\\
            5. Start Postion -Y Matrix\\
            6. Feature Point -X-Y Matrix\\
            7. [Feature Point -X+Y Matrix, Via Point -X Matrix]\\
            8. Overcut Matrix
      """

      matrixList = []
      self.shift = shiftReference

      matrixList.append(self._GetReferenceMatrix()) # Reference Matrix
   
      matrixList.append(self._LinTranslate(0, -height/2+leadin, 0)) # Leadin Matrix
   
      matrixList.append(self._LinTranslate(0, -height/2, 0))
      matrixList.append(self._LinTranslate(length/2-radius, -height/2, 0))
      matrixList.append(self._CirTranslate(length/2, 0, 0, length/2-radius, height/2, 0))
    
      matrixList.append(self._LinTranslate(0, height/2, 0))
      matrixList.append(self._LinTranslate(-length/2+radius, height/2, 0))
      matrixList.append(self._CirTranslate(-length/2, 0, 0, -length/2+radius, -height/2, 0))
   
      matrixList.append(self._LinTranslate(overrun, -height/2, 0))

      self.shift = [0,0,0,0,0,0]

      return matrixList

   def _GetReferenceMatrix(self):
      """
      Args:

      Returns:
            
      """
      
      M = self.op.GetRefTpElement().GetInitialPathMatrix()
      M.Translate(self.shift[0], self.shift[1], self.shift[2], True)
      return M

   def _LinTranslate(self, x, y, z):
      """
      Args:

      Returns:
            
      """

      M = self._GetMatrixFromRefPoint()
      M.Translate(x, y, z, True)
      return M


   def _CirTranslate(self, x1, y1, z1, x2, y2, z2):
      """
      Args:

      Returns:
            
      """
   
      M1 = self._GetMatrixFromRefPoint()
      M1.Translate(x1, y1, z1, True)
      M2 = self._GetMatrixFromRefPoint()
      M2.Translate(x2, y2, z2, True)
      return [M2, M1]
  
   def _GetMatrixFromRefPoint(self):
      """
      Args:

      Returns:
            
      """
      M = self._GetReferenceMatrix() 

      M.RotateX(self.shift[3]) # rotate M with shiftReference rotation settings
      M.RotateY(self.shift[4])
      M.RotateZ(self.shift[5]) 
      return M

   def coordinates_on_circle_given_arc_length(radius, arc_length):
      # Calculate the angle in radians
      angle_radians = arc_length / radius
   
      # Calculate x and y using parametric equations
      x = radius * math.cos(angle_radians)
      y = radius * math.sin(angle_radians)
   
      return x, y

   def coordinates_on_circle_given_degrees(radius, angle_degrees):
      angle_radians = math.radians(angle_degrees)
      # Calculate x and y using parametric equations
      x = radius * math.cos(angle_radians)
      y = radius * math.sin(angle_radians)
   
      return x, y

   def AddLaserOnEvent(Operator, point, action = 0, insertpos = TPINSERTPOS_INSERTBEFORE):
      laserEvent = Operator.GetEventOperator().AddEvent("D1832B09-745C-49A6-B318-8E283B972B5B", point, insertpos)

   def AddLaserOffEvent(Operator, point, action = 0, insertpos = TPINSERTPOS_INSERTBEFORE):
      laserEvent = Operator.GetEventOperator().AddEvent("395C3E6D-6EE9-46C6-B04E-EAB23CE212ED", point, insertpos)