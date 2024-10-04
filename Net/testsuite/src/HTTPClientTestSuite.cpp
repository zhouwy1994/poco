//
// HTTPClientTestSuite.cpp
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "HTTPClientTestSuite.h"
#include "HTTPClientSessionTest.h"
#include "HTTPStreamFactoryTest.h"


Poco::CppUnit::Test* HTTPClientTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("HTTPClientTestSuite");

	pSuite->addTest(HTTPClientSessionTest::suite());
	pSuite->addTest(HTTPStreamFactoryTest::suite());

	return pSuite;
}
