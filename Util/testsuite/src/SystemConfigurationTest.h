//
// SystemConfigurationTest.h
//
// Definition of the SystemConfigurationTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef SystemConfigurationTest_INCLUDED
#define SystemConfigurationTest_INCLUDED


#include "Poco/Util/Util.h"
#include "Poco/CppUnit/TestCase.h"


class SystemConfigurationTest: public Poco::CppUnit::TestCase
{
public:
	SystemConfigurationTest(const std::string& name);
	~SystemConfigurationTest();

	void testProperties();
	void testKeys();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // SystemConfigurationTest_INCLUDED
