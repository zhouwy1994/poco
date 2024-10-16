//
// ChildNodesTest.h
//
// Definition of the ChildNodesTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef ChildNodesTest_INCLUDED
#define ChildNodesTest_INCLUDED


#include "Poco/XML/XML.h"
#include "Poco/CppUnit/TestCase.h"


class ChildNodesTest: public Poco::CppUnit::TestCase
{
public:
	ChildNodesTest(const std::string& name);
	~ChildNodesTest();

	void testChildNodes();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // ChildNodesTest_INCLUDED
