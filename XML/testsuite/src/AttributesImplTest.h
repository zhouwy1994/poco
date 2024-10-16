//
// AttributesImplTest.h
//
// Definition of the AttributesImplTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef AttributesImplTest_INCLUDED
#define AttributesImplTest_INCLUDED


#include "Poco/XML/XML.h"
#include "Poco/CppUnit/TestCase.h"


class AttributesImplTest: public Poco::CppUnit::TestCase
{
public:
	AttributesImplTest(const std::string& name);
	~AttributesImplTest();

	void testNoNamespaces();
	void testNamespaces();
	void testAccessors();
	void testCopy();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // AttributesImplTest_INCLUDED
