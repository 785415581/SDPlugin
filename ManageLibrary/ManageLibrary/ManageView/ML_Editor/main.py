#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2023/9/11 16:26
"""
import os
import sys
from pathlib import Path

libPath = os.path.dirname(os.path.dirname(__file__))
if libPath not in sys.path:
    sys.path.insert(0, libPath)

from PySide2.QtWidgets import QMainWindow, QWidget, QApplication
from ML_Editor.view import ViewWindow


def main():
    app = QApplication([])
    viewWindow = ViewWindow()
    viewWindow.show()
    app.exec_()


if __name__ == '__main__':
    main()