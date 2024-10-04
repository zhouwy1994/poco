//
// HTTPSClientTestSuite.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "HTTPSClientTestSuite.h"
#include "HTTPSClientSessionTest.h"
#include "HTTPSStreamFactoryTest.h"


Poco::CppUnit::Test* HTTPSClientTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("HTTPSClientTestSuite");

	pSuite->addTest(HTTPSClientSessionTest::suite());
	pSuite->addTest(HTTPSStreamFactoryTest::suite());

	return pSuite;
}
