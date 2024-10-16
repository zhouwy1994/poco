//
// MailMessageTest.h
//
// Definition of the MailMessageTest class.
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef MailMessageTest_INCLUDED
#define MailMessageTest_INCLUDED


#include "Poco/Net/Net.h"
#include "Poco/CppUnit/TestCase.h"


class MailMessageTest: public Poco::CppUnit::TestCase
{
public:
	MailMessageTest(const std::string& name);
	~MailMessageTest();

	void testWriteQP();
	void testWrite8Bit();
	void testWriteBase64();
	void testWriteManyRecipients();
	void testWriteMultiPart();
	void testReadWriteMultiPart();
	void testReadWriteMultiPartStore();
	void testReadDefaultTransferEncoding();
	void testContentDisposition();
	void testReadQP();
	void testRead8Bit();
	void testReadMultiPart();
	void testReadMultiPartWithAttachmentNames();
	void testReadMultiPartDefaultTransferEncoding();
	void testReadMultiPartNoFinalBoundaryFromFile();
	void testEncodeWord();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // MailMessageTest_INCLUDED
