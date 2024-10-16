//
// UUIDGeneratorTest.h
//
// Definition of the UUIDGeneratorTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef UUIDGeneratorTest_INCLUDED
#define UUIDGeneratorTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class UUIDGeneratorTest: public Poco::CppUnit::TestCase
{
public:
	UUIDGeneratorTest(const std::string& name);
	~UUIDGeneratorTest();

	void testTimeBased();
	void testRandom();
	void testNameBased();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // UUIDGeneratorTest_INCLUDED
