//
// ODBCTestSuite.h
//
// Definition of the ODBCTestSuite class.
//
// Copyright (c) 2008, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef MySQLTestSuite_INCLUDED
#define MySQLTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"

class MySQLTestSuite
{
public:
	static Poco::CppUnit::Test* suite();

private:
	static void addTest(Poco::CppUnit::TestSuite* pSuite, Poco::CppUnit::Test* pT);
};


#endif // MySQLTestSuite_INCLUDED
