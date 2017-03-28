'''
Script to test automation of render layers setup
@author: sharmah
'''

##import render setup and maya commands modules
import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.app.renderSetup.model.override as override
import maya.cmds as cmds

class Layer(object):
    def __init__(self, layerName):
        self.layerName = layerName
        self.renderSetupInstance = renderSetup.instance()
        self.layer = self.renderSetupInstance.createRenderLayer(self.layerName)
        
    def getListUptoFirstMeshNode(self,groupName):
        newList = []
        groupNodes = cmds.ls(groupName, dag=1)
        for node in groupNodes:
            newList.append(node)
            if cmds.nodeType(node) == 'mesh':
                break
            
        newList = str(groupName).strip("|").split("|")[:-1] + newList
        return ("".join(map((lambda node: '|'+ node), newList)))
        
    def createCollectionForAllLights(self):
        c_allLights = self.layer.createCollection("c_AllLights")
        c_allLights.getSelector().setFilterType(4)
        c_allLights.getSelector().setPattern("*")
        
    def createAllEnvirCollection(self):
        """create envir collection"""
        c_allEnvir = self.layer.createCollection("c_envirAllEnvir")
        c_allEnvir.getSelector().setFilterType(0)
        c_allEnvir.getSelector().setPattern("ENVIR*")
        return c_allEnvir
        
    def createAllCharCollection(self):
        """create char collection"""
        c_allChar = self.layer.createCollection("c_charAllChar")
        c_allChar.getSelector().setFilterType(0)
        c_allChar.getSelector().setPattern("CHAR*")
        return c_allChar
        
    def turnOffAllChar(self, isCutoutChecked):
        """create collection to turn off all chars"""
        
        if cmds.objExists("CHAR"):
            collection = self.createAllCharCollection()
            c_allCharShapes = collection.createCollection("c_allCharShapes")
            c_allCharShapes.getSelector().setFilterType(2)
            c_allCharShapes.getSelector().setPattern("*")
            o_charVisibility = c_allCharShapes.createOverride("CharVisibility", override.AbsOverride.kTypeId)
            if isCutoutChecked == True:
                o_charVisibility.finalize(self.getListUptoFirstMeshNode("CHAR")+".aiMatte")
                o_charVisibility.setAttrValue(1)
            else:
                o_charVisibility.finalize(self.getListUptoFirstMeshNode("CHAR")+".primaryVisibility")
                o_charVisibility.setAttrValue(0)
        
        
    def turnOffAllEnvir(self, isCutoutChecked):
        """create collection to turn off all envir"""
        if cmds.objExists("ENVIR"):
            collection = self.createAllEnvirCollection()
            c_allEnvirShapes = collection.createCollection("c_allEnvirShapes")
            c_allEnvirShapes.getSelector().setFilterType(2)
            c_allEnvirShapes.getSelector().setPattern("*")
            o_envirVisibility = c_allEnvirShapes.createOverride("EnvirVisibility", override.AbsOverride.kTypeId)
            if isCutoutChecked == True:
                o_envirVisibility.finalize(self.getListUptoFirstMeshNode("ENVIR")+".aiMatte")
                o_envirVisibility.setAttrValue(1)
            else:
                o_envirVisibility.finalize(self.getListUptoFirstMeshNode("ENVIR")+".primaryVisibility")
                o_envirVisibility.setAttrValue(0)
        
        
    def switchToLayer(self):
        """set render layer visible"""
        self.renderSetupInstance.switchToLayer(self.layer)
        
    def getTopParentOfSelectedNodes(nodes):
        return list(set(map(lambda node: str(node).strip("|").split("|")[0], nodes)))
        
class EnvirLayer(Layer):
    
    def __init__(self, layerName):
        super(EnvirLayer, self).__init__(layerName)
        
    def turnOffCharLights(self):
        """turn off char lights in envir"""
        c_offCharLights = self.layer.createCollection("c_OffCharLights")
        c_offCharLights.getSelector().setFilterType(4)
        c_offCharLights.getSelector().setPattern("LIGHTS_CHAR*")
        o_offCharLgtVisibility = c_offCharLights.createOverride("offCharLgtVisibility", override.AbsOverride.kTypeId)
        o_offCharLgtVisibility.finalize("LIGHTS_CHAR.visibility")
        o_offCharLgtVisibility.setAttrValue(0)
        
    def createCustomEnvirCollection(self, isCutoutChecked):
        """create custom envir collection"""
        c_customEnvir = self.layer.createCollection("c_envirCustomEnvir")
        c_customEnvir.getSelector().setFilterType(0)
        c_customEnvir.getSelector().setPattern((",").join(cmds.selectedNodes()))
        c_customEnvirShapes = c_customEnvir.createCollection("c_customEnvirShapes")
        c_customEnvirShapes.getSelector().setFilterType(2)
        c_customEnvirShapes.getSelector().setPattern("*")
        o_customEnvirVisibility = c_customEnvirShapes.createOverride("customEnvirVisibility", override.AbsOverride.kTypeId)
        
        if isCutoutChecked == True:
            o_customEnvirVisibility.finalize(self.getListUptoFirstMeshNode(cmds.selectedNodes()[0])+".aiMatte")
            o_customEnvirVisibility.setAttrValue(0)
        else:
            o_customEnvirVisibility.finalize(self.getListUptoFirstMeshNode(cmds.selectedNodes()[0])+".primaryVisibility")
            o_customEnvirVisibility.setAttrValue(1)

