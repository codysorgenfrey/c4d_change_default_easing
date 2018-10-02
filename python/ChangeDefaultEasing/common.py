import c4d, os
from c4d import gui, storage as st

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

def easeOutKeys(keys, easing):
	x = 0
	count = len(keys)
	while x < (count - 1):
		firstKey = keys[x][0]
		secondKey = keys[x+1][0]
		
		minVal = firstKey.GetValue()
		minTime = firstKey.GetTime().Get()
	
		maxVal = secondKey.GetValue()
		maxTime = secondKey.GetTime().Get()
					
		firstKeyRVal = ((maxVal-minVal)*.75) * easing
		firstKeyRTime = 0
		
		lastKeyLVal = 0
		lastKeyLTime = (-1*((maxTime-minTime)*.75)) * easing
		
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

def easeInKeys(keys, easing):
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
		firstKeyRTime = ((maxTime-minTime)*.75) * easing
		
		lastKeyLVal = (-1*((maxVal-minVal)*.75)) * easing
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
		
def easyEaseKeys(keys, easing):
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
		firstKeyRTime = ((maxTime-minTime)*.75) * easing
		
		lastKeyLVal = 0
		lastKeyLTime =  (-1*((maxTime-minTime)*.75)) * easing
		
		if easing > .75:
			midVal = minVal + (maxVal-minVal)/2
			midTime = minTime+((maxTime - minTime)/2)
			midKeyLVal = (-1*((maxVal-minVal)*.2)) * easing
			midKeyLTime = 0
			midKeyRVal = ((maxVal-minVal)*.2) * easing
			midKeyRTime = 0
		
			newKey = firstKey.GetCurve().AddKey(c4d.BaseTime(midTime))
			newKey["key"].SetValue(newKey["key"].GetCurve(), midVal)
			newKey["key"].SetInterpolation(newKey["key"].GetCurve(), c4d.CINTERPOLATION_SPLINE)
			newKey["key"].ChangeNBit(c4d.NBIT_CKEY_AUTO, c4d.NBITCONTROL_CLEAR)
			newKey["key"].SetValueLeft(newKey["key"].GetCurve(), midKeyLVal)
			newKey["key"].SetTimeLeft(newKey["key"].GetCurve(), c4d.BaseTime(midKeyLTime))
			newKey["key"].SetValueRight(newKey["key"].GetCurve(), midKeyRVal)
			newKey["key"].SetTimeRight(newKey["key"].GetCurve(), c4d.BaseTime(midKeyRTime))
			
			firstKeyRTime = firstKeyRTime * .5
			lastKeyLTime = lastKeyLTime * .5
		
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

def resetSelection(keys):
	keys.reverse()
	x = 0
	while x < (len(keys)-1):
		firstKey = keys[x]
		x += 1
		lastKey = keys[x]
		if (firstKey[1]-1) != lastKey[1]:
			middleKey = firstKey[0].GetCurve().GetKey(firstKey[1]-1)
			timeSearch = middleKey.GetCurve().FindKey(middleKey.GetTime())
			middleKey.GetCurve().DelKey(timeSearch["idx"])
		
		firstKey[0].SetInterpolation(firstKey[0].GetCurve(), c4d.CINTERPOLATION_LINEAR)
		lastKey[0].SetInterpolation(lastKey[0].GetCurve(), c4d.CINTERPOLATION_LINEAR)
	keys.reverse()