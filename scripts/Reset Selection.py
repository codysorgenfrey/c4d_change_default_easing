"""
Reset Selection

Copyright Cody Sorgenfrey (www.codysorgenfrey.com)

Name-US: Reset Selection
Description-US: Linearize selected keys and remove the key between them (for high easy ease values).
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
		for keys in keyGroups:
			resetSelection(keys)
	
	c4d.EventAdd(c4d.MSG_UPDATE)
	doc.EndUndo()

if __name__=='__main__':
	main()