//
// HTMLTestSuite.cpp
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "HTMLTestSuite.h"
#include "HTMLFormTest.h"


Poco::CppUnit::Test* HTMLTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("HTMLTestSuite");

	pSuite->addTest(HTMLFormTest::suite());

	return pSuite;
}
