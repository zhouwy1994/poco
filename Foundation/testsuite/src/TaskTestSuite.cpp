//
// TaskTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "TaskTestSuite.h"
#include "TaskTest.h"
#include "TaskManagerTest.h"


Poco::CppUnit::Test* TaskTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("TaskTestSuite");

	pSuite->addTest(TaskTest::suite());
	pSuite->addTest(TaskManagerTest::suite());

	return pSuite;
}
