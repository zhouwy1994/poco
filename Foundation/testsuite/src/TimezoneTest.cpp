//
// TimezoneTest.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "TimezoneTest.h"
#include "Poco/CppUnit/TestCaller.h"
#include "Poco/CppUnit/TestSuite.h"
#include "Poco/Timezone.h"
#include <iostream>


using Poco::Timezone;


TimezoneTest::TimezoneTest(const std::string& name): Poco::CppUnit::TestCase(name)
{
}


TimezoneTest::~TimezoneTest()
{
}


void TimezoneTest::testTimezone()
{
	std::string name = Timezone::name();
	std::string stdName = Timezone::standardName();
	std::string dstName = Timezone::dstName();
	std::cout << "Timezone Names: " << name << ", " << stdName << ", " << dstName << std::endl;
	int utcOffset = Timezone::utcOffset();
	std::cout << "UTC Offset: " << utcOffset << std::endl;
	int dst = Timezone::dst();
	std::cout << "DST Offset: " << dst << std::endl;
}


void TimezoneTest::setUp()
{
}


void TimezoneTest::tearDown()
{
}


Poco::CppUnit::Test* TimezoneTest::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("TimezoneTest");

	CppUnit_addTest(pSuite, TimezoneTest, testTimezone);

	return pSuite;
}
