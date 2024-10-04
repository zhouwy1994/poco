//
// HashTableTest.h
//
// Definition of the HashTableTest class.
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef HashTableTest_INCLUDED
#define HashTableTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class HashTableTest: public Poco::CppUnit::TestCase
{
public:
	HashTableTest(const std::string& name);
	~HashTableTest();

	void testInsert();
	void testOverflow();
	void testUpdate();
	void testSize();
	void testResize();
	void testStatistic();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // HashTableTest_INCLUDED
