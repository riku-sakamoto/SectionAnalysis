# -*- coding = utf-8 -*-


class Section(object):
  def __init__(self,Height,Width,Flange,Web):
    self.height = Height
    self.width = Width
    self.flange = Flange
    self.web = Web
  

class RectSection(Section):
  def __init__(self,Height,Width,Flange,Web):
    super().__init__(Height,Width,Flange,Web)

class Hsection(Section):
  def __init__(self,Height,Width,Flange,Web):
    super().__init__(Height,Width,Flange,Web)
