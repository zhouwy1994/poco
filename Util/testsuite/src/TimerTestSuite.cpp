//
// TimerTestSuite.cpp
//
// Copyright (c) 2009, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "TimerTestSuite.h"
#include "TimerTest.h"


Poco::CppUnit::Test* TimerTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("TimerTestSuite");

	pSuite->addTest(TimerTest::suite());

	return pSuite;
}
