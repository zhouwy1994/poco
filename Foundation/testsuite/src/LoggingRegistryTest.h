//
// LoggingRegistryTest.h
//
// Definition of the LoggingRegistryTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef LoggingRegistryTest_INCLUDED
#define LoggingRegistryTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class LoggingRegistryTest: public Poco::CppUnit::TestCase
{
public:
	LoggingRegistryTest(const std::string& name);
	~LoggingRegistryTest();

	void testRegister();
	void testReregister();
	void testUnregister();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // LoggingRegistryTest_INCLUDED
