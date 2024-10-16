//
// MailTestSuite.cpp
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "MailTestSuite.h"
#include "MailMessageTest.h"
#include "MailStreamTest.h"
#include "SMTPClientSessionTest.h"
#include "POP3ClientSessionTest.h"


Poco::CppUnit::Test* MailTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("MailTestSuite");

	pSuite->addTest(MailMessageTest::suite());
	pSuite->addTest(MailStreamTest::suite());
	pSuite->addTest(SMTPClientSessionTest::suite());
	pSuite->addTest(POP3ClientSessionTest::suite());

	return pSuite;
}
