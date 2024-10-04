//
// HTTPSServerTestSuite.cpp
//
// Copyright (c) 2006-2014, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "HTTPSServerTestSuite.h"
#include "HTTPSServerTest.h"


Poco::CppUnit::Test* HTTPSServerTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("HTTPSServerTestSuite");

	pSuite->addTest(HTTPSServerTest::suite());

	return pSuite;
}
