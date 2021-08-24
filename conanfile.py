from conans import ConanFile, CMake, tools


CMAKE_PROJECT_STR = """project(
    UNITS
    LANGUAGES CXX
    VERSION 0.5.0
)"""


class UnitsConan(ConanFile):
    name = "LLNL-Units"
    version = "0.5.0-dev1"
    license = "BSD-3"
    url = "https://github.com/scipp/conan-llnl-units"
    homepage = "https://units.readthedocs.io"
    description = ("A run-time C++ library for working with units "
                   "of measurement and conversions between them "
                   "and with string representations of units "
                   "and measurements")
    topics = ("units", "dimensions", "quantities", "physical-units",
              "dimensional-analysis", "run-time")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "namespace": "ANY"}
    default_options = {"shared": False, "namespace": None}
    generators = "cmake"

    def source(self):
        git = tools.Git("units")
        git.clone("https://github.com/SimonHeybrock/units.git")

        tools.replace_in_file("units/CMakeLists.txt",
                              CMAKE_PROJECT_STR,
                              CMAKE_PROJECT_STR + """
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        units_namespace = self.options.get_safe("namespace")
        # The library uses C++14, but we want to set the namespace
        # to llnl::units which requires C++17.
        cmake.definitions["CMAKE_CXX_STANDARD"] = "17"
        if units_namespace:
            cmake.definitions["UNITS_NAMESPACE"] = units_namespace
        cmake.configure(source_folder="units")
        cmake.build(target="units")

    def package(self):
        self.copy("*.hpp", dst="include/units", src="units/units")
        self.copy("*units.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["units"]