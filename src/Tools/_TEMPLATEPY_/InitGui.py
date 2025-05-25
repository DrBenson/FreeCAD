# -*- coding: utf-8 -*-
# _TEMPLATEPY_ gui init module
# (c) 2001 Juergen Riegel
# License LGPL

import _TEMPLATEPY__rc
import _TEMPLATEPY_Gui
FreeCADGui.addLanguagePath(":/translations")
FreeCADGui.addIconPath(":/icons")
FreeCADGui.updateLocale()

class _TEMPLATEPY_Workbench(Workbench):
    "_TEMPLATEPY_ workbench object"
    Icon = FreeCAD.getResourceDir() + "Mod/_TEMPLATEPY_/Resources/icons/_TEMPLATEPY_Workbench.svg"
    MenuText = FreeCAD.Qt.translate("Workbench", "_TEMPLATEPY_")
    ToolTip = FreeCAD.Qt.translate("Workbench", "_TEMPLATEPY_ workbench")

    def Initialize(self):
        # load the module
        import _TEMPLATEPY_Gui

        self.appendToolbar(FreeCAD.Qt.translate("Workbench", "_TEMPLATEPY_"), ["_TEMPLATEPY__HelloWorld"])
        self.appendMenu(FreeCAD.Qt.translate("Workbench", "_TEMPLATEPY_"), ["_TEMPLATEPY__HelloWorld"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"


Gui.addWorkbench(_TEMPLATEPY_Workbench())
