//
// PollSetTest.h
//
// Definition of the PollSetTest class.
//
// Copyright (c) 2016, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef PollSetTest_INCLUDED
#define PollSetTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class PollSetTest: public Poco::CppUnit::TestCase
{
public:
	PollSetTest(const std::string& name);
	~PollSetTest();

	void testAddUpdate();
	void testTimeout();
	void testPollNB();
	void testPoll();
	void testPollNoServer();
	void testPollClosedServer();
	void testPollSetWakeUp();
	void testClear();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();
};


#endif // PollSetTest_INCLUDED
