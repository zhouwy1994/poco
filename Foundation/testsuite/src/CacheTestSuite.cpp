//
// CacheTestSuite.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "CacheTestSuite.h"
#include "LRUCacheTest.h"
#include "ExpireCacheTest.h"
#include "ExpireLRUCacheTest.h"
#include "UniqueExpireCacheTest.h"
#include "UniqueExpireLRUCacheTest.h"

Poco::CppUnit::Test* CacheTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("CacheTestSuite");

	pSuite->addTest(LRUCacheTest::suite());
	pSuite->addTest(ExpireCacheTest::suite());
	pSuite->addTest(UniqueExpireCacheTest::suite());
	pSuite->addTest(ExpireLRUCacheTest::suite());
	pSuite->addTest(UniqueExpireLRUCacheTest::suite());

	return pSuite;
}
