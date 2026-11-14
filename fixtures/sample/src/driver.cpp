#include "driver.hpp"

namespace calc {

int RunExpression(std::string_view expression) {
    return Evaluate(expression);
}

}  // namespace calc
