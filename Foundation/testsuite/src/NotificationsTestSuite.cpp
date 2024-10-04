//
// NotificationsTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "NotificationsTestSuite.h"
#include "NotificationCenterTest.h"
#include "NotificationQueueTest.h"
#include "PriorityNotificationQueueTest.h"
#include "TimedNotificationQueueTest.h"


Poco::CppUnit::Test* NotificationsTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("NotificationsTestSuite");

	pSuite->addTest(NotificationCenterTest::suite());
	pSuite->addTest(NotificationQueueTest::suite());
	pSuite->addTest(PriorityNotificationQueueTest::suite());
	pSuite->addTest(TimedNotificationQueueTest::suite());

	return pSuite;
}
