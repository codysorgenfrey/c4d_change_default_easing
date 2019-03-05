import c4d, os
from c4d import gui, storage as st

g_pluginID = 1051473

class ObjectIterator:
	def __init__(self, baseObject):
		self.baseObject = baseObject
		self.currentObject = baseObject
		self.objectStack = []
		self.depth = 0
		self.nextDepth = 0

	def __iter__(self):
		return self

	def next(self):
		if self.currentObject == None :
			raise StopIteration

		obj = self.currentObject
		self.depth = self.nextDepth

		child = self.currentObject.GetDown()
		if child :
			self.nextDepth = self.depth + 1
			self.objectStack.append(self.currentObject.GetNext())
			self.currentObject = child
		else :
			self.currentObject = self.currentObject.GetNext()
			while( self.currentObject == None and len(self.objectStack) > 0 ) :
				self.currentObject = self.objectStack.pop()
				self.nextDepth = self.nextDepth - 1
		return obj
		
class TagIterator:
	def __init__(self, obj):
		currentTag = None
		if obj :
			self.currentTag = obj.GetFirstTag()

	def __iter__(self):
		return self

	def next(self):
		tag = self.currentTag
		if tag == None :
			raise StopIteration

		self.currentTag = tag.GetNext()
		return tag
		
class MaterialIterator:
	def __init__(self, doc):
		self.doc = doc
		self.currentMaterial = None
		if doc == None : return
		self.currentMaterial = doc.GetFirstMaterial()

	def __iter__(self):
		return self

	def next(self):
		if self.currentMaterial == None :
			raise StopIteration

		mat = self.currentMaterial
		self.currentMaterial = self.currentMaterial.GetNext()
		return mat

filekey = 12345 # Choose a custom ident
filepath = os.path.join(st.GeGetStartupWritePath(), "library", "scripts", "Change Default Easing", "defaults.ease")

def Write(filepath, filekey, data):
	hf = st.HyperFile()
	if hf.Open(ident=filekey, filename=filepath, mode=c4d.FILEOPEN_WRITE, error_dialog=c4d.FILEDIALOG_NONE):
		hf.WriteContainer(data)
		hf.Close()
		return True
	else:
		return False

def Read(filepath, filekey):
	hf = st.HyperFile()
	if hf.Open(ident=filekey, filename=filepath, mode=c4d.FILEOPEN_READ, error_dialog=c4d.FILEDIALOG_NONE):
		bc = hf.ReadContainer()
		hf.Close()
		return bc
	else:
		return False
		
def findSelectedKeys(obj, keyGroups):
	bc = Read(filepath, filekey)
	if not bc:
		bc = [1,1,1,10012]

	if bc[3] == 10012:
		timeline = [c4d.NBIT_TL1_SELECT2, c4d.NBIT_TL1_SELECT]
	elif bc[3] == 10013:
		timeline = [c4d.NBIT_TL2_SELECT2, c4d.NBIT_TL2_SELECT]
	elif bc[3] == 10014:
		timeline = [c4d.NBIT_TL3_SELECT2, c4d.NBIT_TL3_SELECT]
	else:
		timeline = [c4d.NBIT_TL4_SELECT2, c4d.NBIT_TL4_SELECT]
		
	track = obj.GetFirstCTrack()
	if track:
		while track:
			curve = track.GetCurve()
			x = 0
			count = curve.GetKeyCount()
			keys = []
			while x < count:
				key = curve.GetKey(x)
				if key.GetNBit(timeline[0]) or key.GetNBit(timeline[1]):
					keys.append([key, x])
				x += 1
			if len(keys) > 0:
				keyGroups.append(keys)
			track = track.GetNext()

def resetSelection(keys):
	x = 0
	while x < len(keys):
		if keys[x][0].GetNBit(c4d.NBIT_CKEY_BREAKDOWNCOLOR):
			keyTime = keys[x][0].GetTime()
			keyCurve = keys[x][0].GetCurve()
			keyID = keyCurve.FindKey(keyTime)["idx"]
			keyCurve.DelKey(keyID)
			del keys[x]
		else:
			keys[x][0].SetInterpolation(keys[x][0].GetCurve(), c4d.CINTERPOLATION_LINEAR)

		x += 1
	c4d.EventAdd()