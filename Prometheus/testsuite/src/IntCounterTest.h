//
// IntCounterTest.h
//
// Definition of the IntCounterTest class.
//
// Copyright (c) 2022, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef IntCounterTest_INCLUDED
#define IntCounterTest_INCLUDED


#include "Poco/CppUnit/TestCase.h"


class IntCounterTest: public Poco::CppUnit::TestCase
{
public:
	IntCounterTest(const std::string& name);
	~IntCounterTest() = default;

	void testBasicBehavior();
	void testExport();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();
};


#endif // IntCounterTest_INCLUDED
