#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2023/9/12 15:51
"""
import os
import json

try:
    print('222')
except RuntimeError:
    print("RunTime Error")

else:
    print("333")

# projName = "maiShelf11"
#
# data = {
#     projName: {
#         "projName": projName,
#         "PerforceServer": "",
#         "ProjectRoot": ""
#     }
# }
#
# config_file = "D:/config.json"
# if not os.path.isfile(config_file):
#     fp = open(config_file, 'w')
#     fp.write("{}")
#     fp.close()
# with open(config_file, 'r') as fp:
#     origin_data = json.load(fp)
#     if projName not in origin_data.keys():
#         origin_data[projName] = data.get(projName)
#     with open(config_file, 'w+') as fp:
#         new_data = json.dumps(origin_data, indent=4, ensure_ascii=False)
#         fp.write(new_data)
#         fp.close()

# dic = "D:/Dev/Assets/SD/Content/SD_Filis"


# def recursiveFile(directory, all_lib=[]):
#     childDirs = os.listdir(directory)
#     for child in childDirs:
#         childPath = os.path.join(directory, child)
#         if os.path.isdir(childPath):
#             recursiveFile(childPath, all_lib)
#         else:
#             if childPath.endswith(".sbs"):
#                 all_lib.append(directory)
#                 break
#
# all_lib = []
# recursiveFile(dic, all_lib)
# print(all_lib)

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

"""
<size>2</size>
<_2 prefix="_">
    <url>file:///D:/Dev/Assets/SD/Content/SD_Filis/Common/Surfaces</url>
    <isrecursive>false</isrecursive>
    <isenabled>true</isenabled>
    <excludepattern></excludepattern>
    <excludefilter></excludefilter>
</_2>
<_1 prefix="_">
    <url>file:///D:/Dev/Assets/SD/Content/SD_Filis/Common</url>
    <isrecursive>false</isrecursive>
    <isenabled>true</isenabled>
    <excludepattern></excludepattern>
    <excludefilter></excludefilter>
</_1>


"""



def addSbsPrj():
    sbsprjPath = r"D:/toolset/SubstanceDesigner/Tools/ManageLibrary/ManageLibrary/ManageView/ML_Config.sbsprj"
    tree = ET.parse(sbsprjPath)
    root = tree.getroot()
    m_PrefsElement = root.find("preferences")
    m_libraryElement = m_PrefsElement.find("library")
    m_watchedpathsElement = m_libraryElement.find("watchedpaths")
    m_sizeElement = m_watchedpathsElement.find("size")
    m_sizeElement.text = "3"

    for i in range(3, 0, -1):
        libElement = ET.SubElement(m_watchedpathsElement, "_{}".format(str(i)))
        libElement.set("prefix", "_")
        libElement.text = ""
        subUrlElement = ET.SubElement(libElement, "url")
        subUrlElement.text = "file:///D:/file_{}".format(str(i))
        subIsrecursiveElement = ET.SubElement(libElement, "isrecursive")
        subIsrecursiveElement.text = "false"

        subIsenabledElement = ET.SubElement(libElement, "isenabled")
        subIsenabledElement.text = "true"

        subExcludepatternElement = ET.SubElement(libElement, "excludepattern")
        subExcludepatternElement.text = ""

        subExcludefilterElement = ET.SubElement(libElement, "excludefilter")
        subExcludefilterElement.text = ""

    tree.write(sbsprjPath, encoding='utf-8')


def deleteSbsprj():
    sbsprjPath = r"D:/toolset/SubstanceDesigner/Tools/ManageLibrary/ManageLibrary/ManageView/ML_Config.sbsprj"
    tree = ET.parse(sbsprjPath)
    root = tree.getroot()
    m_PrefsElement = root.find("preferences")
    m_libraryElement = m_PrefsElement.find("library")
    m_watchedpathsElement = m_libraryElement.find("watchedpaths")
    m_sizeElement = m_watchedpathsElement.find("size")
    m_sizeElement.text = "0"
    for child in m_watchedpathsElement.getchildren():
        if child.tag == "size":
            continue
        if child.tag == "watchedpaths":
            continue
        childElement = m_watchedpathsElement.find(child.tag)
        if childElement is not None:
            for grandChild in childElement.getchildren():
                grandChildElement = childElement.find(grandChild.tag)
                if grandChildElement is not None:
                    # print(grandChildElement.tag)
                    grandChildElement = childElement.find(grandChildElement.tag)
                    childElement.remove(grandChildElement)
            m_watchedpathsElement.remove(childElement)

    tree.write(sbsprjPath, encoding='utf-8')


m_AppDataPath = os.environ.get('LOCALAPPDATA')
default_configuration = os.path.join(m_AppDataPath, "Adobe/Adobe Substance 3D Designer/default_configuration.sbscfg").replace("\\", "/")

# addSbsPrj()
# deleteSbsprj()
template_config = os.path.dirname(__file__)
print(os.device_encoding())