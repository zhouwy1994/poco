//
// TCPServerTest.h
//
// Definition of the TCPServerTest class.
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef TCPServerTest_INCLUDED
#define TCPServerTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class TCPServerTest: public Poco::CppUnit::TestCase
{
public:
	TCPServerTest(const std::string& name);
	~TCPServerTest();

	void testOneConnection();
	void testTwoConnections();
	void testMultiConnections();
	void testReuseSocket();
	void testReuseSession();
	void testContextInvalidCertificateHandler();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // TCPServerTest_INCLUDED
