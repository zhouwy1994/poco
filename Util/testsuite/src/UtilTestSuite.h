//
// UtilTestSuite.h
//
// Definition of the UtilTestSuite class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef UtilTestSuite_INCLUDED
#define UtilTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class UtilTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // UtilTestSuite_INCLUDED
