# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cc_gui.ui'
#
# Created: Tue Jan 07 15:27:30 2014
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4 import QtWebKit
import sys

sys.path.insert(0, './GUI files/Widgets')

from webView import WebView
from tableWidget import TableWidget
from listBox import ListBox
from loadBar import LoadBar
from logWidget import LogWidget

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_CC_GUI(object):
	def setupUi(self, CC_GUI):
		CC_GUI.setObjectName(_fromUtf8("CC_GUI"))
		CC_GUI.resize(712, 634)
		self.centralWidget = QtGui.QWidget(CC_GUI)
		self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
		self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.label_3 = QtGui.QLabel(self.centralWidget)
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.verticalLayout.addWidget(self.label_3)
		self.formLayout = QtGui.QFormLayout()
		self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
		self.formLayout.setObjectName(_fromUtf8("formLayout"))
		self.label = QtGui.QLabel(self.centralWidget)
		self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
		self.label.setObjectName(_fromUtf8("label"))
		self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
		self.lineEdit = QtGui.QLineEdit(self.centralWidget)
		self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
		self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lineEdit)
		self.label_2 = QtGui.QLabel(self.centralWidget)
		self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
		self.lineEdit_3 = QtGui.QLineEdit(self.centralWidget)
		self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
		self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_3)
		self.label_4 = QtGui.QLabel(self.centralWidget)
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.checkBox = QtGui.QCheckBox(self.centralWidget)
		self.checkBox.setText(_fromUtf8(""))
		self.checkBox.toggle()
		self.checkBox.setObjectName(_fromUtf8("checkBox"))
		self.horizontalLayout.addWidget(self.checkBox)
		spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem)
		self.formLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
		self.verticalLayout.addLayout(self.formLayout)
		self.midSection = QtGui.QHBoxLayout(self.centralWidget)
		self.loadBar = LoadBar()
		self.loadBar.setMinimum(0)
		self.pushButton_2 = QtGui.QPushButton(self.centralWidget)
		self.pushButton_2.setAutoDefault(True)
		self.loadBarLabel = QtGui.QLabel(self.centralWidget)
		self.loadBarLabel.setObjectName(_fromUtf8("loadBarLabel"))
		self.loadBarLabel.setText("        Task Progress:")
		self.midSection.addWidget(self.pushButton_2)
		self.midSection.addWidget(self.loadBarLabel)
		self.midSection.addWidget(self.loadBar)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
		self.pushButton_2.setSizePolicy(sizePolicy)
		self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
		self.verticalLayout.addLayout(self.midSection)
		self.line = QtGui.QFrame(self.centralWidget)
		self.line.setFrameShape(QtGui.QFrame.HLine)
		self.line.setFrameShadow(QtGui.QFrame.Sunken)
		self.line.setObjectName(_fromUtf8("line"))
		self.verticalLayout.addWidget(self.line)
		self.tableWidget = TableWidget(["Position", "Company", "Location", "Date"])
		self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
		self.logWidget = LogWidget()
		self.logWidget.setAutoFillBackground(False)
		self.logWidget.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 0); color: rgb(19, 243, 3)"))
		self.logWidget.setReadOnly(True)
		self.mainLayout = QtGui.QHBoxLayout(self.centralWidget)
		self.verticalLayout.addLayout(self.mainLayout)
		self.mainLayout.addWidget(self.tableWidget)
		self.mainStatus = QtGui.QVBoxLayout(self.centralWidget)
		self.mainStatus.addWidget(self.logWidget)
		self.mainLayout.addLayout(self.mainStatus)
		self.groupBox = QtGui.QGroupBox(self.centralWidget)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
		self.groupBox.setSizePolicy(sizePolicy)
		self.groupBox.setObjectName(_fromUtf8("groupBox"))
		self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox)
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.pushButton = QtGui.QPushButton(self.groupBox)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
		self.pushButton.setSizePolicy(sizePolicy)
		self.pushButton.setObjectName(_fromUtf8("pushButton"))
		self.horizontalLayout_2.addWidget(self.pushButton)
		spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem1)
		self.verticalLayout_3 = QtGui.QVBoxLayout()
		self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
		self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
		self.label_6 = QtGui.QLabel(self.groupBox)
		self.label_6.setObjectName(_fromUtf8("label_6"))
		self.horizontalLayout_3.addWidget(self.label_6)
		self.comboBox = ListBox()
		self.comboBox.loadFuncPointers({"getSelected": self.tableWidget.getRowNum, "setStyle":self.tableWidget.setCLStyle})
		self.tableWidget.loadFuncPointers({"setListBox": self.comboBox._setSelection, "loadStyles": self.comboBox.loadItems})
		self.comboBox.setObjectName(_fromUtf8("comboBox"))
		self.horizontalLayout_3.addWidget(self.comboBox)
		self.total_selected_rows = QtGui.QLabel(self.groupBox)
		self.total_selected_rows.setObjectName(_fromUtf8("total_selected_rows"))
		self.newStyleButton = QtGui.QPushButton(self.groupBox)
		self.newStyleButton.setObjectName(_fromUtf8("newStyleButton"))
		self.horizontalLayout_3.addWidget(self.newStyleButton)
		self.horizontalLayout_3.addWidget(self.total_selected_rows)
		self.verticalLayout_3.addLayout(self.horizontalLayout_3)
		self.horizontalLayout_2.addLayout(self.verticalLayout_3)
		spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_2.addItem(spacerItem2)
		self.pushButton_4 = QtGui.QPushButton(self.groupBox)
		self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
		self.horizontalLayout_2.addWidget(self.pushButton_4)
		self.verticalLayout.addWidget(self.groupBox)
		CC_GUI.setCentralWidget(self.centralWidget)
		self.mainToolBar = QtGui.QToolBar(CC_GUI)
		self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
		CC_GUI.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
		self.statusBar = QtGui.QStatusBar(CC_GUI)
		self.statusBar.setObjectName(_fromUtf8("statusBar"))
		CC_GUI.setStatusBar(self.statusBar)

		self.retranslateUi(CC_GUI)
		QtCore.QMetaObject.connectSlotsByName(CC_GUI)
		
	def retranslateUi(self, CC_GUI):
		CC_GUI.setWindowTitle(_translate("CC_GUI", "CC_GUI", None))
		self.label_3.setText(_translate("CC_GUI", "Enter search info below to crawl Monster.ca for jobs:", None))
		self.label.setText(_translate("CC_GUI", "Keywords:", None))
		self.label_2.setText(_translate("CC_GUI", "Location:", None))
		self.label_4.setText(_translate("CC_GUI", "Accumulate Results?", None))
		self.pushButton_2.setText(_translate("CC_GUI", "Crawl", None))
		self.groupBox.setTitle(_translate("CC_GUI", "Actions", None))
		self.pushButton.setText(_translate("CC_GUI", "Remove", None))
		self.label_6.setText(_translate("CC_GUI", "Cover Letter Style:", None))
		self.total_selected_rows.setText(_translate("CC_GUI", "       Total Selected Rows: --", None))
		self.pushButton_4.setText(_translate("CC_GUI", "Auto-Submit", None))
		self.newStyleButton.setText(_translate("CC_GUI", "New Style...", None))

