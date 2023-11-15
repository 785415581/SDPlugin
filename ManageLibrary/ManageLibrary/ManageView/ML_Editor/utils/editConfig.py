#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2023/9/22 16:23
"""
import xml.etree.ElementTree as ET


def addSbsPrj(sbsconfig, listSet):
    try:
        lens = len(listSet)
        tree = ET.parse(sbsconfig)
        root = tree.getroot()
        m_PrefsElement = root.find("preferences")
        m_libraryElement = m_PrefsElement.find("library")
        m_watchedpathsElement = m_libraryElement.find("watchedpaths")
        m_sizeElement = m_watchedpathsElement.find("size")
        m_sizeElement.text = str(lens)

        for i in range(lens, 0, -1):
            libElement = ET.SubElement(m_watchedpathsElement, "_{}".format(str(i)))
            libElement.set("prefix", "_")
            libElement.text = ""
            subUrlElement = ET.SubElement(libElement, "url")
            subUrlElement.text = "file:///{}".format(listSet[i - 1])
            subIsrecursiveElement = ET.SubElement(libElement, "isrecursive")
            subIsrecursiveElement.text = "false"

            subIsenabledElement = ET.SubElement(libElement, "isenabled")
            subIsenabledElement.text = "true"

            subExcludepatternElement = ET.SubElement(libElement, "excludepattern")
            subExcludepatternElement.text = ""

            subExcludefilterElement = ET.SubElement(libElement, "excludefilter")
            subExcludefilterElement.text = ""
        tree.write(sbsconfig, encoding='utf-8')
        return True
    except:
        return False


def initSbsprj(sbsconfig):
    try:
        tree = ET.parse(sbsconfig)
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
                        grandChildElement = childElement.find(grandChildElement.tag)
                        childElement.remove(grandChildElement)
                m_watchedpathsElement.remove(childElement)
        tree.write(sbsconfig, encoding='utf-8')
        return True
    except:
        return False


def modifyUserConfig(sbsconfig, user_ML_config):
    try:
        tree = ET.parse(sbsconfig)
        root = tree.getroot()
        m_ProjectElement = root.find("projects")
        m_ProjectFilesElement = m_ProjectElement.find("projectfiles")
        m_sizeElement = m_ProjectFilesElement.find("size")
        configSize = int(m_sizeElement.text)
        if configSize > 0:
            for i in range(configSize, 0, -1):
                m_prefixElement = m_ProjectElement.find("_{}".format(str(i)))
                m_pathElement = m_prefixElement.find("path")
                if m_pathElement.text ==user_ML_config:
                    return True
        configSize += 1
        m_sizeElement.text = str(configSize)
        libElement = ET.SubElement(m_ProjectFilesElement, "_{}".format(str(configSize)))
        libElement.text = user_ML_config
        tree.write(sbsconfig, encoding='utf-8')
        return True
    except:
        return False

user_ML_config = "D:/toolset/SubstanceDesigner/Tools/ManageLibrary/ManageLibrary/ManageView/ML_Config.sbsprj"
sbsconfig = r'C:\Users\jiaxin.qin\AppData\Local\Adobe\Adobe Substance 3D Designer\default_configuration.sbscfg'

modifyUserConfig(sbsconfig, user_ML_config)