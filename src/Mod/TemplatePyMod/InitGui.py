# TemplatePyMod gui init module  
# (c) 2007 Juergen Riegel LGPL
#

import _TEMPLATEPY__rc
FreeCADGui.addLanguagePath(":/translations")
FreeCADGui.addIconPath(":/icons")
FreeCADGui.updateLocale()

class TemplatePyModWorkbench ( Workbench ):
	"Test workbench object"
	Icon = """
			/* XPM */
			static const char *test_icon[]={
			"16 16 2 1",
			"a c #000000",
			". c None",
			"................",
			"................",
			"..############..",
			"..############..",
			"..############..",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"......####......",
			"................",
			"................"};
			"""
	MenuText = FreeCAD.Qt.translate("Workbench", "Python sandbox")
	ToolTip = FreeCAD.Qt.translate("Workbench", "Python template workbench")
	
	def Initialize(self):
		import Commands

		self.appendToolbar("TemplateTools",["TemplatePyMod_Cmd1","TemplatePyMod_Cmd2","TemplatePyMod_Cmd3","TemplatePyMod_Cmd4","TemplatePyMod_Cmd5"])

		menu = [FreeCAD.Qt.translate("TemplateTools", "ModulePy &Commands"), FreeCAD.Qt.translate("TemplateTools", "PyModuleCommands")]
		list = ["TemplatePyMod_Cmd1","TemplatePyMod_Cmd2","TemplatePyMod_Cmd3","TemplatePyMod_Cmd5","TemplatePyMod_Cmd6"]
		self.appendCommandbar("PyModuleCommands",list)
		self.appendMenu(menu,list)

		Log ('Loading TemplatePyMod module... done\n')
	def Activated(self):
		Msg("TemplatePyModWorkbench::Activated()\n")
	def Deactivated(self):
		Msg("TemplatePyModWorkbench::Deactivated()\n")

Gui.addWorkbench(TemplatePyModWorkbench)
