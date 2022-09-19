project( msgbuf-test)
cmake_minimum_required( VERSION 3.0 )

find_program(MSGBUFC msgbufc)
set(CMAKE_CXX_STANDARD 17)

message(STATUS "msgbufc: ${MSGBUFC}")

set(MSG_FILE ${CMAKE_SOURCE_DIR}/../msg/msg.yaml)
add_custom_command(OUTPUT A.hpp
    COMMAND ${MSGBUFC}  --in-file=${MSG_FILE}
    DEPENDS ${MSG_FILE}
    COMMENT "Generating code for ${MSG_FILE}."
)

add_executable( ${PROJECT_NAME} test.cc A.hpp)
