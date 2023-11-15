#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2023/9/12 16:36
"""

import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Dict
from PySide2.QtWidgets import QVBoxLayout, QWidget, QDialog
libPath = os.path.dirname(os.path.dirname(__file__))
if libPath not in sys.path:
    sys.path.insert(0, libPath)

from PySide2.QtWidgets import QMainWindow, QWidget, QApplication

from .view import ViewWindow


def open_ML_Editor(MLCore):
    MLCore.log.info("Opening ML Editor window")
    # dock = MLCore.ui_mgr.newDockWidget(identifier="sample.test.dock", title="New Dock")
    ml_editor_dialog = ViewWindow(MLCore.main_window)
    ml_editor_dialog.show()


def on_initialize(MLCore):
    action = MLCore.menu.addAction("Open ML Editor")
    action.triggered.connect(lambda: open_ML_Editor(MLCore))

