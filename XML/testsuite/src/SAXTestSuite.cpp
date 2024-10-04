//
// SAXTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "SAXTestSuite.h"
#include "AttributesImplTest.h"
#include "NamespaceSupportTest.h"
#include "SAXParserTest.h"


Poco::CppUnit::Test* SAXTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("SAXTestSuite");

	pSuite->addTest(AttributesImplTest::suite());
	pSuite->addTest(NamespaceSupportTest::suite());
	pSuite->addTest(SAXParserTest::suite());

	return pSuite;
}
