if (APPLE)
    find_library(IOKIT_LIBRARY IOKit)
    find_library(FOUNDATION_LIBRARY Foundation)
endif ()

# Sources
file(GLOB SRCS_G "src/SerialPort.cc")

if (APPLE)
    # If OSX
    list(APPEND SRCS_G src/impl/unix.cc)
    list(APPEND SRCS_G src/impl/list_ports/list_ports_osx.cc)
elseif (UNIX)
    # If unix
    list(APPEND SRCS_G src/impl/unix.cc)
    list(APPEND SRCS_G src/impl/list_ports/list_ports_linux.cc)
else ()
    # If windows
    list(APPEND SRCS_G src/impl/win.cc)
    list(APPEND SRCS_G src/impl/list_ports/list_ports_win.cc)
endif ()

POCO_SOURCES_AUTO(SRCS ${SRCS_G})

# Headers
file(GLOB_RECURSE HDRS_G "include/*.h")
POCO_HEADERS_AUTO(SRCS ${HDRS_G})

# # Version Resource
# if(MSVC AND BUILD_SHARED_LIBS)
# 	source_group("Resources" FILES ${PROJECT_SOURCE_DIR}/DLLVersion.rc)
# 	list(APPEND SRCS ${PROJECT_SOURCE_DIR}/DLLVersion.rc)
# endif()

add_library(SerialPort ${SRCS})
add_library(Poco::SerialPort ALIAS SerialPort)
set_target_properties(SerialPort
	PROPERTIES
		VERSION ${SHARED_LIBRARY_VERSION} SOVERSION ${SHARED_LIBRARY_VERSION}
		OUTPUT_NAME PocoSerialPort
		DEFINE_SYMBOL SerialPort_EXPORTS
)

if (APPLE)
  target_link_libraries(SerialPort ${FOUNDATION_LIBRARY} ${IOKIT_LIBRARY})
elseif(UNIX AND NOT ANDROID)
  target_link_libraries(SerialPort rt pthread)
elseif(ANDROID)
  target_link_libraries(SerialPort)
else ()
    target_link_libraries(SerialPort setupapi)
endif ()

target_include_directories(SerialPort
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
	PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src
)

POCO_INSTALL(SerialPort)
POCO_GENERATE_PACKAGE(SerialPort)

add_subdirectory(samples)
if(ENABLE_TESTS)
	add_subdirectory(samples)
	# add_subdirectory(testsuite)
endif()

