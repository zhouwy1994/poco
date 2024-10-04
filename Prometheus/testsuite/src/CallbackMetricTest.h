//
// CallbackMetricTest.h
//
// Definition of the CallbackMetricTest class.
//
// Copyright (c) 2022, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef CallbackMetricTest_INCLUDED
#define CallbackMetricTest_INCLUDED


#include "Poco/CppUnit/TestCase.h"


class CallbackMetricTest: public Poco::CppUnit::TestCase
{
public:
	CallbackMetricTest(const std::string& name);
	~CallbackMetricTest() = default;

	void testExport();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();
};


#endif // CallbackMetricTest_INCLUDED
