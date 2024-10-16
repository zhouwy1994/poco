//
// JSONTestSuite.h
//
// Definition of the JSONTestSuite class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef JSONTestSuite_INCLUDED
#define JSONTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class JSONTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // JSONTestSuite_INCLUDED
