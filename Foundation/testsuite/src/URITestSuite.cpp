//
// URITestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "URITestSuite.h"
#include "URITest.h"
#include "URIStreamOpenerTest.h"


Poco::CppUnit::Test* URITestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("URITestSuite");

	pSuite->addTest(URITest::suite());
	pSuite->addTest(URIStreamOpenerTest::suite());

	return pSuite;
}
