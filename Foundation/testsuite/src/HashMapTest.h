//
// HashMapTest.h
//
// Definition of the HashMapTest class.
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef HashMapTest_INCLUDED
#define HashMapTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class HashMapTest: public Poco::CppUnit::TestCase
{
public:
	HashMapTest(const std::string& name);
	~HashMapTest();

	void testInsert();
	void testErase();
	void testIterator();
	void testConstIterator();
	void testIndex();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // HashMapTest_INCLUDED
