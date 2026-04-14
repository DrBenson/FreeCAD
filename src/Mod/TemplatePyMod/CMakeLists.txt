
IF (BUILD_GUI)
    set (TemplatePyMod_TR_QRC ${CMAKE_CURRENT_BINARY_DIR}/Resources/TemplatePyMod_translation.qrc)
    qt_find_and_add_translation(QM_SRCS "Resources/translations/*_*.ts"
        ${CMAKE_CURRENT_BINARY_DIR}/Resources/translations)
    qt_create_resource_file(${TemplatePyMod_TR_QRC} ${QM_SRCS})
    qt_add_resources(TemplatePyMod_QRC_SRCS Resources/TemplatePyMod.qrc ${TemplatePyMod_TR_QRC})

    PYSIDE_WRAP_RC(TemplatePyMod_QRC_SRCS Resources/TemplatePyMod.qrc)
    SOURCE_GROUP("Resources" FILES ${TemplatePyMod_QRC_SRCS})
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
        ${TemplatePyMod_QRC_SRCS}
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
