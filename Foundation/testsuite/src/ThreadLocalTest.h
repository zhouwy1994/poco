//
// ThreadLocalTest.h
//
// Definition of the ThreadLocalTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef ThreadLocalTest_INCLUDED
#define ThreadLocalTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class ThreadLocalTest: public Poco::CppUnit::TestCase
{
public:
	ThreadLocalTest(const std::string& name);
	~ThreadLocalTest();

	void testLocality();
	void testAccessors();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // ThreadLocalTest_INCLUDED
