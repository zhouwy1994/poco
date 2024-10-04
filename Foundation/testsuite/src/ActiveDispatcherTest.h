//
// ActiveDispatcherTest.h
//
// Definition of the ActiveDispatcherTest class.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef ActiveDispatcherTest_INCLUDED
#define ActiveDispatcherTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class ActiveDispatcherTest: public Poco::CppUnit::TestCase
{
public:
	ActiveDispatcherTest(const std::string& name);
	~ActiveDispatcherTest();

	void testWait();
	void testWaitInterval();
	void testTryWait();
	void testFailure();
	void testVoid();
	void testVoidIn();
	void testVoidInOut();
	void testActiveDispatcher();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // ActiveDispatcherTest_INCLUDED
