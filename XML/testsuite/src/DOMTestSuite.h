//
// DOMTestSuite.h
//
// Definition of the DOMTestSuite class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef DOMTestSuite_INCLUDED
#define DOMTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class DOMTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // DOMTestSuite_INCLUDED
