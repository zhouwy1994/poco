//
// UniqueExpireCacheTest.h
//
// Tests for ExpireCache
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//

#ifndef UniqueExpireCacheTest_INCLUDED
#define UniqueExpireCacheTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class UniqueExpireCacheTest: public Poco::CppUnit::TestCase
{
public:
	UniqueExpireCacheTest(const std::string& name);
	~UniqueExpireCacheTest();

	void testClear();
	void testAccessClear();
	void testDuplicateAdd();
	void testAccessDuplicateAdd();
	void testExpire0();
	void testAccessExpire0();
	void testExpireN();
	void testExpirationDecorator();
	void testAccessUpdate();

	void setUp();
	void tearDown();
	static Poco::CppUnit::Test* suite();
};


#endif // UniqueExpireCacheTest_INCLUDED
