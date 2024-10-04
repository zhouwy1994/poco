//
// HTTPServerTestSuite.h
//
// Definition of the HTTPServerTestSuite class.
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef HTTPServerTestSuite_INCLUDED
#define HTTPServerTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class HTTPServerTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // HTTPServerTestSuite_INCLUDED
