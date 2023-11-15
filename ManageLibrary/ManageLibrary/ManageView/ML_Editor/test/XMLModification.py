#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2023/9/20 10:34
"""

import xml.etree.ElementTree as ElementTree
import os


##Example Python script for changing Substance 3D Designer user preference file##

def SetConfigurationFile(p_ConfigPath):
    # Check is the path passed as parameter exists.
    if (os.path.isfile(p_ConfigPath)):
        # replace backslashes by forwardslahes to ensure consistency
        p_ConfigPath = p_ConfigPath.replace("\\", "/")
        # get Local Appadata path from Environment variables, construct full path to user_preferences.xml and check if it exists.
        m_AppDataPath = os.environ.get('LOCALAPPDATA')
        if m_AppDataPath != None:
            m_UserPrefsPath = os.path.join(m_AppDataPath, str("Adobe/Adobe Substance 3D Designer/user_preferences.xml"))
            if (os.path.isfile(m_UserPrefsPath)):
                # read XML elementtree from file, find correct element until we get to the actual line that defines
                # the configruation file path
                m_PrefsTree = ElementTree.parse(m_UserPrefsPath)
                m_PrefsRoot = m_PrefsTree.getroot()
                m_PrefsElement = m_PrefsRoot.find("preferences")
                m_XMLError = True
                if (m_PrefsElement != None):
                    m_ConfigElement = m_PrefsElement.find("configuration")
                    if m_ConfigElement != None:
                        m_ConfigFileElement = m_ConfigElement.find("configurationfile")
                        if (m_ConfigFileElement != None):
                            m_XMLError = False
                            # Check if path is already set, to avoid double work
                            if m_ConfigFileElement.text.replace("file:///", "") == p_ConfigPath:
                                print("configurationfile is already set to desired path. Aborting.")
                                return True
                            else:
                                # construct correctly formatted path, insert into elementtree
                                m_ConfigPath = str("file:///" + p_ConfigPath)
                                m_ConfigFileElement.text = m_ConfigPath
                                # Write to file
                                m_XMLString = str("<?xml version="1.0" encoding="UTF - 8"?>n") + ElementTree.tostring(m_PrefsRoot, 'utf-8')
                                m_File = open(m_UserPrefsPath, 'w')
                                m_File.write(m_XMLString)
                                m_File.close()
                                print("configuration file path successfully changed!")
                                return True
                if m_XMLError:
                    # if this flag was not set to false, we can assume something was missing or went wrong when walking through the XML
                    print("Error: malformed content in user_preferences.xml!")
                    return False
            else:
                print("Error: user_preferences.xml does not exist, try starting Substance 3D Designer first!")
                return False
        else:
            print("Error: LocalAppData path returned None")
            return False
    else:
        print("Error: Invalid Configuration File path!")
        return False