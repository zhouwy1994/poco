//
// UUIDTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "UUIDTestSuite.h"
#include "UUIDTest.h"
#include "UUIDGeneratorTest.h"


Poco::CppUnit::Test* UUIDTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("UUIDTestSuite");

	pSuite->addTest(UUIDTest::suite());
	pSuite->addTest(UUIDGeneratorTest::suite());

	return pSuite;
}
