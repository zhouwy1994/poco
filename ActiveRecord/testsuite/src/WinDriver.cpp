//
// WinDriver.cpp
//
// Windows test driver for Poco ActiveRecord.
//
// Copyright (c) 2020, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier: Apache-2.0
//


#include "WinTestRunner/WinTestRunner.h"
#include "ActiveRecordTestSuite.h"


class TestDriver: public Poco::CppUnit::WinTestRunnerApp
{
	void TestMain()
	{
		Poco::CppUnit::WinTestRunner runner;
		runner.addTest(ActiveRecordTestSuite::suite());
		runner.run();
	}
};


TestDriver theDriver;
