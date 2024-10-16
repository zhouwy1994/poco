//
// RawSocketTest.h
//
// Definition of the RawSocketTest class.
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef RawSocketTest_INCLUDED
#define RawSocketTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class RawSocketTest: public Poco::CppUnit::TestCase
{
public:
	RawSocketTest(const std::string& name);
	~RawSocketTest();

	void testEchoIPv4();
	void testSendToReceiveFromIPv4();
	void testEchoIPv4Move();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // RawSocketTest_INCLUDED
