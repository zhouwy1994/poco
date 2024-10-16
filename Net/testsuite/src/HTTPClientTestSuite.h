//
// HTTPClientTestSuite.h
//
// Definition of the HTTPClientTestSuite class.
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef HTTPClientTestSuite_INCLUDED
#define HTTPClientTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class HTTPClientTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // HTTPClientTestSuite_INCLUDED
