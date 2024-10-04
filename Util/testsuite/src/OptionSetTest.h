//
// OptionSetTest.h
//
// Definition of the OptionSetTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef OptionSetTest_INCLUDED
#define OptionSetTest_INCLUDED


#include "Poco/Util/Util.h"
#include "Poco/CppUnit/TestCase.h"


class OptionSetTest: public Poco::CppUnit::TestCase
{
public:
	OptionSetTest(const std::string& name);
	~OptionSetTest();

	void testOptionSet();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // OptionSetTest_INCLUDED