class CharLayer(Layer):
    
    def __init__(self, layerName):
        super(CharLayer, self).__init__(layerName)
        
    def turnOffEnvirLights(self):
        """turn off envir lights in char"""
        c_offEnvirLights = self.layer.createCollection("c_OffEnvirLights")
        c_offEnvirLights.getSelector().setFilterType(4)
        c_offEnvirLights.getSelector().setPattern("LIGHTS_ENVIR*")
        o_offEnvirLgtVisibility = c_offEnvirLights.createOverride("offEnvirLgtVisibility", override.AbsOverride.kTypeId)
        o_offEnvirLgtVisibility.finalize("LIGHTS_ENVIR.visibility")
        o_offEnvirLgtVisibility.setAttrValue(0)
        
    def createCustomCharCollection(self, isCutoutChecked):
        """create collection custom char collection"""
        c_customChar = self.layer.createCollection("c_customCharAllChar")
        c_customChar.getSelector().setFilterType(0)
        c_customChar.getSelector().setPattern((",").join(cmds.selectedNodes()))
        c_customCharShapes = c_customChar.createCollection("c_customCharShapes")
        c_customCharShapes.getSelector().setFilterType(2)
        c_customCharShapes.getSelector().setPattern("*")
        o_customCharVisibility = c_customCharShapes.createOverride("customCharVisibility", override.AbsOverride.kTypeId)
        
        if isCutoutChecked == True:
            o_customCharVisibility.finalize(self.getListUptoFirstMeshNode(cmds.selectedNodes()[0])+".aiMatte")
            o_customCharVisibility.setAttrValue(0)
        else:
            o_customCharVisibility.finalize(self.getListUptoFirstMeshNode(cmds.selectedNodes()[0])+".primaryVisibility")
            o_customCharVisibility.setAttrValue(1)
    
#Check for the parent in custom rig selection
#If the parent and selection type are different then through message.
#createEnvirLayer("ENVIR")
#createCharLayer("CHAR")
#createCustomEnvirLayer("Props")
#createCustomCharLayer("GIRL")
"""
def createEnvirLayer(layerName):
    layer = EnvirLayer(layerName)
    #layer.createCollectionForAllLights()
    layer.turnOffCharLights()
    layer.turnOffAllChar(False)
    layer.createAllEnvirCollection()
    layer.switchToLayer()
    
def createCharLayer(layerName):
    layer = CharLayer(layerName)
    #layer.createCollectionForAllLights()
    layer.turnOffEnvirLights()
    layer.turnOffAllEnvir(True)
    layer.createAllCharCollection()
    layer.switchToLayer()
    
def createCustomEnvirLayer(layerName, isCutoutChecked):
    layer = EnvirLayer(layerName)
    #layer.createCollectionForAllLights()
    layer.turnOffCharLights()
    
    #toggle only Envir cutout
    layer.turnOffAllEnvir(isCutoutChecked)
    
    layer.createCustomEnvirCollection(isCutoutChecked)
    layer.turnOffAllChar(False)
    layer.switchToLayer()
    
def createCustomCharLayer(layerName, isCutoutChecked):
    layer = CharLayer(layerName)
    #layer.createCollectionForAllLights()
    layer.turnOffEnvirLights()
    layer.turnOffAllEnvir(True)
    
    #toggle only Char cutout
    layer.turnOffAllChar(isCutoutChecked)
    
    layer.createCustomCharCollection(isCutoutChecked)
    layer.switchToLayer()

createEnvirLayer("ENVIR")
createCharLayer("CHAR")
createCustomEnvirLayer("TEST",False)
createCustomCharLayer("TEST2",False)
"""

"""
def createCustomCharLayer(layerName, isCutoutChecked):
    layer = CharLayer(layerName)
    layer.createCollectionForAllLights()
    layer.turnOffEnvirLights()
    layer.turnOffAllEnvir(True)
    
    #toggle only Char cutout
    layer.turnOffAllChar(isCutoutChecked)
    layer.createCustomCharCollection(isCutoutChecked)
    
    layer.switchToLayer()

createCustomCharLayer("TEST", True)
"""

"""
print cmds.selectedNodes()
nodes = map(lambda x: str(x), cmds.selectedNodes())
print nodes
pattern = (",").join(map(lambda x: x+"*", cmds.selectedNodes()))
print pattern


nodeName = str(node)
print type(nodeName)
print nodeName.replace("|","|")

print cmds.ls(node, dag=1, sn=1, showType=1)
print cmds.listRelatives(node, allParents=True)
"""


#print cmds.listRelatives(cmds.selectedNodes()[0], children=1)

"""
def getListUptoFirstMeshNode(groupName):
    newList = []
    groupNodes = cmds.ls(groupName, dag=1)
    print groupNodes
    for node in groupNodes:
        newList.append(node)
        if cmds.nodeType(node) == 'mesh':
            break
    
    newList = str(groupName).strip("|").split("|")[:-1] + newList   
    return ("".join(map((lambda node: '|'+ node), newList)))
    
print getListUptoFirstMeshNode("ENVIR")
"""