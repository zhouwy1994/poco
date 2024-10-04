//
// TestFailure.cpp
//


#include "Poco/CppUnit/TestFailure.h"
#include "Poco/CppUnit/Test.h"


namespace Poco {
namespace CppUnit {


// Returns a short description of the failure.
std::string TestFailure::toString()
{
	return _failedTest->toString () + ": " + _thrownException->what();
}


} // namespace CppUnit
} // namespace Poco
