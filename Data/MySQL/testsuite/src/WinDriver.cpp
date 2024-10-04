//
// WinDriver.cpp
//
// Windows test driver for Poco MySQL.
//
// Copyright (c) 2008, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "WinTestRunner/WinTestRunner.h"
#include "MySQLTestSuite.h"


class TestDriver: public Poco::CppUnit::WinTestRunnerApp
{
	void TestMain()
	{
		Poco::CppUnit::WinTestRunner runner;
		runner.addTest(MySQLTestSuite::suite());
		runner.run();
	}
};


TestDriver theDriver;