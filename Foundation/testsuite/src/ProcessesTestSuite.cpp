//
// ProcessesTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "ProcessesTestSuite.h"
#include "ProcessTest.h"
#include "NamedMutexTest.h"
#include "NamedEventTest.h"
#include "SharedMemoryTest.h"


Poco::CppUnit::Test* ProcessesTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("ProcessesTestSuite");

	pSuite->addTest(ProcessTest::suite());
	pSuite->addTest(NamedMutexTest::suite());
	pSuite->addTest(NamedEventTest::suite());
	pSuite->addTest(SharedMemoryTest::suite());

	return pSuite;
}
