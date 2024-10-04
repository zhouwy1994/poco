//
// PostgreSQLTestSuite.cpp
//
// Copyright (c) 2015, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "PostgreSQLTestSuite.h"
#include "PostgreSQLTest.h"

Poco::CppUnit::Test* PostgreSQLTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("PostgreSQLTestSuite");

	addTest(pSuite, PostgreSQLTest::suite());
	return pSuite;
}


void PostgreSQLTestSuite::addTest(Poco::CppUnit::TestSuite* pSuite, Poco::CppUnit::Test* pT)
{
	if (pSuite && pT) pSuite->addTest(pT);
}
