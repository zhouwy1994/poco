//
// HTTPSStreamFactoryTest.h
//
// Definition of the HTTPSStreamFactoryTest class.
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef HTTPSStreamFactoryTest_INCLUDED
#define HTTPSStreamFactoryTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class HTTPSStreamFactoryTest: public Poco::CppUnit::TestCase
{
public:
	HTTPSStreamFactoryTest(const std::string& name);
	~HTTPSStreamFactoryTest();

	void testNoRedirect();
	void testEmptyPath();
	void testRedirect();
	void testProxy();
	void testError();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // HTTPSStreamFactoryTest_INCLUDED
