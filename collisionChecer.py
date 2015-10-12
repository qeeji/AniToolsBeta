import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds

def collisioncheck(*pArgs):
	
	coll_frames = []
	
	def goThroughMesh(iter):
		lix =[]
		liz =[]
		liy = []
		while(meshIter.isDone() == 0):
			pt = OpenMaya.MPoint()
			pt = meshIter.position(OpenMaya.MSpace.kWorld)
			vertIndex = meshIter.index()
			lix.append(pt.x)
			liy.append(pt.y)
			liz.append(pt.z)
			meshIter.next()
		return lix, liy, liz
	
	def maxMin(lix, liy, liz):
		maxpt = OpenMaya.MPoint()
		minpt = OpenMaya.MPoint()
		maxx = max(lix)
		maxy = max(liy)
		maxz = max(liz)
		minx = min(lix)
		miny = min(liy)
		minz = min(liz)
		maxpt.x = maxx 
		maxpt.y = maxy
		maxpt.z = maxz
		minpt.x = minx 
		minpt.y = miny
		minpt.z = minz 
		return maxpt, minpt


	
	startTime = int(cmds.playbackOptions(query = True , minTime = True))
	endTime = int(cmds.playbackOptions(query = True , maxTime = True))
	
	
	for time in range(startTime , endTime+1):
		cmds.currentTime(time)	
		
		intersects = False
		#stat = OpenMaya.MStatus.kSuccess
		selection = OpenMaya.MSelectionList()
		OpenMaya.MGlobal.getActiveSelectionList( selection )
		dagPath = OpenMaya.MDagPath()
		component = OpenMaya.MObject()
		vertIndex = 0
			
		iter = OpenMaya.MItSelectionList(selection)
			
		while(iter.isDone() == 0):
			iter.getDagPath(dagPath,component)
			meshIter = OpenMaya.MItMeshVertex(dagPath, component)
			try:
				lix, liy, liz = goThroughMesh(iter)
				maxpt1, minpt1 = maxMin(lix, liy, liz)
				bbox1 = OpenMaya.MBoundingBox(maxpt1, minpt1)
				iter.next()
			except:
				pass
			iter.getDagPath(dagPath,component)
			meshIter = OpenMaya.MItMeshVertex(dagPath, component)
			lix, liy, liz = goThroughMesh(iter)
			maxpt2, minpt2 = maxMin(lix, liy, liz) 
			bbox2 = OpenMaya.MBoundingBox(maxpt2, minpt2)
			iter.next()
			
		intersects = OpenMaya.MBoundingBox.intersects(bbox1, bbox2)
		
		print time		
		print intersects
		if intersects is True:
			coll_frames.append(time)
		
	return coll_frames
