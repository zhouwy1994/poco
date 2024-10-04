//
// PDFTestSuite.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "PDFTestSuite.h"
#include "PDFTest.h"


Poco::CppUnit::Test* PDFTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("PDFTestSuite");

	pSuite->addTest(PDFTest::suite());

	return pSuite;
}
