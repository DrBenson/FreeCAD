
IF (BUILD_GUI)
    PYSIDE_WRAP_RC(_TEMPLATEPY__QRC_SRCS Resources/TemplatePyMod.qrc)
ENDIF (BUILD_GUI)

set(TemplatePyModScripts
    InitGui.py
    Init.py
    Commands.py
    PythonQt.py
    Tests.py
    DocumentObject.py
)

INSTALL(
    FILES
        ${TemplatePyModScripts}
        ${_TEMPLATEPY__QRC_SRCS}
    DESTINATION
        Mod/TemplatePyMod
)

INSTALL(
    FILES
        Init.py
        InitGui.py
        Commands.py
        FeaturePython.py
        PythonQt.py
        Tests.py
    DESTINATION
        Mod/TemplatePyMod
)
