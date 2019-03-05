"""
Ease Out

Copyright Cody Sorgenfrey (www.codysorgenfrey.com)

Name-US: Ease Out
Description-US: Set the easing of the selected keyframes to the cubic-bezier value specified in Easing Values.
"""

import c4d
from ChangeDefaultEasing.common import *

def easeOutKeys(keys, easing):
	x = 0
	count = len(keys)
	while x < (count-1):
		firstKey = keys[x][0]
		secondKey = keys[x+1][0]
		
		minVal = firstKey.GetValue()
		minTime = firstKey.GetTime().Get()
	
		maxVal = secondKey.GetValue()
		maxTime = secondKey.GetTime().Get()
					
		firstKeyRVal = 0
		firstKeyRTime = ((maxTime-minTime) * easing) * .75
		
		lastKeyLVal = 0
		lastKeyLTime = 0
				
		firstKey.SetInterpolation(firstKey.GetCurve(), c4d.CINTERPOLATION_SPLINE)
		secondKey.SetInterpolation(secondKey.GetCurve(), c4d.CINTERPOLATION_SPLINE)
		
		firstKey.ChangeNBit(c4d.NBIT_CKEY_BREAK, c4d.NBITCONTROL_SET)
		secondKey.ChangeNBit(c4d.NBIT_CKEY_BREAK, c4d.NBITCONTROL_SET)
		
		firstKey.ChangeNBit(c4d.NBIT_CKEY_AUTO, c4d.NBITCONTROL_CLEAR)
		secondKey.ChangeNBit(c4d.NBIT_CKEY_AUTO, c4d.NBITCONTROL_CLEAR)
		
		firstKey.ChangeNBit(c4d.NBIT_CKEY_LOCK_O, c4d.NBITCONTROL_CLEAR)
		secondKey.ChangeNBit(c4d.NBIT_CKEY_LOCK_O, c4d.NBITCONTROL_CLEAR)
		
		firstKey.ChangeNBit(c4d.NBIT_CKEY_LOCK_L, c4d.NBITCONTROL_CLEAR)
		secondKey.ChangeNBit(c4d.NBIT_CKEY_LOCK_L, c4d.NBITCONTROL_CLEAR)
		
		firstKey.ChangeNBit(c4d.NBIT_CKEY_REMOVEOVERSHOOT, c4d.NBITCONTROL_CLEAR)
		secondKey.ChangeNBit(c4d.NBIT_CKEY_REMOVEOVERSHOOT, c4d.NBITCONTROL_CLEAR)
		
		firstKey.ChangeNBit(c4d.NBIT_CKEY_CLAMP, c4d.NBITCONTROL_CLEAR)
		secondKey.ChangeNBit(c4d.NBIT_CKEY_CLAMP, c4d.NBITCONTROL_CLEAR)
		
		firstKey.SetValueRight(firstKey.GetCurve(), firstKeyRVal)
		firstKey.SetTimeRight(firstKey.GetCurve(), c4d.BaseTime(firstKeyRTime))
		
		secondKey.SetValueLeft(secondKey.GetCurve(), lastKeyLVal)
		secondKey.SetTimeLeft(secondKey.GetCurve(), c4d.BaseTime(lastKeyLTime))
		
		x += 1		

def main():
	doc.StartUndo()
	
	keyGroups = []
	
	obj = doc.GetFirstObject()
	scene = ObjectIterator(obj)
	
	for obj in scene:
		findSelectedKeys(obj, keyGroups)
		tags = TagIterator(obj)
		for tag in tags:
			findSelectedKeys(tag, keyGroups)
	
	materials = MaterialIterator(doc)
	
	for mat in materials:
		findSelectedKeys(mat, keyGroups)
	
	if len(keyGroups) > 0:
		easing = Read(filepath, filekey)
		if not easing:
			easing = [1, 1, 1]
	
		for keys in keyGroups:
			resetSelection(keys)
			easeOutKeys(keys, easing[2])
	
	doc.EndUndo()
	c4d.EventAdd()

if __name__=='__main__':
	main()