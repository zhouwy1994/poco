//
// ODBCTestSuite.h
//
// Definition of the ODBCTestSuite class.
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef ODBCTestSuite_INCLUDED
#define ODBCTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class ODBCTestSuite
{
public:
	static Poco::CppUnit::Test* suite();

private:
	static void addTest(Poco::CppUnit::TestSuite* pSuite, Poco::CppUnit::Test* pT);
};


#endif // ODBCTestSuite_INCLUDED
