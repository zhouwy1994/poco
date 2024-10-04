//
// StopwatchTest.h
//
// Definition of the StopwatchTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef StopwatchTest_INCLUDED
#define StopwatchTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class StopwatchTest: public Poco::CppUnit::TestCase
{
public:
	StopwatchTest(const std::string& name);
	~StopwatchTest();

	void testStopwatch();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // StopwatchTest_INCLUDED
