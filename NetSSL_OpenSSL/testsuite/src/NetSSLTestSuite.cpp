//
// OpenSSLTestSuite.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "NetSSLTestSuite.h"

#include "HTTPSClientTestSuite.h"
#include "TCPServerTestSuite.h"
#include "HTTPSServerTestSuite.h"
#include "WebSocketTestSuite.h"
#include "FTPSClientTestSuite.h"


Poco::CppUnit::Test* NetSSLTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("OpenSSLTestSuite");

	pSuite->addTest(HTTPSClientTestSuite::suite());
	pSuite->addTest(TCPServerTestSuite::suite());
	pSuite->addTest(HTTPSServerTestSuite::suite());
	pSuite->addTest(WebSocketTestSuite::suite());
	pSuite->addTest(FTPSClientTestSuite::suite());

	return pSuite;
}
