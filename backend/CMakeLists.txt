cmake_minimum_required(VERSION 3.12)
project(trading_engine)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find dependency packages
find_package(pybind11 REQUIRED)  # Python interface
find_package(spdlog REQUIRED)    # Logging
find_package(nlohmann_json REQUIRED)  # JSON processing
find_package(Boost REQUIRED COMPONENTS system)  # Boost

# Add header file paths
include_directories(${CMAKE_SOURCE_DIR}/include)

# Collect source files
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Create executable
add_executable(trading_engine ${SOURCES})

# Link dependency libraries
target_link_libraries(trading_engine
    PRIVATE
        pybind11::embed
        spdlog::spdlog
        nlohmann_json::nlohmann_json
        Boost::system
        pthread
)