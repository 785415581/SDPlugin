# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(597, 517)
        Dialog.setStyleSheet(u"/* Widget -----------------------------------------*/\n"
"QWidget {\n"
"	background-color: #2b2b2b;\n"
"    outline: 0px;\n"
"}\n"
"\n"
"/* Tree -----------------------------------------*/\n"
"\n"
"QTreeView {\n"
"	background-color: #333333;\n"
"    outline: 0px;\n"
"    border: 1px solid rgb(117, 118, 118);\n"
"}\n"
"\n"
"QTreeView::item {\n"
"    color:#d4d4d4;\n"
"	/*background-color: #323232;*/\n"
"	height:30px;\n"
"\n"
"}\n"
"\n"
"QTreeView::item:selected {\n"
"    background-color: #5285a6;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    font: 10pt \"Consolas\";\n"
"    height:25px;\n"
"    color:#FFFFFF;\n"
"    background:#5285a6;\n"
"    border-left:0px solid gray;\n"
"    border-right:1px solid gray;\n"
"    border-top:0px solid gray;\n"
"    border-bottom:0px solid gray;\n"
"}\n"
"/* LsitView -----------------------------------------*/\n"
"QListView {\n"
"	background-color: #333333;\n"
"    outline: 0px;\n"
"    border: 1px solid rgb(117, 118, 118);\n"
"}\n"
"\n"
"/* Label ----------------------------"
                        "-------------*/\n"
"QLabel {\n"
"	color: #c8c8c8;\n"
"	font: 11pt \"Consolas\";\n"
"}\n"
"\n"
"/* LineEdit -----------------------------------------*/\n"
"QLineEdit {\n"
"    border-radius: 5px;\n"
"    border: 1px solid rgb(117, 118, 118);\n"
"    background-color: #36393f;\n"
"\n"
"}\n"
"\n"
"\n"
"/* QPushButton -----------------------------------------*/\n"
"QPushButton{\n"
"	color: #c8c8c8;\n"
"    font: 11pt \"Consolas\";\n"
"    border-radius: 5px;\n"
"    border: 1px solid rgb(117, 118, 118);\n"
"    background-color: #2d2d2d;\n"
"    background-repeat: no-repeat;\n"
"    background-position: left center;\n"
"}\n"
"QPushButton:hover { background-color: #262626; border-style: solid; border-radius: 5px; }\n"
"QPushButton:pressed { background-color: #262626; border-style: solid; border-radius: 5px; }\n"
"\n"
"\n"
"QMenuBar{\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QStatusBar{\n"
"    color: #ffffff;\n"
"}")
        self.verticalLayout_4 = QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.splitter = QSplitter(self.widget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton = QPushButton(self.layoutWidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"")

        self.verticalLayout.addWidget(self.pushButton)

        self.listView = QListView(self.layoutWidget)
        self.listView.setObjectName(u"listView")

        self.verticalLayout.addWidget(self.listView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_3 = QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_2 = QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pushButton_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget_2 = QWidget(self.splitter)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.pushButton_4 = QPushButton(self.layoutWidget_2)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.pushButton_4)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.layoutWidget_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(self.layoutWidget_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.layoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.layoutWidget_2)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.pushButton_5 = QPushButton(self.layoutWidget_2)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setStyleSheet(u"")

        self.gridLayout.addWidget(self.pushButton_5, 1, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.pushButton_6 = QPushButton(self.layoutWidget_2)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.pushButton_6)

        self.listView_2 = QListView(self.layoutWidget_2)
        self.listView_2.setObjectName(u"listView_2")

        self.verticalLayout_2.addWidget(self.listView_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButton_7 = QPushButton(self.layoutWidget_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.layoutWidget_2)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.pushButton_8)

        self.pushButton_9 = QPushButton(self.layoutWidget_2)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.pushButton_9)

        self.horizontalLayout_5.setStretch(0, 3)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.splitter.addWidget(self.layoutWidget_2)
        self.treeView = QTreeView(self.splitter)
        self.treeView.setObjectName(u"treeView")
        self.splitter.addWidget(self.treeView)

        self.verticalLayout_3.addWidget(self.splitter)


        self.verticalLayout_4.addWidget(self.widget)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Projects", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"+", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"Settings", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"PerforceServer", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"ProjectRoot", None))
        self.pushButton_5.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.pushButton_6.setText(QCoreApplication.translate("Dialog", u"WatchedPaths", None))
        self.pushButton_7.setText(QCoreApplication.translate("Dialog", u"Auto Search", None))
        self.pushButton_8.setText(QCoreApplication.translate("Dialog", u"-", None))
        self.pushButton_9.setText(QCoreApplication.translate("Dialog", u"+", None))
    # retranslateUi

