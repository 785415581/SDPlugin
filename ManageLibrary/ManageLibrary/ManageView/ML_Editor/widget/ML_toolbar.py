#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2023/9/12 15:55
"""
from PySide2.QtWidgets import QAction, QToolBar


class MLToolbar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.uid = self.__class__.__name__
        self.objectName = self.uid
        self._actions = dict()

    def add_action(self, id: str, action: QAction):
        if id in self._actions:
            return
        self.addAction(action)
        self._actions[id] = action
