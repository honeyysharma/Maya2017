from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2 import QtWidgets, QtCore
from RLManager import RLManager
import maya.cmds as cmds

class CustomDialog(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    def __init__(self, parent, RLManager):
        super(CustomDialog, self).__init__(parent=parent)
        self.RLManager = RLManager
        self.generateUI()
        
    def generateUI(self):
        self.lblLayerName = QtWidgets.QLabel('Layer Name:')
        
        self.leLayerName = QtWidgets.QLineEdit()
        self.leLayerName.setPlaceholderText("Layer")
        
        self.lblLayerType = QtWidgets.QLabel('Layer Type:')
        
        self.comboLayerType = QtWidgets.QComboBox()
        self.comboLayerType.addItems(['          - SELECT -', 'ENVIR', 'CHAR'])
        
        self.cutOutCheckBox = QtWidgets.QCheckBox("With Holdouts")
        self.cutOutCheckBox.setChecked(False)
        
        self.btnAddLayer = QtWidgets.QPushButton('Add Layer', self)
        self.btnAddLayer.clicked.connect(self.createCustomLayer)
        
        #grid layout for adding custom widgets
        self.customLayerGridLayout = QtWidgets.QGridLayout()
        self.customLayerGridLayout.addWidget(self.lblLayerName, 0, 0)
        self.customLayerGridLayout.addWidget(self.leLayerName, 0, 1)
        self.customLayerGridLayout.addWidget(self.lblLayerType, 1, 0)
        self.customLayerGridLayout.addWidget(self.comboLayerType, 1, 1)
        self.customLayerGridLayout.addWidget(self.cutOutCheckBox, 2, 0)
        self.customLayerGridLayout.addWidget(self.btnAddLayer, 2, 1)
        
        self.setLayout(self.customLayerGridLayout)
            
    def createCustomLayer(self):
        if cmds.selectedNodes() is None:
            QtWidgets.QMessageBox.information(self, "Alert", "Please select assets in the Outliner!")    
        else:
            layerType = str(self.comboLayerType.currentText())
            layerName = str(self.leLayerName.text()).upper()
            parentList = list(set(map(lambda node: str(node).strip("|").split("|")[0], cmds.selectedNodes())))
            
            if layerType == "ENVIR":
                if "CHAR" in parentList:
                    QtWidgets.QMessageBox.information(self, "Alert", "CHAR type asset selected to create ENVIR layer!")
                else:
                    self.RLManager.createCustomEnvirLayer(layerName, self.cutOutCheckBox.isChecked())
            else:
                if "ENVIR" in parentList:
                    QtWidgets.QMessageBox.information(self, "Alert", "ENVIR type asset selected to create ENVIR layer!")
                else:
                    self.RLManager.createCustomCharLayer(layerName, self.cutOutCheckBox.isChecked())
        

class RLSetup(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RLSetup, self).__init__(parent=parent)
        self.setMinimumSize(QtCore.QSize(450, 200))
        self.showCustomLayer = 0
        self.RLManager = RLManager()
        self.customLayer = CustomDialog(self, self.RLManager)
        self.toggleAnimation()
        self.initUI()
        
    def initUI(self):
        #main layout
        vbox = QtWidgets.QVBoxLayout()
        
        #top frame
        defaultGroupBox = QtWidgets.QGroupBox()
        #defaultGroupBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        defaultGroupBox.setTitle("Default")
        defaultGroupBox.setStyleSheet("QGroupBox { background-color: rgb(50, 50, 50); border:1px solid rgb(0, 0, 0); }")
        
        #bottom frame
        customGroupBox = QtWidgets.QGroupBox()
        #customGroupBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        customGroupBox.setTitle("Custom")
        customGroupBox.setStyleSheet("QGroupBox { background-color: rgb(50, 50, 50); border:1px solid rgb(0, 0, 0); }")

        #split window and add frame
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(defaultGroupBox)
        splitter.addWidget(customGroupBox)
        
        #add splitter to main layout
        vbox.addWidget(splitter)
        
        #create default layer buttons
        self.btnEnvir = QtWidgets.QPushButton('ADD ALL ENVIR LAYER', self)
        self.btnEnvir.clicked.connect(self.createEnvirLayer)
        
        self.btnChar = QtWidgets.QPushButton('ADD ALL CHAR LAYER', self)
        self.btnChar.clicked.connect(self.createCharLayer)
        
        self.btnCustom = QtWidgets.QPushButton('ADD MORE LAYERS', self)
        self.btnCustom.clicked.connect(self.toggleAnimation)
        
        #create grid layout to add buttons
        defaultBtnGridLayout = QtWidgets.QGridLayout()
        defaultBtnGridLayout.addWidget(self.btnEnvir, 0, 0)
        defaultBtnGridLayout.addWidget(self.btnChar, 1, 0)
        
        #set grid layout for top frame
        defaultGroupBox.setLayout(defaultBtnGridLayout)
        

        #vertical layout for bottom frame
        vboxCustom = QtWidgets.QVBoxLayout()
        vboxCustom.addStretch(1)
        vboxCustom.addWidget(self.btnCustom)
        vboxCustom.addStretch(1)
        vboxCustom.addWidget(self.customLayer)
        
        #set vertical layout for bottom frame
        customGroupBox.setLayout(vboxCustom)
        
        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle('Render Layer Setup')
        self.show()
        
    def toggleAnimation(self):
        self.animation = QtCore.QPropertyAnimation(self.customLayer, "maximumHeight")
        
        if self.showCustomLayer == 0:
            self.animation.setDuration(300)
            self.animation.setStartValue(100)
            self.animation.setEndValue(0)
            self.animation.start()
            self.showCustomLayer = 1
        else:
            self.animation.setDuration(200)
            self.animation.setStartValue(0)
            self.animation.setEndValue(100)
            self.animation.start()
            self.showCustomLayer = 0
   
    def createEnvirLayer(self):
        self.RLManager.createEnvirLayer("ENVIR")
        
    def createCharLayer(self):
        self.RLManager.createCharLayer("CHAR")
        
test = RLSetup()
