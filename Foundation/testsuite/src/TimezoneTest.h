//
// TimezoneTest.h
//
// Definition of the TimezoneTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef TimezoneTest_INCLUDED
#define TimezoneTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class TimezoneTest: public Poco::CppUnit::TestCase
{
public:
	TimezoneTest(const std::string& name);
	~TimezoneTest();

	void testTimezone();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // TimezoneTest_INCLUDED
