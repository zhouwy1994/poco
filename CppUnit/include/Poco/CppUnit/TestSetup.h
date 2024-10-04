//
// TestSetup.h
//


#ifndef CppUnit_TestSetup_INCLUDED
#define CppUnit_TestSetup_INCLUDED


#include "Poco/CppUnit/CppUnit.h"
#include "Poco/CppUnit/Guards.h"
#include "Poco/CppUnit/TestDecorator.h"


namespace Poco {
namespace CppUnit {


class Test;
class TestResult;


class CppUnit_API TestSetup: public TestDecorator
{
	REFERENCEOBJECT (TestSetup)

public:
	TestSetup(Test* test): TestDecorator(test)
	{
	}

	void run(TestResult* result);

protected:
	void setUp()
	{
	}

	void tearDown()
	{
	}
};


inline void TestSetup::run(TestResult* result)
{
	setUp();
	TestDecorator::run(result);
	tearDown();
}


} // namespace CppUnit
} // namespace Poco


#endif // CppUnit_TestSetup_INCLUDED
