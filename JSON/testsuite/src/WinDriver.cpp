//
// WinDriver.cpp
//
// Windows test driver for Poco JSON.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "WinTestRunner/WinTestRunner.h"
#include "JSONTestSuite.h"


class TestDriver: public Poco::CppUnit::WinTestRunnerApp
{
	void TestMain()
	{
		Poco::CppUnit::WinTestRunner runner;
		runner.addTest(JSONTestSuite::suite());
		runner.run();
	}
};


TestDriver theDriver;
