//
// ValidatorTest.h
//
// Definition of the ValidatorTest class.
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef ValidatorTest_INCLUDED
#define ValidatorTest_INCLUDED


#include "Poco/Util/Util.h"
#include "Poco/CppUnit/TestCase.h"


class ValidatorTest: public Poco::CppUnit::TestCase
{
public:
	ValidatorTest(const std::string& name);
	~ValidatorTest();

	void testRegExpValidator();
	void testIntValidator();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // ValidatorTest_INCLUDED
