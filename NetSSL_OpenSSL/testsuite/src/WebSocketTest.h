//
// WebSocketTest.h
//
// Definition of the WebSocketTest class.
//
// Copyright (c) 2012, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef WebSocketTest_INCLUDED
#define WebSocketTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class WebSocketTest: public Poco::CppUnit::TestCase
{
public:
	WebSocketTest(const std::string& name);
	~WebSocketTest();

	void testWebSocket();
	void testWebSocketLarge();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // WebSocketTest_INCLUDED
