//
// NetTestSuite.h
//
// Definition of the NetTestSuite class.
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef NetTestSuite_INCLUDED
#define NetTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class NetTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // NetTestSuite_INCLUDED
