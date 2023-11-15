#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2023/9/18 17:13
"""
import os


def create_file_folder():
    app_data_folder = os.getenv("LOCALAPPDATA")
    AppDataFolder = os.path.join(app_data_folder, "ManageLibrary_DS")
    if not os.path.exists(AppDataFolder):
        os.mkdir(AppDataFolder)
    return AppDataFolder


def create_config():
    AppDataFolder = create_file_folder()
    config_file = os.path.join(AppDataFolder, "config.json")
    if not os.path.isfile(config_file):
        fp = open(config_file, 'w')
        fp.write("{}")
        fp.close()
    return config_file

