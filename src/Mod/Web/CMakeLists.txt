add_subdirectory(App)

set(Web_Scripts
    Init.py
)

if(BUILD_GUI)
    if(QtWebEngineWidgets_FOUND)
        add_subdirectory(Gui)
    endif()
    list (APPEND Web_Scripts InitGui.py)
    set(WebUI_libs
        WebGui.so
    )
endif(BUILD_GUI)

add_custom_target(WebScripts ALL
    SOURCES ${Web_Scripts}
)

fc_target_copy_resource_flat(WebScripts
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/Mod/Web
    ${Web_Scripts}
)

INSTALL(
    FILES
        ${Web_Scripts}
    DESTINATION
        Mod/Web
)
INSTALL(
    FILES
        ${WebUI_libs}
    DESTINATION
        ${CMAKE_INSTALL_LIBDIR}
)
