//
// PatternFormatterTest.h
//
// Definition of the PatternFormatterTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef PatternFormatterTest_INCLUDED
#define PatternFormatterTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class PatternFormatterTest: public Poco::CppUnit::TestCase
{
public:
	PatternFormatterTest(const std::string& name);
	~PatternFormatterTest();

	void testPatternFormatter();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // PatternFormatterTest_INCLUDED
