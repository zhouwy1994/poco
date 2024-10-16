//
// NTPClientTest.h
//
// Definition of the NTPClientTest class.
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef NTPClientTest_INCLUDED
#define NTPClientTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"
#include "Poco/Net/NTPClient.h"
#include "Poco/Net/NTPEventArgs.h"


class NTPClientTest: public Poco::CppUnit::TestCase
{
public:
	NTPClientTest(const std::string& name);
	~NTPClientTest();

	void testTimeSync();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

	void onResponse(const void* pSender, Poco::Net::NTPEventArgs& args);
private:
	Poco::Net::NTPClient _ntpClient;
};


#endif // NTPClientTest_INCLUDED
