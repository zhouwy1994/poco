//
// SocketReactorTest.h
//
// Definition of the SocketReactorTest class.
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef SocketReactorTest_INCLUDED
#define SocketReactorTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class SocketReactorTest: public Poco::CppUnit::TestCase
{
public:
	SocketReactorTest(const std::string& name);
	~SocketReactorTest();

	void testSocketReactor();
	void testSetSocketReactor();
	void testParallelSocketReactor();
	void testSocketConnectorFail();
	void testSocketConnectorTimeout();
	void testDataCollection();
	void testSocketConnectorDeadlock();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // SocketReactorTest_INCLUDED
