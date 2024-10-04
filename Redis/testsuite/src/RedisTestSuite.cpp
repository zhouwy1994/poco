//
// RedisTestSuite.cpp
//
// Copyright (c) 2015, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "RedisTestSuite.h"
#include "RedisTest.h"


Poco::CppUnit::Test* RedisTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("RedisTestSuite");

	pSuite->addTest(RedisTest::suite());

	return pSuite;
}
