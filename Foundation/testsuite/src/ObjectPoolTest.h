//
// ObjectPoolTest.h
//
// Definition of the ObjectPoolTest class.
//
// Copyright (c) 2010-2012, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef ObjectPoolTest_INCLUDED
#define ObjectPoolTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class ObjectPoolTest: public Poco::CppUnit::TestCase
{
public:
	ObjectPoolTest(const std::string& name);
	~ObjectPoolTest();

	void testObjectPool();
	void testObjectPoolWaitOnBorrowObject();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // ObjectPoolTest_INCLUDED
