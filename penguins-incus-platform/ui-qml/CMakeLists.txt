cmake_minimum_required(VERSION 3.22)
project(penguins-incus-platform VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

# Options
option(BUILD_LIB     "Build libpenguins-incus-qt D-Bus client library" ON)
option(BUILD_APP     "Build the QML desktop application"    ON)
option(BUILD_TESTS   "Build unit tests"                     OFF)

find_package(Qt6 REQUIRED COMPONENTS
    Core
    DBus
    Gui
    Network
    Qml
    Quick
    QuickControls2
    WebSockets
)

find_package(ECM QUIET)
if(ECM_FOUND)
    set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH})
    include(KDEInstallDirs)
    include(KDECMakeSettings)
    include(KDECompilerSettings NO_POLICY_SCOPE)
    find_package(KF6 QUIET COMPONENTS
        CoreAddons
        I18n
        Notifications
        WindowSystem
    )
endif()

if(BUILD_LIB)
    add_subdirectory(lib)
endif()

if(BUILD_APP)
    add_subdirectory(app)
endif()

if(BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()
