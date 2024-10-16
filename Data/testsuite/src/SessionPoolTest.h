//
// SessionPoolTest.h
//
// Definition of the SessionPoolTest class.
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef SessionPoolTest_INCLUDED
#define SessionPoolTest_INCLUDED


#include "Poco/Data/Data.h"
#include "Poco/CppUnit/TestCase.h"


class SessionPoolTest: public Poco::CppUnit::TestCase
{
public:
	SessionPoolTest(const std::string& name);
	~SessionPoolTest();

	void testSessionPool();
	void testSessionPoolContainer();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // SessionPoolTest_INCLUDED
