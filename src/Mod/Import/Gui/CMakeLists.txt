# SPDX-License-Identifier: LGPL-2.1-or-later

include_directories(
    ${CMAKE_BINARY_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}
)

set(ImportGui_LIBS
    FreeCADGui
    PartGui
    Import
    ${OCC_OCAF_LIBRARIES}
    ${OCC_OCAF_DEBUG_LIBRARIES}
)

set (Import_TR_QRC ${CMAKE_CURRENT_BINARY_DIR}/Resources/Import_translation.qrc)
qt_find_and_add_translation(QM_SRCS "Resources/translations/*_*.ts"
    ${CMAKE_CURRENT_BINARY_DIR}/Resources/translations)
qt_create_resource_file(${Import_TR_QRC} ${QM_SRCS})
qt_add_resources(ImportResource_SRCS Resources/Import.qrc ${Import_TR_QRC})
PYSIDE_WRAP_RC(ImportResource_SRCS Resources/Import.qrc)
SOURCE_GROUP("Resources" FILES ${ImportResource_SRCS})

SET(ImportGui_SRCS
    AppImportGui.cpp
    AppImportGuiPy.cpp
    Command.cpp
    ExportOCAFGui.cpp
    ExportOCAFGui.h
    dxf/ImpExpDxfGui.cpp
    dxf/ImpExpDxfGui.h
    ImportOCAFGui.cpp
    ImportOCAFGui.h
    OCAFBrowser.cpp
    OCAFBrowser.h
#    PreCompiled.cpp
    PreCompiled.h
    Workbench.cpp
    Workbench.h
    ${ImportResource_SRCS}
)

add_library(ImportGui SHARED ${ImportGui_SRCS})

if(FREECAD_USE_PCH)
    target_precompile_headers(ImportGui PRIVATE
            $<$<COMPILE_LANGUAGE:CXX>:"${CMAKE_CURRENT_LIST_DIR}/PreCompiled.h">
    )
endif(FREECAD_USE_PCH)

target_include_directories(
    ImportGui
    PRIVATE
    ${CMAKE_BINARY_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(ImportGui ${ImportGui_LIBS})

if (MSVC)
    target_compile_options(ImportGui PRIVATE /wd4251)
endif()

if (FREECAD_WARN_ERROR)
    target_compile_warn_error(ImportGui)
endif()


SET_BIN_DIR(ImportGui ImportGui /Mod/Import)
SET_PYTHON_PREFIX_SUFFIX(ImportGui)

INSTALL(TARGETS ImportGui DESTINATION ${CMAKE_INSTALL_LIBDIR})
