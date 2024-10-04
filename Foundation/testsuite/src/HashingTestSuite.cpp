//
// HashingTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "HashingTestSuite.h"
#include "HashTableTest.h"
#include "SimpleHashTableTest.h"
#include "LinearHashTableTest.h"
#include "HashSetTest.h"
#include "HashMapTest.h"


Poco::CppUnit::Test* HashingTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("HashingTestSuite");

	pSuite->addTest(HashTableTest::suite());
	pSuite->addTest(SimpleHashTableTest::suite());
	pSuite->addTest(LinearHashTableTest::suite());
	pSuite->addTest(HashSetTest::suite());
	pSuite->addTest(HashMapTest::suite());

	return pSuite;
}
