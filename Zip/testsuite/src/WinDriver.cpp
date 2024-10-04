//
// WinDriver.cpp
//
// Windows test driver for Poco Zip.
//
// Copyright (c) 2007, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "WinTestRunner/WinTestRunner.h"
#include "ZipTestSuite.h"


class TestDriver: public Poco::CppUnit::WinTestRunnerApp
{
	void TestMain()
	{
		Poco::CppUnit::WinTestRunner runner;
		runner.addTest(ZipTestSuite::suite());
		runner.run();
	}
};


TestDriver theDriver;
