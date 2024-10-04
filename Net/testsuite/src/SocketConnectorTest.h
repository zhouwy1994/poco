//
// SocketConnectorTest.h
//
// Definition of the SocketConnectorTest class.
//
// Copyright (c) 2005-2019, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef SocketConnectorTest_INCLUDED
#define SocketConnectorTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class SocketConnectorTest: public Poco::CppUnit::TestCase
{
public:
	SocketConnectorTest(const std::string& name);
	~SocketConnectorTest();

	void testUnregisterConnector();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();
};


#endif // SocketConnectorTest_INCLUDED
