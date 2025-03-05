cmake_minimum_required(VERSION 3.30)
project(deep_dive_course)

set(CMAKE_CXX_STANDARD 20)

file(GLOB SOURCES
    binary_tree/bst.c
    hash_tables/hash.c
    hash_tables/open_address.c
    hash_tables/main.c
#    fibonacci/fibonacci.c
)

add_executable(deep_dive_course
#        mini_bash/main.c
#        spinlock_mutex.c
#        main.c
#        fork_2.c
#        hash_tables/simple_table.c
#    binary_tree/bst.c
#        binary_tree/main.c
        ${SOURCES}
)
