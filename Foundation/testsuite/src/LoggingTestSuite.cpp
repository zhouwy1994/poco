//
// LoggingTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "LoggingTestSuite.h"
#include "LoggerTest.h"
#include "ChannelTest.h"
#include "PatternFormatterTest.h"
#include "FileChannelTest.h"
#include "SimpleFileChannelTest.h"
#include "LoggingFactoryTest.h"
#include "LoggingRegistryTest.h"
#include "LogStreamTest.h"


Poco::CppUnit::Test* LoggingTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("LoggingTestSuite");

	pSuite->addTest(LoggerTest::suite());
	pSuite->addTest(ChannelTest::suite());
	pSuite->addTest(PatternFormatterTest::suite());
	pSuite->addTest(FileChannelTest::suite());
	pSuite->addTest(SimpleFileChannelTest::suite());
	pSuite->addTest(LoggingFactoryTest::suite());
	pSuite->addTest(LoggingRegistryTest::suite());
	pSuite->addTest(LogStreamTest::suite());

	return pSuite;
}
