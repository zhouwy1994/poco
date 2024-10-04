//
// CppParserTestSuite.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "CppParserTestSuite.h"
#include "AttributesTestSuite.h"
#include "CppParserTest.h"


Poco::CppUnit::Test* CppParserTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("CppParserTestSuite");

	pSuite->addTest(AttributesTestSuite::suite());
	pSuite->addTest(CppParserTest::suite());

	return pSuite;
}
