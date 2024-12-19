cmake_minimum_required(VERSION 3.10)

project(prague LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall -Wextra -O3 -fPIC")

# include(GNUInstallDirs)

# install(TARGETS libprague
#     LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
#     PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})


# Add source files
add_library(prague SHARED
prague_wrapper.cpp
)

# Add header files
target_include_directories(prague PUBLIC
  ${CMAKE_CURRENT_SOURCE_DIR}
)

# Add executable targets
add_executable(udp_prague_receiver udp_prague_receiver.cpp)
target_link_libraries(udp_prague_receiver prague)

add_executable(udp_prague_sender udp_prague_sender.cpp)
target_link_libraries(udp_prague_sender prague)

# Add dependency for shared library
target_link_libraries(prague)

# Install targets
install(TARGETS udp_prague_receiver udp_prague_sender DESTINATION bin)
install(TARGETS prague DESTINATION lib)

# Clean target
# add_custom_target(clean
#   COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_BINARY_DIR}/CMakeFiles
#   COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_BINARY_DIR}/lib
#   COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_BINARY_DIR}/bin
# )