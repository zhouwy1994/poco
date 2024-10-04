//
// OptionProcessorTest.h
//
// Definition of the OptionProcessorTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef OptionProcessorTest_INCLUDED
#define OptionProcessorTest_INCLUDED


#include "Poco/Util/Util.h"
#include "Poco/CppUnit/TestCase.h"


class OptionProcessorTest: public Poco::CppUnit::TestCase
{
public:
	OptionProcessorTest(const std::string& name);
	~OptionProcessorTest();

	void testUnix();
	void testDefault();
	void testRequired();
	void testArgs();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // OptionProcessorTest_INCLUDED
