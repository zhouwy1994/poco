file(GLOB SRCS_G
    memory_pool.cpp
    binding_normalization.cpp
    demangle_type_name.cpp
    component.cpp
    fixed_size_allocator.cpp
    injector_storage.cpp
    normalized_component_storage.cpp
    normalized_component_storage_holder.cpp
    semistatic_map.cpp
    semistatic_graph.cpp)

POCO_SOURCES_AUTO(SRCS ${SRCS_G})

file(GLOB_RECURSE HDRS_G "../include/*.h"
                         "${CMAKE_CURRENT_BINARY_DIR}/../include/*.h")

POCO_HEADERS_AUTO(SRCS ${HDRS_G})

add_library(Fruit ${SRCS})
add_library(Poco::Fruit ALIAS Fruit)
set_target_properties(Fruit
	PROPERTIES
		VERSION ${SHARED_LIBRARY_VERSION} SOVERSION ${SHARED_LIBRARY_VERSION}
		OUTPUT_NAME PocoFruit
		DEFINE_SYMBOL Fruit_EXPORTS
)

if(BUILD_SHARED_LIBS)
    set_target_properties(Fruit PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif()

# target_include_directories(Fruit PUBLIC ${FRUIT_INCLUDE_DIRS})
target_compile_options(Fruit PUBLIC ${FRUIT_ADDITIONAL_COMPILE_FLAGS})

if(FRUIT_USES_BOOST)
    find_package(Boost REQUIRED)
    target_include_directories(Fruit PRIVATE ${Boost_INCLUDE_DIRS})
endif()

# target_include_directories(Fruit
# 	PUBLIC
# 		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
# 		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
# 	PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src
# )

target_include_directories(Fruit
	PUBLIC
		$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../include>
		$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/../include>
		$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
	PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# install(TARGETS fruit
#     RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
#     ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
#     LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}")
