//
// MongoDBTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "MongoDBTestSuite.h"
#include "MongoDBTest.h"


Poco::CppUnit::Test* MongoDBTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("MongoDBTestSuite");

	pSuite->addTest(MongoDBTest::suite());

	return pSuite;
}
