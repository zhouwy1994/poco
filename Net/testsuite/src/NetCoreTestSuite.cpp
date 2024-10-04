//
// NetCoreTestSuite.cpp
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "NetCoreTestSuite.h"
#include "IPAddressTest.h"
#include "SocketAddressTest.h"
#include "DNSTest.h"
#include "NetworkInterfaceTest.h"


Poco::CppUnit::Test* NetCoreTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("NetCoreTestSuite");

	pSuite->addTest(IPAddressTest::suite());
	pSuite->addTest(SocketAddressTest::suite());
	pSuite->addTest(DNSTest::suite());
#ifdef POCO_NET_HAS_INTERFACE
	pSuite->addTest(NetworkInterfaceTest::suite());
#endif // POCO_NET_HAS_INTERFACE
	return pSuite;
}
