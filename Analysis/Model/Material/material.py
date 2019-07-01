# -*- coding = utf-8 -*-

class Material(object):
  def __init__(self, initial_stiffness: float):
    self.initial_stiffness = initial_stiffness

  def stiffness(self,strain):
    # デフォルトは弾性
    return self.initial_stiffness

  def stress(self,strain):
    return self.stiffness(strain)*strain
  

class Steel(Material):
  def __init__(self, initial_stiffness: float, yield_stress: float, alfa:float = 1.0):
    super().__init__(initial_stiffness)
    self.yield_stress = yield_stress
    self.yield_strain = yield_stress / initial_stiffness
    self.alfa = alfa
  
  def stress(self,strain):
    if strain < self.yield_strain:
      return self.stiffness(strain)*strain
    else:
      return self.yield_stress + self.stiffness(strain)*(strain - self.yield_strain)
  
  def stiffness(self,strain):
    if strain < self.yield_strain:
      return self.initial_stiffness
    else:
      return self.alfa*self.initial_stiffness
  


