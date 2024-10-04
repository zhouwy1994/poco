//
// JSONTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "JSONTestSuite.h"
#include "JSONTest.h"


Poco::CppUnit::Test* JSONTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("JSONTestSuite");

	pSuite->addTest(JSONTest::suite());

	return pSuite;
}
