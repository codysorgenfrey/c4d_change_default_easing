"""
Easing Values

Copyright Cody Sorgenfrey (www.codysorgenfrey.com)

Name-US: Easing Values
Description-US: Set the values used in the cubic-bezier function of the easing scripts.
"""
import c4d
from c4d import gui
from ChangeDefaultEasing.common import *

class BANNER(c4d.gui.GeUserArea):
	def __init__(self):
		self.bmp = c4d.bitmaps.BaseBitmap()
	
	def GetMinSize(self):
		self.width = 400 ####WIDTH OF YOUR IMAGE FILE
		self.height = 40 ####HEIGHT OF YOUR IMAGE FILE
		return (self.width, self.height)
	
	def DrawMsg(self, x1, y1, x2, y2, msg):
		path = os.path.join(os.path.dirname(__file__), "ChangeDefaultEasingHeader.png")
		result, ismovie = self.bmp.InitWith(path)
		x1 = 0
		y1 = 0
		x2 = self.bmp.GetBw()
		y2 = self.bmp.GetBh()
		if result == c4d.IMAGERESULT_OK:
			self.DrawBitmap(self.bmp, 0, 0, self.bmp.GetBw(), self.bmp.GetBh(), x1, y1, x2, y2, c4d.BMP_NORMAL)

GROUP_VALUES = 10000
TEXT_EASE = 10007
TEXT_IN = 10008
TEXT_OUT = 10009
TEXT_TL = 10011
VALUE_EASE = 10001
VALUE_IN = 10002
VALUE_OUT = 10003
VALUE_TL = 10010
BUTTON_OK = 10004
BUTTON_CANCEL = 10005
GROUP_ACTIONS = 10006
COMBO1 = 10012
COMBO2 = 10013
COMBO3 = 10014
COMBO4 = 10015
HEADERGROUP = 10016
HEADERIMAGE = 10017

class OptionsDialog(gui.GeDialog):
	
	LOGO = BANNER()

	def CreateLayout(self):
		
		self.SetTitle("Update Easing Values")
		#logo group
		self.GroupBegin(HEADERGROUP, c4d.BFH_CENTER | c4d.BFV_CENTER, cols=1)
		self.GroupBorderNoTitle(c4d.BORDER_NONE)
		self.GroupBorderSpace(0, 0, 0, 0)
		self.AddUserArea(HEADERIMAGE, c4d.BFV_CENTER | c4d.BFV_CENTER)    
		self.AttachUserArea(self.LOGO, HEADERIMAGE)
		self.GroupEnd()
		# end logo group
		self.GroupBegin(GROUP_VALUES, c4d.BFH_SCALEFIT, 2, 1,)
		self.GroupBorderSpace(4,4,4,4)
		self.AddStaticText(TEXT_EASE, c4d.BFH_LEFT, name="Easy Ease")
		self.AddEditSlider(VALUE_EASE, c4d.BFH_SCALEFIT)
		self.AddStaticText(TEXT_IN, c4d.BFH_LEFT, name="Ease In")
		self.AddEditSlider(VALUE_IN, c4d.BFH_SCALEFIT)
		self.AddStaticText(TEXT_OUT, c4d.BFH_LEFT, name="Ease Out")
		self.AddEditSlider(VALUE_OUT, c4d.BFH_SCALEFIT)
		self.AddStaticText(TEXT_TL, c4d.BFH_LEFT, name="Timeline")
		self.AddComboBox(VALUE_TL, c4d.BFH_SCALEFIT)
		self.AddChild(VALUE_TL, COMBO1, "Timeline 1 (Default)")
		self.AddChild(VALUE_TL, COMBO2, "Timeline 2")
		self.AddChild(VALUE_TL, COMBO3, "Timeline 3")
		self.AddChild(VALUE_TL, COMBO4, "Timeline 4")
		self.GroupEnd()
		
		self.GroupBegin(GROUP_ACTIONS, c4d.BFH_CENTER|c4d.BFV_BOTTOM, 2, 1)
		self.GroupBorderSpace(4,4,4,4)
		self.AddButton(BUTTON_OK, c4d.BFH_SCALE, 50, 15, name="Ok")
		self.GroupEnd()
		return True
		
	def Command(self, id, msg):
		if id == BUTTON_OK:
			bc = c4d.BaseContainer()
			bc[0] = self.GetFloat(VALUE_EASE)
			bc[1] = self.GetFloat(VALUE_IN)
			bc[2] = self.GetFloat(VALUE_OUT)
			bc[3] = self.GetLong(VALUE_TL)
			Write(filepath, filekey, bc)
			self.Close()
		if id == 1:
			self.Command(BUTTON_OK, msg)
		return True
		
	def InitValues(self):
		bc = Read(filepath, filekey)
		if bc:
			self.SetFloat(VALUE_EASE, value=bc[0], min=0, max=1, step=.01, format=c4d.FORMAT_PERCENT, min2=0, max2=1)
			self.SetFloat(VALUE_IN, value=bc[1], min=0, max=1, step=.01, format=c4d.FORMAT_PERCENT, min2=0, max2=1)
			self.SetFloat(VALUE_OUT, value=bc[2], min=0, max=1, step=.01, format=c4d.FORMAT_PERCENT, min2=0, max2=1)
			self.SetLong(VALUE_TL, bc[3])
		else:
			bc = c4d.BaseContainer()
			bc[0] = 1
			bc[1] = 1
			bc[2] = 1
			bc[3] = COMBO1
			Write(filepath, filekey, bc)
			self.InitValues()
		return True
	

def main():
	myDialog = OptionsDialog()
	myDialog.Open(c4d.DLG_TYPE_MODAL, defaultw=375)
	
if __name__=='__main__':
	main()