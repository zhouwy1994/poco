//
// TestDecorator.h
//


#ifndef CppUnit_TestDecorator_INCLUDED
#define CppUnit_TestDecorator_INCLUDED


#include "Poco/CppUnit/CppUnit.h"
#include "Poco/CppUnit/Guards.h"
#include "Poco/CppUnit/Test.h"


namespace Poco {
namespace CppUnit {


class TestResult;


/*
 * A Decorator for Tests
 *
 * Does not assume ownership of the test it decorates
 *
 */
class CppUnit_API TestDecorator: public Test
{
	REFERENCEOBJECT(TestDecorator)

public:
	TestDecorator(Test* test);

	virtual ~TestDecorator();

	int countTestCases() const;

	void run(TestResult* result, const Test::Callback& callback = nullptr);

	std::string toString() const;

protected:
	Test* _test;
};


} // namespace CppUnit
} // namespace Poco


#endif // CppUnit_TestDecorator_INCLUDED
