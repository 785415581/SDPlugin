#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Author: 785415581@qq.com
Date: 2023/9/12 15:54
"""

import json
import logging
from enum import Enum
from pathlib import Path
from typing import List, Optional, TypeVar

import sd
from PySide2 import QtGui, QtWidgets
from sd.api.qtforpythonuimgrwrapper import QtForPythonUIMgrWrapper
from sd.api.sbs.sdsbscompgraph import SDSBSCompGraph
from sd.api.sbs.sdsbsfunctiongraph import SDSBSFunctionGraph
from sd.api.sdapplication import SDApplication
from sd.api.sdgraph import SDGraph
from sd.api.sdgraphobject import SDGraphObject
from sd.api.sdnode import SDNode
from sd.api.sdpackage import SDPackage
from sd.api.sdpackagemgr import SDPackageMgr
from sd.context import Context as SDContext


from .ML_Editor.widget.ML_toolbar import MLToolbar

ML_Module = TypeVar("ML_Module")


class MLCore:
    def __init__(self):
        self.context = sd.getContext()
        self.logger = None
        self.log_handler = None
        self.application = self.context.getSDApplication()
        self.ui_mgr = self.application.getQtForPythonUIMgr()
        self.pkg_mgr = self.application.getPackageMgr()
        self.main_window = self.ui_mgr.getMainWindow()
        self.loaded_modules = []
        self.menu = None
        self.callback_ids = []

        self._max_toolbars = 3
        self._graph_view_ids = []
        self._graph_view_toolbar_list = dict()
        self._menu_object_name = "ML"
        self._menu_label = "ML Tool"

    @property
    def current_node_selection(self):
        return self.ui_mgr.getCurrentGraphSelectedNodes()

    @property
    def current_graph(self):
        return self.ui_mgr.getCurrentGraph()

    @property
    def current_package(self):
        return self.current_graph.getPackage()

    @property
    def current_graph_object_selection(self) -> List[SDGraphObject]:
        return self.ui_mgr.getCurrentGraphSelectedObjects()

    @property
    def current_graph_is_supported(self) -> bool:
        """
        Returns whether the graph is a support type for bw_tools.

        Some graph types in the designer API are not fully supported.
        We only support those which are fully functional.

        This property should be removed when the API is updated.
        """
        # Some graphs do not even return with the designer API
        if self.current_graph is None:
            return False

        return isinstance(self.current_graph, (SDSBSCompGraph, SDSBSFunctionGraph))

    @property
    def log(self) -> logging.RootLogger:
        return self.logger

    def get_graph_view_toolbar(self, graph_view_id: int) -> MLToolbar:
        try:
            toolbar = self._graph_view_toolbar_list[graph_view_id]
        except KeyError:
            toolbar = MLToolbar(self.main_window)
            icon = Path(__file__).parent / "ML_Editor/resource/icon/main.svg"
            self.ui_mgr.addToolbarToGraphView(
                graph_view_id,
                toolbar,
                icon=QtGui.QIcon(str(icon.resolve())),
                tooltip="ML Toolbar",
            )
            self._graph_view_toolbar_list[graph_view_id] = toolbar
            self._graph_view_ids.append(graph_view_id)

            # Maintain a limited number of toolbars since new ones
            # are continously created when the user switches graphs
            if len(self._graph_view_ids) == self._max_toolbars:
                id = self._graph_view_ids.pop(0)
                del self._graph_view_toolbar_list[id]

        return toolbar

    def initialize_logger(self):
        self.logger = logging.getLogger("ML tools")
        self.log_handler = sd.getContext().createRuntimeLogHandler()
        self.logger.propagate = False
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.DEBUG)

    def uninitialize_logger(self):
        self.logger.removeHandler(self.log_handler)
        self.log_handler = None

    def initialize(self, module: ML_Module) -> bool:
        """Initialize a module by calling the modules .on_initialize()"""
        if module.__name__ not in self.loaded_modules:
            try:
                module.on_initialize(self)
            except AttributeError:
                self.logger.warning(
                    f"Unable to initialize module {module.__name__}, "
                    f"on_initialize() has not been implemented correctly"
                )
                return False

            name = module.__name__.split(".")[-1]  # Strips module path and returns the name
            self.loaded_modules.append(name)
            self.logger.info(f"Initialized module {name}")
        return True

    def unload(self, module: ML_Module) -> bool:
        if module.__name__ not in self.loaded_modules:
            return False

        module.on_unload()
        self.loaded_modules.remove(module.__name__)

    def add_menu(self):
        self.logger.debug("Creating ML Tools menu...")
        self.menu = self.ui_mgr.newMenu(self._menu_label, self._menu_object_name)

    def remove_menu(self):
        self.ui_mgr.deleteMenu(self._menu_object_name)

    def unregister_callbacks(self):
        for callback in self.callback_ids:
            self.ui_mgr.unregisterCallback(callback)

    def register_on_graph_view_created_callback(self, func) -> int:
        graph_view_id = self.ui_mgr.registerGraphViewCreatedCallback(func)
        self.callback_ids.append(graph_view_id)
        return graph_view_id

    def remove_toolbars(self):
        for toolbar in self._graph_view_toolbar_list.values():
            toolbar.deleteLater()



