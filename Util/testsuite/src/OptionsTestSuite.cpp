//
// OptionsTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "OptionsTestSuite.h"
#include "OptionTest.h"
#include "OptionSetTest.h"
#include "HelpFormatterTest.h"
#include "OptionProcessorTest.h"
#include "ValidatorTest.h"


Poco::CppUnit::Test* OptionsTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("OptionsTestSuite");

	pSuite->addTest(OptionTest::suite());
	pSuite->addTest(OptionSetTest::suite());
	pSuite->addTest(HelpFormatterTest::suite());
	pSuite->addTest(OptionProcessorTest::suite());
	pSuite->addTest(ValidatorTest::suite());

	return pSuite;
}
