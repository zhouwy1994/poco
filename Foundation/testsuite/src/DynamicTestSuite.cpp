//
// DynamicTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "DynamicTestSuite.h"
#include "VarTest.h"


Poco::CppUnit::Test* DynamicTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("DynamicTestSuite");

	pSuite->addTest(VarTest::suite());

	return pSuite;
}
