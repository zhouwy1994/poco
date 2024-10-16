//
// NullStreamTest.h
//
// Definition of the NullStreamTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef NullStreamTest_INCLUDED
#define NullStreamTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class NullStreamTest: public Poco::CppUnit::TestCase
{
public:
	NullStreamTest(const std::string& name);
	~NullStreamTest();

	void testInput();
	void testOutput();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // NullStreamTest_INCLUDED
