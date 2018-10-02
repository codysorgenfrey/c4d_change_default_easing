"""
Easy Ease

Copyright Cody Sorgenfrey (www.codysorgenfrey.com)

Name-US: Easy Ease
Description-US: Set the easing of the selected keyframes to the cubic-bezier value specified in Easing Values.
"""

import c4d
from ChangeDefaultEasing.common import *

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
			easyEaseKeys(keys, easing[0])			
			
	c4d.EventAdd(c4d.MSG_UPDATE)
	doc.EndUndo()

if __name__=='__main__':
	main()