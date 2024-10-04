//
// HTTPServerTestSuite.cpp
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "HTTPServerTestSuite.h"
#include "HTTPServerTest.h"


Poco::CppUnit::Test* HTTPServerTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("HTTPServerTestSuite");

	pSuite->addTest(HTTPServerTest::suite());

	return pSuite;
}
