# -*- coding = utf-8 -*-


from .Model.Section import section 
from .Model.Material import material
from .Model.CalcModel import fiber_model

class AnalysisManager(object):
  def __init__(self):
    self.result = []
    self.section = None
    self.material = None
  
  def run_analysis(self):
    self.set_section()
    self.set_material()
    intDivisionForWidth=10
    intDivisionForHeight=20
    self.calc_model = fiber_model.FiberModel(self.section,intDivisionForWidth,intDivisionForHeight,self.material)


  def set_section(self):
    height = 100
    width = 200
    self.section = section.RectSection(height,width,0,0)
  
  def set_material(self):
    initial_stiffness = 205.0
    yield_strength = 0.258
    alfa = 0.001
    self.material = material.Steel(initial_stiffness,yield_strength,alfa)

    

