//
// StreamTokenizerTest.h
//
// Definition of the StreamTokenizerTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef StreamTokenizerTest_INCLUDED
#define StreamTokenizerTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class StreamTokenizerTest: public Poco::CppUnit::TestCase
{
public:
	StreamTokenizerTest(const std::string& name);
	~StreamTokenizerTest();

	void testTokenizer1();
	void testTokenizer2();
	void testTokenizer3();
	void testTokenizer4();
	void testTokenizer5();
	void testTokenizer6();
	void testTokenizer7();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // StreamTokenizerTest_INCLUDED
