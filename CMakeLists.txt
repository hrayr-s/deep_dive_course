cmake_minimum_required(VERSION 3.30)
project(deep_dive_course)

set(CMAKE_CXX_STANDARD 20)

file(GLOB SOURCES
    binary_tree/bst.c
)

add_executable(deep_dive_course
#        main.c
#        fork_2.c
#        hash_tables/simple_table.c
        ${SOURCES}
        binary_tree/main.c
)
