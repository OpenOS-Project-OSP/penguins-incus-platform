set(LIB_SOURCES
    src/pipclient.cpp
    src/pipclient.h
    src/containersmodel.cpp
    src/containersmodel.h
    src/networksmodel.cpp
    src/networksmodel.h
    src/storagemodel.cpp
    src/storagemodel.h
    src/imagesmodel.cpp
    src/imagesmodel.h
    src/profilesmodel.cpp
    src/profilesmodel.h
    src/eventsource.cpp
    src/eventsource.h
    src/types.h
)

add_library(penguins-incus-qt SHARED ${LIB_SOURCES})

target_link_libraries(penguins-incus-qt
    PUBLIC
        Qt6::Core
        Qt6::DBus
        Qt6::Network
        Qt6::WebSockets
)

target_include_directories(penguins-incus-qt
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
        $<INSTALL_INTERFACE:include/penguins-incus-qt>
)

set_target_properties(penguins-incus-qt PROPERTIES
    VERSION   ${PROJECT_VERSION}
    SOVERSION 0
)

install(TARGETS penguins-incus-qt
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)
install(FILES
    src/pipclient.h
    src/containersmodel.h
    src/networksmodel.h
    src/storagemodel.h
    src/imagesmodel.h
    src/profilesmodel.h
    src/eventsource.h
    src/types.h
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/penguins-incus-qt
)
