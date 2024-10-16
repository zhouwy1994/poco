//
// LocalDateTimeTest.h
//
// Definition of the LocalDateTimeTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef LocalDateTimeTest_INCLUDED
#define LocalDateTimeTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class LocalDateTimeTest: public Poco::CppUnit::TestCase
{
public:
	LocalDateTimeTest(const std::string& name);
	~LocalDateTimeTest();

	void testGregorian1();
	void testGregorian2();
	void testConversions();
	void testCalcs();
	void testAMPM();
	void testRelational1();
	void testRelational2();
	void testArithmetics1();
	void testArithmetics2();
	void testSwap();
	void testTimezone();
	void testTimezone2();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // LocalDateTimeTest_INCLUDED
