//
// FTPClientTestSuite.cpp
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "FTPClientTestSuite.h"
#include "FTPClientSessionTest.h"
#include "FTPStreamFactoryTest.h"


Poco::CppUnit::Test* FTPClientTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("FTPClientTestSuite");

	pSuite->addTest(FTPClientSessionTest::suite());
	pSuite->addTest(FTPStreamFactoryTest::suite());

	return pSuite;
}
