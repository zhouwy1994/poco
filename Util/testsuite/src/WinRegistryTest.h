//
// WinRegistryTest.h
//
// Definition of the WinRegistryTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef WinRegistryTest_INCLUDED
#define WinRegistryTest_INCLUDED


#include "Poco/Util/Util.h"
#include "Poco/CppUnit/TestCase.h"


class WinRegistryTest: public Poco::CppUnit::TestCase
{
public:
	WinRegistryTest(const std::string& name);
	~WinRegistryTest();

	void testRegistry();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // WinRegistryTest_INCLUDED
