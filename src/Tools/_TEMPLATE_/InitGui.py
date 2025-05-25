# _TEMPLATE_ gui init module
# (c) 2001 Juergen Riegel LGPL

import _TEMPLATE_Gui
FreeCADGui.addLanguagePath(":/translations")
FreeCADGui.addIconPath(":/icons")
FreeCADGui.updateLocale()

class _TEMPLATE_Workbench(Workbench):
    "_TEMPLATE_ workbench object"

    MenuText = FreeCAD.Qt.translate("Workbench", "_TEMPLATE_")
    ToolTip = FreeCAD.Qt.translate("Workbench", "_TEMPLATE_ workbench")

    def Initialize(self):
        # load the module
        import _TEMPLATE_Gui

    def GetClassName(self):
        return "_TEMPLATE_Gui::Workbench"


Gui.addWorkbench(_TEMPLATE_Workbench())
