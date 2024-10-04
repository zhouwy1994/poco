//
// HTTPCredentialsTest.h
//
// Definition of the HTTPCredentialsTest class.
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef HTTPCredentialsTest_INCLUDED
#define HTTPCredentialsTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class HTTPCredentialsTest: public Poco::CppUnit::TestCase
{
public:
	HTTPCredentialsTest(const std::string& name);
	~HTTPCredentialsTest();

	void testBasicCredentials();
	void testProxyBasicCredentials();
	void testBadCredentials();
	void testAuthenticationParams();
	void testAuthenticationParamsMultipleHeaders();
	void testDigestCredentials();
	void testDigestCredentialsQoP();
	void testDigestCredentialsQoPSHA256();
	void testCredentialsBasic();
	void testProxyCredentialsBasic();
	void testCredentialsDigest();
	void testCredentialsDigestMultipleHeaders();
	void testProxyCredentialsDigest();
	void testExtractCredentials();
	void testVerifyAuthInfo();
	void testVerifyAuthInfoQoP();
	void testVerifyAuthInfoQoPSHA256();
	void testIsAlgorithmSupported();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // HTTPCredentialsTest_INCLUDED
