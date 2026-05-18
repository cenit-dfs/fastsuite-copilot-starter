"""COPYRIGHT Cenit AG 2023"""


class DynamicLimits:
   """Dynamic limits utility functions."""
   
   def Ramp(joint, x1, y1, x2, y2):
      """Linear step function of joint, where the inputs x1, y1, x2, y2 are used to define the ramp.

      Args:
          joint (float): current joint value.
          x1 (float): value used for calculation.
          y1 (float): value used for calculation.
          x2 (float): value used for calculation.
          y2 (float): value used for calculation.

      Returns:
          float: ramp value.
      """
      
      if joint < x1:
         return y1
      elif joint > x2:
         return y2
      else:
         dx = x2 - x1
         if abs(dx) < 1e-20:
            if joint < (x1+x2)/2.0:
               return y1
            elif joint > (x1+x2)/2.0:
               return y2
            else:
               return ((y1+y2)/2.0)
         else:
            dy = y2 - y1
            slope = dy/dx
            return (y1 + (joint - x1) * slope)
