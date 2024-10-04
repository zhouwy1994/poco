//
// ZipTestSuite.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "ZipTestSuite.h"
#include "ZipTest.h"
#include "PartialStreamTest.h"
#include "CompressTest.h"


Poco::CppUnit::Test* ZipTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("ZipTestSuite");

	pSuite->addTest(CompressTest::suite());
	pSuite->addTest(ZipTest::suite());
	pSuite->addTest(PartialStreamTest::suite());

	return pSuite;
}
