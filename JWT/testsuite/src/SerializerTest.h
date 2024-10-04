//
// SerializerTest.h
//
// Definition of the SerializerTest class.
//
// Copyright (c) 2019, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef SerializerTest_INCLUDED
#define SerializerTest_INCLUDED


#include "Poco/JWT/JWT.h"
#include "Poco/CppUnit/TestCase.h"


class SerializerTest: public Poco::CppUnit::TestCase
{
public:
	SerializerTest(const std::string& name);
	~SerializerTest();

	void setUp();
	void tearDown();

	void testSerializeEmpty();
	void testSerializeAlgNone();
	void testSerializeAlgHS256();
	void testDeserializeEmpty();
	void testDeserializeAlgNone();
	void testDeserializeAlgHS256();
	void testSplit();
	void testSplitEmptySig();

	static Poco::CppUnit::Test* suite();
};


#endif // SerializerTest_INCLUDED
