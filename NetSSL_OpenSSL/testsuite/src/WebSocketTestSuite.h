//
// WebSocketTestSuite.h
//
// Definition of the WebSocketTestSuite class.
//
// Copyright (c) 2012, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef WebSocketTestSuite_INCLUDED
#define WebSocketTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class WebSocketTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // WebSocketTestSuite_INCLUDED
