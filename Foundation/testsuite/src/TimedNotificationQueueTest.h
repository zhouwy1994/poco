//
// TimedNotificationQueueTest.h
//
// Definition of the TimedNotificationQueueTest class.
//
// Copyright (c) 2009, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef TimedNotificationQueueTest_INCLUDED
#define TimedNotificationQueueTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"
#include "Poco/TimedNotificationQueue.h"
#include "Poco/Mutex.h"
#include <set>


class TimedNotificationQueueTest: public Poco::CppUnit::TestCase
{
public:
	TimedNotificationQueueTest(const std::string& name);
	~TimedNotificationQueueTest();

	void testDequeue();
	void testDequeueNext();
	void testWaitDequeue();
	void testWaitDequeueTimeout();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

protected:
	void work();

private:
};


#endif // TimedNotificationQueueTest_INCLUDED
