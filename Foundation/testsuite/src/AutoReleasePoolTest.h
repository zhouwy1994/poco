//
// AutoReleasePoolTest.h
//
// Definition of the AutoReleasePoolTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef AutoReleasePoolTest_INCLUDED
#define AutoReleasePoolTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class AutoReleasePoolTest: public Poco::CppUnit::TestCase
{
public:
	AutoReleasePoolTest(const std::string& name);
	~AutoReleasePoolTest();

	void testAutoReleasePool();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // AutoReleasePoolTest_INCLUDED
