# -*- coding = utf-8 -*-

'''
ファイバーモデル構成クラス
'''

from collections import namedtuple
from enum import Enum

import numpy as np

from Material import material
from Section import section

#region セグメント
class Segment(object):
  def __init__(self,Material:material.Material,position_x,position_y,size_x,size_y):
    self.Material = Material
    self.Position = namedtuple("Position",("x","y","z"))
    self.Position.x = position_x
    self.Position.y = position_y
    self.Position.z = 0.0

    self.Size = namedtuple("Size",("x","y","z"))
    self.Size.x = size_x
    self.Size.y = size_y

    self.StressState = namedtuple("Stress",("axis"))
    self.StrainState = namedtuple("Strain",("axis"))
  
  @property
  def axial_stiffness(self):
    strain = self.StrainState.axis
    stiffness = self.Material.stiffness(strain)
    return stiffness*self.Size.y*self.Size.z
  
  def update_segment_state(self,entire_displacement_state:{StateDirection:float}):
    df_dy = np.tan(entire_displacement_state[StateDirection.RY]) # Y軸周りの傾き（y軸方向の傾き）
    df_dz = np.tan(entire_displacement_state[StateDirection.RX]) # X軸周りの傾き（z軸方向の傾き）
    dx0 = entire_displacement_state[StateDirection.DZ]
    vertical_displacement = self.Position.y*df_dy + self.Position.z*df_dz + dx0

    self.StrainState.axis = vertical_displacement/self.axial_stiffness
    self.StressState.axis = self.Material.stress(self.StrainState.axis)

#endregion



#region ファイバーモデル

class FiberModel(object):
  def __init__(self,Section:section.Section,intDivisionForWidth,intDivisionForHeight,material:material.Material):
    self.Section = Section
    self.segments_lst=[]
    self.entire_load_state = {direction:0.0 for direction in StateDirection}
    self.entire_deform_state = {direction:0.0 for direction in StateDirection}
    self.entire_stiffness_state = {direction:0.0 for direction in StateDirection}

    self.set_segments(intDivisionForWidth,intDivisionForHeight,material)

  
  def set_segments(self,intDivisionForWidth,intDivisionForHeight,material:material.Material):
    if self.Section.__class__.__name__ == section.RectSection.__class__.__name__:
      width = self.Section.width / intDivisionForWidth
      height = self.Section.height / intDivisionForHeight

      PosXlist = [width*0.5+i*width for i in range(intDivisionForWidth)]
      PosYlist = [height*0.5+i*height for i in range(intDivisionForHeight)]

      for x,y in zip(PosXlist,PosYlist):
        segment = Segment(material,x,y,width,height)
        self.segments_lst.append(segment)

  def update_stress_state(self,direction:StateDirection,value:float):
    if direction == StateDirection.DZ:
      stiffness = self.get_axial_stiffness()
    elif direction == StateDirection.RX:
      stiffness = self.get_moment_stiffness(direction)
    elif direction == StateDirection.RY:
      stiffness = self.get_moment_stiffness(direction)
    else:
      raise Exception("未定義の応力状態です。")

    self.entire_load_state[direction] = value
    self.entire_deform_state[direction] = value/stiffness
    self.entire_stiffness_state[direction] = stiffness

    self.update_segments_state()
  
  def update_segments_state(self):
    for segment in self.segments_lst:
      segment.update_segment_state(self.entire_deform_state)

  def get_axial_stiffness(self):
    axial_stiffness = sum([segment.axial_stiffness for segment in self.segments_lst])
    return axial_stiffness
  
  def get_moment_stiffness(self,direction:StateDirection):
    if direction != StateDirection.RX or direction != StateDirection.RY:
      raise Exception("定義されていない応力状態です。")
    else:
      # 中立軸の移動量
      if direction == StateDirection.RX:
        y_0 = sum([segment.axial_stiffness*segment.y for segment in self.segments_lst])/sum([segment.axial_stiffness for segment in self.segments_lst])
        flexural_stiffness = sum([segment.axial_stiffness*(segment.y - y_0)**2.0 for segment in self.segments_lst])
      else :
        x_0 = sum([segment.axial_stiffness*segment.x for segment in self.segments_lst])/sum([segment.axial_stiffness for segment in self.segments_lst])
        flexural_stiffness = sum([segment.axial_stiffness*(segment.x - x_0)**2.0 for segment in self.segments_lst])
      return flexural_stiffness

#endregion

class StateDirection(Enum):
  DX = 0,
  DY = 1,
  DZ = 2,
  RX = 3,
  RY = 4,
  RZ = 5


if __name__ == "__main__":
  pass