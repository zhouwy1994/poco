//
// HTTPClientSessionTest.h
//
// Definition of the HTTPClientSessionTest class.
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef HTTPClientSessionTest_INCLUDED
#define HTTPClientSessionTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class HTTPClientSessionTest: public Poco::CppUnit::TestCase
{
public:
	HTTPClientSessionTest(const std::string& name);
	~HTTPClientSessionTest();

	void testGetSmall();
	void testGetLarge();
	void testHead();
	void testPostSmallIdentity();
	void testPostLargeIdentity();
	void testPostSmallChunked();
	void testPostLargeChunked();
	void testPostSmallClose();
	void testPostLargeClose();
	void testKeepAlive();
	void testTrailer();
	void testProxy();
	void testProxyAuth();
	void testBypassProxy();
	void testExpectContinue();
	void testExpectContinueFail();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // HTTPClientSessionTest_INCLUDED
