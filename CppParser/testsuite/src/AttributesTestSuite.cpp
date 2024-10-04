//
// AttributesTestSuite.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "AttributesTestSuite.h"
#include "AttributesParserTest.h"


Poco::CppUnit::Test* AttributesTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("CppParserTestSuite");

	pSuite->addTest(AttributesParserTest::suite());

	return pSuite;
}
