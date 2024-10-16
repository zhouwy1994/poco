//
// RWLockTest.h
//
// Definition of the RWLockTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef RWLockTest_INCLUDED
#define RWLockTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class RWLockTest: public Poco::CppUnit::TestCase
{
public:
	RWLockTest(const std::string& name);
	~RWLockTest();

	void testLock();
	void testTryLock();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // RWLockTest_INCLUDED
