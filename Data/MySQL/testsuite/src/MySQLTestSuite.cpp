//
// ODBCTestSuite.cpp
//
// Copyright (c) 2008, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "MySQLTestSuite.h"
#include "MySQLTest.h"


Poco::CppUnit::Test* MySQLTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("MySQLTestSuite");

	addTest(pSuite, MySQLTest::suite());
	return pSuite;
}


void MySQLTestSuite::addTest(Poco::CppUnit::TestSuite* pSuite, Poco::CppUnit::Test* pT)
{
	if (pSuite && pT) pSuite->addTest(pT);
}
