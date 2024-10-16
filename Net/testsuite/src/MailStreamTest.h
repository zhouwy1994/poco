//
// MailStreamTest.h
//
// Definition of the MailStreamTest class.
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef MailStreamTest_INCLUDED
#define MailStreamTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class MailStreamTest: public Poco::CppUnit::TestCase
{
public:
	MailStreamTest(const std::string& name);
	~MailStreamTest();

	void testMailInputStream();
	void testMailOutputStream();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // MailStreamTest_INCLUDED
