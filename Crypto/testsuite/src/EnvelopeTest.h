//
// EnvelopeTest.h
//
// Definition of the EnvelopeTest class.
//
// Copyright (c) 2012, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef EnvelopeTest_INCLUDED
#define EnvelopeTest_INCLUDED


#include "Poco/Crypto/Crypto.h"
#include "Poco/CppUnit/TestCase.h"


class EnvelopeTest: public Poco::CppUnit::TestCase
{
public:
	EnvelopeTest(const std::string& name);
	~EnvelopeTest();

	void testOneKeyRSA();
	void testMultiKeyRSA();
	void testRSATransfer();
	void testRSAMultiTransfer();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // EnvelopeTest_INCLUDED
