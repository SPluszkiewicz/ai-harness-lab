#pragma once

#include "calculator.hpp"

namespace calc {

// Thin wrapper used by the test driver. Call sites of RunExpression are
// distinct from call sites of Evaluate — that is intentional.
int RunExpression(std::string_view expression);

}  // namespace calc
