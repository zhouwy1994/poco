//
// POP3ClientSessionTest.cpp
//
// Copyright (c) 2005-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "POP3ClientSessionTest.h"
#include "Poco/CppUnit/TestCaller.h"
#include "Poco/CppUnit/TestSuite.h"
#include "DialogServer.h"
#include "Poco/Net/POP3ClientSession.h"
#include "Poco/Net/MailMessage.h"
#include "Poco/Net/NetException.h"


using Poco::Net::POP3ClientSession;
using Poco::Net::MessageHeader;
using Poco::Net::MailMessage;
using Poco::Net::POP3Exception;


POP3ClientSessionTest::POP3ClientSessionTest(const std::string& name): Poco::CppUnit::TestCase(name)
{
}


POP3ClientSessionTest::~POP3ClientSessionTest()
{
}


void POP3ClientSessionTest::testLogin()
{
	DialogServer server;
	server.addResponse("+OK POP3 Ready...");
	server.addResponse("+OK USER");
	server.addResponse("+OK PASS");
	server.addResponse("+OK QUIT");
	POP3ClientSession session("127.0.0.1", server.port());
	session.login("user", "secret");
	std::string cmd = server.popCommand();
	assertTrue (cmd == "USER user");
	cmd = server.popCommand();
	assertTrue (cmd == "PASS secret");
	session.close();
	cmd = server.popCommand();
	assertTrue (cmd == "QUIT");
}


void POP3ClientSessionTest::testLoginFail()
{
	DialogServer server;
	server.addResponse("+OK POP3 Ready...");
	server.addResponse("+OK USER");
	server.addResponse("-ERR PASS");
	server.addResponse("+OK QUIT");
	POP3ClientSession session("127.0.0.1", server.port());
	try
	{
		session.login("user", "secret");
		fail("login failed - must throw");
	}
	catch (POP3Exception&)
	{
	}
	session.close();
}


void POP3ClientSessionTest::testMessageCount()
{
	DialogServer server;
	server.addResponse("+OK POP3 Ready...");
	server.addResponse("+OK USER");
	server.addResponse("+OK PASS");
	server.addResponse("+OK 42 12345");
	server.addResponse("+OK QUIT");
	POP3ClientSession session("127.0.0.1", server.port());
	session.login("user", "secret");
	server.clearCommands();
	int n = session.messageCount();
	std::string cmd = server.popCommand();
	assertTrue (cmd == "STAT");
	assertTrue (n == 42);
	session.close();
}


void POP3ClientSessionTest::testList()
{
	DialogServer server;
	server.addResponse("+OK POP3 Ready...");
	server.addResponse("+OK USER");
	server.addResponse("+OK PASS");
	server.addResponse(
		"+OK Here comes da list\r\n"
		"1 1234\r\n"
		"2 5678\r\n"
		"3 987\r\n"
		".\r\n"
	);
	server.addResponse("+OK QUIT");
	POP3ClientSession session("127.0.0.1", server.port());
	session.login("user", "secret");
	server.clearCommands();
	std::vector<POP3ClientSession::MessageInfo> infos;
	session.listMessages(infos);
	std::string cmd = server.popCommand();
	assertTrue (cmd == "LIST");
	assertTrue (infos.size() == 3);
	assertTrue (infos[0].id == 1);
	assertTrue (infos[0].size == 1234);
	assertTrue (infos[1].id == 2);
	assertTrue (infos[1].size == 5678);
	assertTrue (infos[2].id == 3);
	assertTrue (infos[2].size == 987);
	session.close();
}


void POP3ClientSessionTest::testRetrieveMessage()
{
	DialogServer server;
	server.addResponse("+OK POP3 Ready...");
	server.addResponse("+OK USER");
	server.addResponse("+OK PASS");
	server.addResponse(
		"+OK Here comes the message\r\n"
		"From: john.doe@no.where\r\n"
		"To: jane.doe@no.where\r\n"
		"Subject: test\r\n"
		"\r\n"
		"Hello Jane,\r\n"
		"\r\n"
		"blah blah blah...\r\n"
		"....\r\n"
		"\r\n"
		"Yours, John\r\n"
		".\r\n"
	);
	server.addResponse("+OK QUIT");
	POP3ClientSession session("127.0.0.1", server.port());
	session.login("user", "secret");
	server.clearCommands();
	MailMessage message;
	session.retrieveMessage(1, message);
	std::string cmd = server.popCommand();
	assertTrue (cmd == "RETR 1");

	assertTrue (message.getContent() ==
		"Hello Jane,\r\n"
		"\r\n"
		"blah blah blah...\r\n"
		"...\r\n"
		"\r\n"
		"Yours, John\r\n"
	);

	session.close();
}


