//
// ActiveRecordTestSuite.cpp
//
// Copyright (c) 2020, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "ActiveRecordTestSuite.h"
#include "ActiveRecordTest.h"


Poco::CppUnit::Test* ActiveRecordTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("ActiveRecordTestSuite");

	pSuite->addTest(ActiveRecordTest::suite());

	return pSuite;
}
