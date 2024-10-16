//
// DigestEngineTest.h
//
// Definition of the DigestEngineTest class.
//
// Copyright (c) 2012, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef DigestEngineTest_INCLUDED
#define DigestEngineTest_INCLUDED


#include "Poco/Crypto/Crypto.h"
#include "Poco/CppUnit/TestCase.h"


class DigestEngineTest: public Poco::CppUnit::TestCase
{
public:
	DigestEngineTest(const std::string& name);
	~DigestEngineTest();

	void testMD5();
	void testSHA1();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // DigestEngineTest_INCLUDED
