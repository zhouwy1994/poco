//
// AutoPtrTest.h
//
// Definition of the AutoPtrTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef AutoPtrTest_INCLUDED
#define AutoPtrTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class AutoPtrTest: public Poco::CppUnit::TestCase
{
public:
	AutoPtrTest(const std::string& name);
	~AutoPtrTest();

	void testAutoPtr();
	void testOps();
	void testMakeAuto();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // AutoPtrTest_INCLUDED
