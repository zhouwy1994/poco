//
// FoundationTestSuite.h
//
// Definition of the FoundationTestSuite class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef FoundationTestSuite_INCLUDED
#define FoundationTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class FoundationTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // FoundationTestSuite_INCLUDED