void POP3ClientSessionTest::testRetrieveHeader()
{
	DialogServer server;
	server.addResponse("+OK POP3 Ready...");
	server.addResponse("+OK USER");
	server.addResponse("+OK PASS");
	server.addResponse(
		"+OK Here comes the message\r\n"
		"From: john.doe@no.where\r\n"
		"To: jane.doe@no.where\r\n"
		"Subject: test\r\n"
		"\r\n"
		"."
	);
	server.addResponse("+OK QUIT");
	POP3ClientSession session("127.0.0.1", server.port());
	session.login("user", "secret");
	server.clearCommands();
	MessageHeader header;
	session.retrieveHeader(1, header);
	std::string cmd = server.popCommand();
	assertTrue (cmd == "TOP 1 0");
	assertTrue (header.get("From") == "john.doe@no.where");
	assertTrue (header.get("To") == "jane.doe@no.where");
	assertTrue (header.get("Subject") == "test");
	session.close();
}


void POP3ClientSessionTest::testRetrieveMessages()
{
	DialogServer server;
	server.addResponse("+OK POP3 Ready...");
	server.addResponse("+OK USER");
	server.addResponse("+OK PASS");
	server.addResponse(
		"+OK Here comes the message\r\n"
		"From: john.doe@no.where\r\n"
		"To: jane.doe@no.where\r\n"
		"Subject: test\r\n"
		"\r\n"
		"."
	);
	server.addResponse(
		"+OK Here comes the message\r\n"
		"From: john.doe@no.where\r\n"
		"To: jane.doe@no.where\r\n"
		"Subject: test\r\n"
		"\r\n"
		"Hello Jane,\r\n"
		"\r\n"
		"blah blah blah...\r\n"
		"....\r\n"
		"\r\n"
		"Yours, John\r\n"
		"."
	);
	server.addResponse("+OK QUIT");
	POP3ClientSession session("127.0.0.1", server.port());
	session.login("user", "secret");
	server.clearCommands();
	MessageHeader header;
	session.retrieveHeader(1, header);
	std::string cmd = server.popCommand();
	assertTrue (cmd == "TOP 1 0");
	assertTrue (header.get("From") == "john.doe@no.where");
	assertTrue (header.get("To") == "jane.doe@no.where");
	assertTrue (header.get("Subject") == "test");

	MailMessage message;
	session.retrieveMessage(2, message);
	cmd = server.popCommand();
	assertTrue (cmd == "RETR 2");

	assertTrue (message.getContent() ==
		"Hello Jane,\r\n"
		"\r\n"
		"blah blah blah...\r\n"
		"...\r\n"
		"\r\n"
		"Yours, John\r\n"
	);
	session.close();
}


void POP3ClientSessionTest::testDeleteMessage()
{
	DialogServer server;
	server.addResponse("+OK POP3 Ready...");
	server.addResponse("+OK USER");
	server.addResponse("+OK PASS");
	server.addResponse("+OK DELETED");
	server.addResponse("+OK QUIT");
	POP3ClientSession session("127.0.0.1", server.port());
	session.login("user", "secret");
	server.clearCommands();
	session.deleteMessage(42);
	std::string cmd = server.popCommand();
	assertTrue (cmd == "DELE 42");
	session.close();
}


void POP3ClientSessionTest::setUp()
{
}


void POP3ClientSessionTest::tearDown()
{
}


Poco::CppUnit::Test* POP3ClientSessionTest::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("POP3ClientSessionTest");

	CppUnit_addTest(pSuite, POP3ClientSessionTest, testLogin);
	CppUnit_addTest(pSuite, POP3ClientSessionTest, testLoginFail);
	CppUnit_addTest(pSuite, POP3ClientSessionTest, testMessageCount);
	CppUnit_addTest(pSuite, POP3ClientSessionTest, testList);
	CppUnit_addTest(pSuite, POP3ClientSessionTest, testRetrieveMessage);
	CppUnit_addTest(pSuite, POP3ClientSessionTest, testRetrieveHeader);
	CppUnit_addTest(pSuite, POP3ClientSessionTest, testRetrieveMessages);
	CppUnit_addTest(pSuite, POP3ClientSessionTest, testDeleteMessage);

	return pSuite;
}
