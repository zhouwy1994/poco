//
// UtilTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "UtilTestSuite.h"
#include "ConfigurationTestSuite.h"
#include "OptionsTestSuite.h"
#include "TimerTestSuite.h"
#if defined(_MSC_VER) && !defined(_WIN32_WCE)
#include "WindowsTestSuite.h"
#endif


Poco::CppUnit::Test* UtilTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("UtilTestSuite");

	pSuite->addTest(ConfigurationTestSuite::suite());
	pSuite->addTest(OptionsTestSuite::suite());
	pSuite->addTest(TimerTestSuite::suite());
#if defined(_MSC_VER) && !defined(_WIN32_WCE)
	pSuite->addTest(WindowsTestSuite::suite());
#endif

	return pSuite;
}
