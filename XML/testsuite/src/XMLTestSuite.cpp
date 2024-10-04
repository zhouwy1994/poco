//
// XMLTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "XMLTestSuite.h"
#include "NameTest.h"
#include "NamePoolTest.h"
#include "XMLWriterTest.h"
#include "SAXTestSuite.h"
#include "DOMTestSuite.h"
#include "XMLStreamParserTest.h"

Poco::CppUnit::Test* XMLTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("XMLTestSuite");

	pSuite->addTest(NameTest::suite());
	pSuite->addTest(NamePoolTest::suite());
	pSuite->addTest(XMLWriterTest::suite());
	pSuite->addTest(SAXTestSuite::suite());
	pSuite->addTest(DOMTestSuite::suite());
	pSuite->addTest(XMLStreamParserTest::suite());

	return pSuite;
}
