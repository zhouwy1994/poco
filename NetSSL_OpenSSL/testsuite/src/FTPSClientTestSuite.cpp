//
// FTPClientTestSuite.cpp
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "FTPSClientTestSuite.h"
#include "FTPSClientSessionTest.h"


Poco::CppUnit::Test* FTPSClientTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("FTPSClientTestSuite");

	pSuite->addTest(FTPSClientSessionTest::suite());

	return pSuite;
}
