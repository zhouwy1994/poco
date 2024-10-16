//
// HTTPTestSuite.cpp
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "HTTPTestSuite.h"
#include "HTTPRequestTest.h"
#include "HTTPResponseTest.h"
#include "HTTPCookieTest.h"
#include "HTTPCredentialsTest.h"
#include "NTLMCredentialsTest.h"


Poco::CppUnit::Test* HTTPTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("HTTPTestSuite");

	pSuite->addTest(HTTPRequestTest::suite());
	pSuite->addTest(HTTPResponseTest::suite());
	pSuite->addTest(HTTPCookieTest::suite());
	pSuite->addTest(HTTPCredentialsTest::suite());
	pSuite->addTest(NTLMCredentialsTest::suite());

	return pSuite;
}
