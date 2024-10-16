//
// SQLiteTestSuite.h
//
// Definition of the SQLiteTestSuite class.
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef SQLiteTestSuite_INCLUDED
#define SQLiteTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class SQLiteTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // SQLiteTestSuite_INCLUDED
