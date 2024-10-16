//
// ActivityTest.h
//
// Definition of the ActivityTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef ActivityTest_INCLUDED
#define ActivityTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class ActivityTest: public Poco::CppUnit::TestCase
{
public:
	ActivityTest(const std::string& name);
	~ActivityTest();

	void testActivity();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // ActivityTest_INCLUDED
