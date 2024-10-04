//
// JWTTestSuite.h
//
// Definition of the JWTTestSuite class.
//
// Copyright (c) 2019, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef JWTTestSuite_INCLUDED
#define JWTTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class JWTTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // JWTTestSuite_INCLUDED
