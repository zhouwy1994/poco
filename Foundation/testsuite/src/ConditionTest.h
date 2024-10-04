//
// ConditionTest.h
//
// Definition of the ConditionTest class.
//
// Copyright (c) 2007, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef ConditionTest_INCLUDED
#define ConditionTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class ConditionTest: public Poco::CppUnit::TestCase
{
public:
	ConditionTest(const std::string& name);
	~ConditionTest();

	void testSignal();
	void testBroadcast();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // ConditionTest_INCLUDED
