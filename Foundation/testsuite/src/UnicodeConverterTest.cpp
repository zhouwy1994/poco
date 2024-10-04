//
// UnicodeConverterTest.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef POCO_NO_WSTRING


#include "Poco/UnicodeConverter.h"
#include "UnicodeConverterTest.h"
#include "Poco/CppUnit/TestCaller.h"
#include "Poco/CppUnit/TestSuite.h"
#include "Poco/UTFString.h"


using Poco::UnicodeConverter;
using Poco::UTF16Char;
using Poco::UTF16String;
using Poco::UTF32Char;
using Poco::UTF32String;


UnicodeConverterTest::UnicodeConverterTest(const std::string& name): Poco::CppUnit::TestCase(name)
{
}


UnicodeConverterTest::~UnicodeConverterTest()
{
}


void UnicodeConverterTest::testUTF16()
{

	runTests<UTF16String>();
}


void UnicodeConverterTest::testUTF32()
{
	runTests<UTF32String>();
}


void UnicodeConverterTest::setUp()
{
}


void UnicodeConverterTest::tearDown()
{
}


Poco::CppUnit::Test* UnicodeConverterTest::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("UnicodeConverterTest");

	CppUnit_addTest(pSuite, UnicodeConverterTest, testUTF16);
	CppUnit_addTest(pSuite, UnicodeConverterTest, testUTF32);

	return pSuite;
}


#endif

