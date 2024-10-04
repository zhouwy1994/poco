//
// ICMPClientTestSuite.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "ICMPClientTestSuite.h"
#include "ICMPClientTest.h"
#include "ICMPSocketTest.h"


Poco::CppUnit::Test* ICMPClientTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("ICMPClientTestSuite");

	pSuite->addTest(ICMPClientTest::suite());
	pSuite->addTest(ICMPSocketTest::suite());

	return pSuite;
}
