#include <iostream>

#include "units/units.hpp"

int main() {
  if (units::unit_from_string("m/s") != units::m / units::s) {
    std::cerr << "PACKAGE TEST FAILED\n";
    exit(1);
  }
}
