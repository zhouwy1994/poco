//
// ReactorTestSuite.cpp
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "ReactorTestSuite.h"
#include "SocketReactorTest.h"
#include "SocketConnectorTest.h"


Poco::CppUnit::Test* ReactorTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("ReactorTestSuite");

	pSuite->addTest(SocketReactorTest::suite());
	pSuite->addTest(SocketConnectorTest::suite());

	return pSuite;
}
