//
// WinDriver.cpp
//
// Windows test driver for Poco Encodings.
//
// Copyright (c) 2018, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier: Apache-2.0
//


#include "WinTestRunner/WinTestRunner.h"
#include "EncodingsTestSuite.h"


class TestDriver: public Poco::CppUnit::WinTestRunnerApp
{
	void TestMain()
	{
		Poco::CppUnit::WinTestRunner runner;
		runner.addTest(EncodingsTestSuite::suite());
		runner.run();
	}
};


TestDriver theDriver;
