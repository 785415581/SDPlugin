#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2023/9/11 14:52
"""
import os
import sys
import json
from functools import partial
import shutil

DEBUG = False

libPath = os.path.dirname(os.path.dirname(__file__))
if libPath not in sys.path:
    sys.path.insert(0, libPath)

from PySide2.QtWidgets import (
    QApplication,
    QColorDialog,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QListWidgetItem,
    QFileDialog,
    QListView,
    QMessageBox
)

if DEBUG:
    from utils import create_app_data
    from utils import editConfig
else:
    from .utils import create_app_data
    from .utils import editConfig
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Slot, Signal, Qt
from PySide2.QtGui import QStandardItem, QStandardItemModel


class ViewWindow(QDialog):

    def __init__(self, parent=None):
        super(ViewWindow, self).__init__(parent)
        self.setParent(parent)
        # self.mainWidget = QWidget()
        # self.setupUi(self)
        self.ui = QUiLoader().load(os.path.join(os.path.dirname(__file__), "widget/main_.ui"))
        self.setModal(False)
        self.resize(960, 610)
        self.vlay = QVBoxLayout()
        self.vlay.addWidget(self.ui)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlay)

        self.currentProjectName = None
        self.currentProjectRoot = None
        self.createProjectName = None
        self.config_file = None

        self.ProjItemModel = QStandardItemModel()
        self.ui.Lv_Projects.setModel(self.ProjItemModel)

        self.LibPathModel = QStandardItemModel()
        self.ui.Lv_LibPath.setModel(self.LibPathModel)
        self.ui.Lv_LibPath.setSelectionMode(QListView.SingleSelection)
        # init var
        self.AddProjectDialog = AddProjectDialog(self)
        self.MangeProjectsDialog = MangeProjectsDialog(self)
        self.initConnectSignal()
        self.preInitConfig()

    def preInitConfig(self):
        self.ProjItemModel.clear()
        self.LibPathModel.clear()
        origin_data = self.get_config_data()
        for projName, projData in origin_data.items():
            isInstall = projData.get("Install")
            if isInstall:
                Item = QStandardItem()
                Item.setText(projName)
                Item.setData(projName, role=Qt.UserRole)
                self.ProjItemModel.appendRow(Item)

    def get_config_data(self):
        config_file = create_app_data.create_config()
        with open(config_file, 'r') as fp:
            origin_data = json.load(fp)
        return origin_data

    def initConnectSignal(self):
        self.ui.Btn_Projects.clicked.connect(self.on_Btn_Projects)
        self.ui.Btn_addProject.clicked.connect(self.on_Btn_addProject)
        self.ui.Btn_deleteProject.clicked.connect(self.on_Btn_deleteProject)
        self.ui.Lv_Projects.clicked.connect(self.on_Project_listView_Clicked)
        self.ui.Lv_LibPath.doubleClicked.connect(self.on_Lv_LibPath_doubleClicked)
        self.ui.Btn_BrowserRoot.clicked.connect(self.on_Btn_BrowserRoot)
        self.ui.Btn_deleteWatchPath.clicked.connect(self.on_Btn_deleteWatchPath)
        self.ui.Btn_addWatchPath.clicked.connect(self.on_Btn_addWatchPath)
        self.ui.Btn_Search.clicked.connect(self.on_Btn_Search)
        self.ui.Btn_apply.clicked.connect(self.on_Btn_apply)

    def on_Btn_apply(self):
        m_AppDataPath = os.environ.get('LOCALAPPDATA')
        designer_config_path = os.path.join(m_AppDataPath, "Adobe/Adobe Substance 3D Designer").replace("\\", "/")
        default_configuration = os.path.join(m_AppDataPath, "Adobe/Adobe Substance 3D Designer/default_configuration.sbscfg").replace("\\", "/")
        user_ML_config = os.path.join(designer_config_path, "ML_Config.sbsprj")
        template_config = os.path.dirname(os.path.dirname(__file__)) + "/ML_Config.sbsprj"
        if not os.path.isfile(user_ML_config):
            shutil.copy(template_config, user_ML_config)
        config_data = self.get_config_data()
        libSet = list()
        for project, projectData in config_data.items():
            if projectData.get("Install"):
                for i in projectData.get("SearchPath"):
                    if i.replace("\\", "/") not in libSet:
                        libSet.append(i.replace("\\", "/"))
        isTrueInit = editConfig.initSbsprj(user_ML_config)
        if isTrueInit:
            isTrueEdit = editConfig.addSbsPrj(user_ML_config, libSet)
            if isTrueEdit:
                editConfig.modifyUserConfig(default_configuration, user_ML_config)

    @Slot()
    def on_Btn_deleteWatchPath(self):
        selected_indexes = self.ui.Lv_LibPath.selectedIndexes()
        if selected_indexes:
            selected_items = [self.LibPathModel.itemFromIndex(index) for index in selected_indexes]
            for item in selected_items:
                self.addOrDeleteConfigWatchPath(item.text())

        selected_index = self.ui.Lv_LibPath.selectionModel().currentIndex()
        if selected_index:
            row = selected_index.row()
            self.LibPathModel.removeRow(row)

    @Slot()
    def on_Btn_addWatchPath(self):
        watchPath = QFileDialog.getExistingDirectory(self, 'select folder', "D:/Dev/Assets/SD")
        if not watchPath:
            return
        if self.LibPathModel.findItems(watchPath):
            return
        else:
            watchPath = watchPath.replace("\\", "/")
            Item = QStandardItem()
            Item.setText(watchPath)
            Item.setData(watchPath, role=Qt.UserRole)
            self.LibPathModel.appendRow(Item)
            self.addOrDeleteConfigWatchPath(watchPath)

    def addOrDeleteConfigWatchPath(self, watchPath):
        config_file = create_app_data.create_config()
        config_data = self.get_config_data()
        watchPathList = config_data.get(self.currentProjectName)["SearchPath"]
        if watchPath in watchPathList:
            watchPathList.remove(watchPath)
            config_data.get(self.currentProjectName)["SearchPath"] = watchPathList
        with open(config_file, 'w+') as fp:
            new_data = json.dumps(config_data, indent=4, ensure_ascii=False)
            fp.write(new_data)
            fp.close()

    def updateWatchPathList(self, watchPathList):
        config_file = create_app_data.create_config()
        origin_data = self.get_config_data()
        if self.currentProjectName in origin_data.keys():
            origin_data[self.currentProjectName]["SearchPath"] = watchPathList
        with open(config_file, 'w+') as fp:
            new_data = json.dumps(origin_data, indent=4, ensure_ascii=False)
            fp.write(new_data)
            fp.close()

    @Slot()
    def on_Btn_deleteProject(self):
        self.LibPathModel.clear()
        config_data = self.get_config_data()
        config_data.pop(self.currentProjectName)
        config_file = create_app_data.create_config()
        with open(config_file, 'w+') as fp:
            new_data = json.dumps(config_data, indent=4, ensure_ascii=False)
            fp.write(new_data)
            fp.close()
        selected_index = self.ui.Lv_Projects.selectionModel().currentIndex()
        if selected_index:
            row = selected_index.row()
            self.ProjItemModel.removeRow(row)

    @Slot()
    def on_Btn_Search(self):
        print(self.currentProjectName)
        if self.currentProjectRoot:
            self.LibPathModel.clear()
            recursive_path = self.recursive_lib()
            self.updateWatchPathList(recursive_path)
            for path in recursive_path:
                Item = QStandardItem()
                Item.setText(path)
                Item.setData(path, role=Qt.UserRole)
                self.LibPathModel.appendRow(Item)

    @Slot()
    def on_Lv_LibPath_doubleClicked(self, index):
        os.startfile(index.data())

    @Slot()
    def on_Btn_BrowserRoot(self):
        print("Root Browser...")
        ProjectRoot = QFileDialog.getExistingDirectory(self, 'select folder', "D:/Dev/Assets/SD")
        if not ProjectRoot:
            return
        self.currentProjectRoot = ProjectRoot
        self.ui.Line_ProjRoot.setText(ProjectRoot)
        self.updateProjectRootConfig(ProjectRoot)

    @Slot()
    def on_Project_listView_Clicked(self, index):
        self.LibPathModel.clear()
        self.currentProjectName = index.data()
        origin_data = self.get_config_data()
        PerforceServer = origin_data[self.currentProjectName]["PerforceServer"]
        projectRoot = origin_data[self.currentProjectName]["ProjectRoot"]
        self.currentProjectRoot = projectRoot
        self.ui.Line_Server.setText(PerforceServer)
        self.ui.Line_ProjRoot.setText(projectRoot)
        # 初始化扫面路径

        self.rebuildLvPathListView()

        print(self.currentProjectName)

    def rebuildLvPathListView(self):
        self.LibPathModel.clear()
        config_data = self.get_config_data()
        watchPathList = config_data.get(self.currentProjectName)["SearchPath"]
        if watchPathList:
            for watchPath in watchPathList:
                Item = QStandardItem()
                Item.setText(watchPath)
                Item.setData(watchPath, role=Qt.UserRole)
                self.LibPathModel.appendRow(Item)

    @Slot(str)
    def on_Btn_Projects(self):
        print("Projects Btn Clicked...")
        # init var
        self.MangeProjectsDialog = MangeProjectsDialog(self)
        self.MangeProjectsDialog.show()
        # self.MangeProjectsDialog.exec_()  # 使用 exec_() 方法显示子窗口，是模态的
        self.MangeProjectsDialog.SettingProjects.connect(self.updateProject)

    def updateProject(self):
        print("preInitConfig...")
        self.preInitConfig()

    @Slot(str)
    def on_Btn_addProject(self, value):
        print("Add Projects Btn Clicked...")
        # init var
        self.AddProjectDialog = AddProjectDialog(self)
        self.AddProjectDialog.show()  # 使用 exec_() 方法显示子窗口，是模态的
        self.AddProjectDialog.S_returnProject.connect(self.on_addProject_dialog)

    def on_addProject_dialog(self, value):
        self.createProjectName = value
        self.add_project_to_listView(self.createProjectName)
        print("createProjectName = {}".format(value))

    def recursive_lib(self):
        recursive_path = []
        self.recursiveFile(self.currentProjectRoot, recursive_path)
        return recursive_path

    def recursiveFile(self, directory, all_lib=[]):
        childDirs = os.listdir(directory)
        for child in childDirs:
            childPath = os.path.join(directory, child)
            if os.path.isdir(childPath):
                self.recursiveFile(childPath, all_lib)
            else:
                if childPath.endswith(".sbs"):
                    all_lib.append(directory)
                    break

    def add_project_to_listView(self, projName):

        Item = QStandardItem()
        Item.setText(projName)
        Item.setData(projName, role=Qt.UserRole)
        self.ProjItemModel.appendRow(Item)
        self.initConfig(projName)

    def updateProjectRootConfig(self, projectRoot):
        config_file = create_app_data.create_config()
        origin_data = self.get_config_data()
        if self.currentProjectName in origin_data.keys():
            origin_data[self.currentProjectName]["ProjectRoot"] = projectRoot
        with open(config_file, 'w+') as fp:
            new_data = json.dumps(origin_data, indent=4, ensure_ascii=False)
            fp.write(new_data)
            fp.close()

    def initConfig(self, projName):
        AppDataFolder = create_app_data.create_file_folder()
        config_file = create_app_data.create_config()
        print("config_file = {}".format(config_file))
        data = {
            projName: {
                "projName": projName,
                "PerforceServer": "10.0.201.12:1666",
                "ProjectRoot": "",
                "Install": True,
                "SearchPath": []
            }
        }
        with open(config_file, 'r') as fp:
            origin_data = json.load(fp)
            if projName not in origin_data.keys():
                origin_data[projName] = data.get(projName)
            with open(config_file, 'w+') as fp:
                new_data = json.dumps(origin_data, indent=4, ensure_ascii=False)
                fp.write(new_data)
                fp.close()

    def closeEvent(self, event) -> None:
        print("Main Window Closed...")
        if self.AddProjectDialog.isWindow():
            self.AddProjectDialog.close()
            print('close AddProjectDialog...')
        if self.MangeProjectsDialog.isWindow():
            self.MangeProjectsDialog.close()
            print('close MangeProjectsDialog...')


class AddProjectDialog(QDialog):
    S_returnProject = Signal(str)

    def __init__(self, parent=None):
        super(AddProjectDialog, self).__init__(parent)

        self.ProjectName = None

        self.ui = QUiLoader().load(os.path.join(os.path.dirname(__file__), "widget/AddProjectDialog.ui"))

        self.setModal(False)
        self.resize(330, 120)
        self.vlay = QVBoxLayout()
        self.vlay.addWidget(self.ui)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlay)

        self.ui.Btn_Cancel.clicked.connect(self.close)
        self.ui.Btn_Ok.clicked.connect(self.getProjectName)

    def getProjectName(self, value):
        self.ProjectName = self.ui.Line_ProjectName.text()
        if self.ProjectName:
            # self.S_returnProject.emit(self.ProjectName)
            self.S_returnProject.emit(self.ProjectName)
            self.ui.Line_ProjectName.clear()
            self.close()

    def getMainFormSignal(self, value):
        print("getMainFormSignal = {}".format(value))

    def closeEvent(self, event) -> None:
        print(event)


class MangeProjectsDialog(QDialog):
    SettingProjects = Signal()

    def __init__(self, parent=None):
        super(MangeProjectsDialog, self).__init__(parent)
        self.origin_data = None
        self.config_file = create_app_data.create_config()
        with open(self.config_file, 'r') as fp:
            self.origin_data = json.load(fp)
        self.ui = QUiLoader().load(os.path.join(os.path.dirname(__file__), "widget/projectSetting.ui"))

        self.setModal(False)
        self.resize(630, 470)
        self.vlay = QVBoxLayout()
        self.vlay.addWidget(self.ui)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlay)

        self.rebuildUI()

    def rebuildUI(self):
        index = 0
        for project in self.origin_data.keys():
            label = QLabel(project)
            if self.origin_data.get(project)["Install"]:
                btn_install = QPushButton("Remove")
            else:
                btn_install = QPushButton("Install")
            btn_install.clicked.connect(partial(self.InstallLab, btn_install, project))
            hLay = QHBoxLayout()
            hLay.addWidget(label)
            hLay.addWidget(btn_install)
            self.ui.verticalLayout_4.insertLayout(0, hLay)
            index += 1

    def InstallLab(self, btn_install, project):
        if btn_install.text() == "Install":
            btn_install.setText("Remove")
            self.origin_data.get(project)['Install'] = True
            print(self.origin_data.get(project))
        elif btn_install.text() == "Remove":
            btn_install.setText("Install")
            self.origin_data.get(project)['Install'] = False
            print(self.origin_data.get(project))

    def closeEvent(self, event) -> None:
        self.callBackConfig()

    def callBackConfig(self):
        with open(self.config_file, 'w+') as fp:
            new_data = json.dumps(self.origin_data, indent=4, ensure_ascii=False)
            fp.write(new_data)
            fp.close()
        self.SettingProjects.emit()


if __name__ == '__main__':
    app = QApplication()
    ml_editor_dialog = ViewWindow()
    ml_editor_dialog.show()
    sys.exit(app.exec_())
