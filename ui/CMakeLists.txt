cmake_minimum_required(VERSION 3.20)

# --- Qt Configuration ---
find_package(Qt6 COMPONENTS Widgets Core Gui Network QUIET)
if(NOT Qt6_FOUND)
    find_package(Qt5 COMPONENTS Widgets Core Gui Network QUIET)
endif()

if(NOT Qt6_FOUND AND NOT Qt5_FOUND)
    message(STATUS "Qt not found - skipping UI build")
    return()
endif()

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

# --- VisionCast UI Executable ---
# Explicitly list Q_OBJECT headers so that AUTOMOC discovers and processes them.
# AUTOMOC only scans headers in the same directory as listed sources; since our
# headers live in include/visioncast_ui/ (not src/), they must be added here.
set(UI_HEADERS
    include/visioncast_ui/main_window.h
    include/visioncast_ui/preview_panel.h
    include/visioncast_ui/overlay_editor.h
    include/visioncast_ui/talent_manager.h
    include/visioncast_ui/output_config.h
    include/visioncast_ui/monitoring_panel.h
    include/visioncast_ui/control_room.h
    include/visioncast_ui/design_panel.h
    include/visioncast_ui/recognition_panel.h
    include/visioncast_ui/device_scanner.h
    include/visioncast_ui/license_manager.h
    include/visioncast_ui/license_dialog.h
    include/visioncast_ui/python_launcher.h
)

set(UI_SOURCES
    src/main.cpp
    src/main_window.cpp
    src/preview_panel.cpp
    src/overlay_editor.cpp
    src/talent_manager.cpp
    src/output_config.cpp
    src/monitoring_panel.cpp
    src/control_room.cpp
    src/design_panel.cpp
    src/recognition_panel.cpp
    src/device_scanner.cpp
    src/license_manager.cpp
    src/license_dialog.cpp
    src/license_config.cpp
    src/license_secure_logger.cpp
    src/license_storage.cpp
    src/python_launcher.cpp
    ${UI_HEADERS}
)

# --- Windows: embed icon into the executable via .rc (only if the .ico exists) ---
if(WIN32)
    set(_ico_file ${CMAKE_SOURCE_DIR}/packaging/icons/visioncast.ico)
    set(_rc_file  ${CMAKE_SOURCE_DIR}/packaging/icons/visioncast.rc)
    if(EXISTS ${_ico_file} AND EXISTS ${_rc_file})
        list(APPEND UI_SOURCES ${_rc_file})
    else()
        message(STATUS "VisionCast UI: visioncast.ico not found — skipping icon embedding "
                       "(generate it from packaging/icons/visioncast.svg; see packaging/icons/README.md)")
    endif()
endif()

add_executable(visioncast_ui ${UI_SOURCES})

# --- macOS: attach .icns to the application bundle ---
if(APPLE)
    set(APP_ICON_MACOS ${CMAKE_SOURCE_DIR}/packaging/icons/visioncast.icns)
    if(EXISTS ${APP_ICON_MACOS})
        set_source_files_properties(${APP_ICON_MACOS} PROPERTIES MACOSX_PACKAGE_LOCATION "Resources")
        target_sources(visioncast_ui PRIVATE ${APP_ICON_MACOS})
    endif()
    set_target_properties(visioncast_ui PROPERTIES
        MACOSX_BUNDLE TRUE
        MACOSX_BUNDLE_ICON_FILE visioncast.icns
    )
endif()

target_include_directories(visioncast_ui
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
        ${CMAKE_SOURCE_DIR}/sdk/include
)

if(Qt6_FOUND)
    target_link_libraries(visioncast_ui PRIVATE
        Qt6::Widgets Qt6::Core Qt6::Gui Qt6::Network
        visioncast_engine_lib
        visioncast_sdk
    )
else()
    target_link_libraries(visioncast_ui PRIVATE
        Qt5::Widgets Qt5::Core Qt5::Gui Qt5::Network
        visioncast_engine_lib
        visioncast_sdk
    )
endif()

# --- License API defaults (can be overridden at build time) ---
# Usage: cmake -DVISIONCAST_LICENSE_API_URL="https://..." -DVISIONCAST_LICENSE_API_KEY="..."
if(DEFINED VISIONCAST_LICENSE_API_URL)
    target_compile_definitions(visioncast_ui PRIVATE
        VISIONCAST_LICENSE_API_URL="${VISIONCAST_LICENSE_API_URL}")
endif()
if(DEFINED VISIONCAST_LICENSE_API_KEY)
    target_compile_definitions(visioncast_ui PRIVATE
        VISIONCAST_LICENSE_API_KEY="${VISIONCAST_LICENSE_API_KEY}")
endif()

# --- Install Rules ---
if(APPLE)
    install(TARGETS visioncast_ui
        BUNDLE DESTINATION .
    )
else()
    install(TARGETS visioncast_ui
        RUNTIME DESTINATION bin
    )
endif()
