//
// HelpFormatterTest.h
//
// Definition of the HelpFormatterTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef HelpFormatterTest_INCLUDED
#define HelpFormatterTest_INCLUDED


#include "Poco/Util/Util.h"
#include "Poco/CppUnit/TestCase.h"


class HelpFormatterTest: public Poco::CppUnit::TestCase
{
public:
	HelpFormatterTest(const std::string& name);
	~HelpFormatterTest();

	void testHelpFormatter();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // HelpFormatterTest_INCLUDED
