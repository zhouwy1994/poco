//
// WindowsTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "WindowsTestSuite.h"
#include "WinRegistryTest.h"
#include "WinConfigurationTest.h"
#include "WinServiceTest.h"


Poco::CppUnit::Test* WindowsTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("WindowsTestSuite");

	pSuite->addTest(WinRegistryTest::suite());
	pSuite->addTest(WinConfigurationTest::suite());
#ifdef ENABLE_WINSERVICE_TEST
	pSuite->addTest(WinServiceTest::suite());
#endif

	return pSuite;
}
