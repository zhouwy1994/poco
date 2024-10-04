//
// EventTestSuite.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "EventTestSuite.h"
#include "FIFOEventTest.h"
#include "BasicEventTest.h"
#include "PriorityEventTest.h"

Poco::CppUnit::Test* EventTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("EventTestSuite");

	pSuite->addTest(BasicEventTest::suite());
	pSuite->addTest(PriorityEventTest::suite());
	pSuite->addTest(FIFOEventTest::suite());

	return pSuite;
}
