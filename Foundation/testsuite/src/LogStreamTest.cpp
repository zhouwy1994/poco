//
// LogStreamTest.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// All rights reserved.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "LogStreamTest.h"
#include "Poco/CppUnit/TestCaller.h"
#include "Poco/CppUnit/TestSuite.h"
#include "Poco/Logger.h"
#include "Poco/LogStream.h"
#include "Poco/AutoPtr.h"
#include "TestChannel.h"


using Poco::Logger;
using Poco::LogStream;
using Poco::Channel;
using Poco::Message;
using Poco::AutoPtr;


LogStreamTest::LogStreamTest(const std::string& name): Poco::CppUnit::TestCase(name)
{
}


LogStreamTest::~LogStreamTest()
{
}


void LogStreamTest::testLogStream()
{
	AutoPtr<TestChannel> pChannel = new TestChannel;
	Logger& root = Logger::root();
	root.setChannel(pChannel);

	LogStream ls(root);

	ls << "information" << ' ' << 1 << std::endl;
	assertTrue (pChannel->list().begin()->getPriority() == Message::PRIO_INFORMATION);
	assertTrue (pChannel->list().begin()->getText() == "information 1");
	pChannel->list().clear();

	ls.error() << "error" << std::endl;
	assertTrue (pChannel->list().begin()->getPriority() == Message::PRIO_ERROR);
	assertTrue (pChannel->list().begin()->getText() == "error");
	pChannel->list().clear();
}


void LogStreamTest::setUp()
{
}


void LogStreamTest::tearDown()
{
}


Poco::CppUnit::Test* LogStreamTest::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("LogStreamTest");

	CppUnit_addTest(pSuite, LogStreamTest, testLogStream);

	return pSuite;
}
