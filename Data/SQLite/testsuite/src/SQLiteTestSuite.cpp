//
// SQLiteTestSuite.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "SQLiteTestSuite.h"
#include "SQLiteTest.h"


Poco::CppUnit::Test* SQLiteTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("SQLiteTestSuite");

	pSuite->addTest(SQLiteTest::suite());

	return pSuite;
}
