//
// CppParserTest.h
//
// Definition of the CppParserTest class.
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef CppParserTest_INCLUDED
#define CppParserTest_INCLUDED


#include "Poco/CppParser/CppParser.h"
#include "Poco/CppUnit/TestCase.h"


class CppParserTest: public Poco::CppUnit::TestCase
{
public:
	CppParserTest(const std::string& name);
	~CppParserTest();

	void testParseDir();
	void testExtractName();
	void testNumberLiterals();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

protected:
	void testNumberLiteral(const std::string& literal);

private:
};


#endif // CppParserTest_INCLUDED
