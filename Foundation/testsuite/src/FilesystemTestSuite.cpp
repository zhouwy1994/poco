//
// FilesystemTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "FilesystemTestSuite.h"
#include "PathTest.h"
#include "FileTest.h"
#include "GlobTest.h"
#include "DirectoryWatcherTest.h"
#include "DirectoryIteratorsTest.h"


Poco::CppUnit::Test* FilesystemTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("FilesystemTestSuite");

	pSuite->addTest(PathTest::suite());
	pSuite->addTest(FileTest::suite());
	pSuite->addTest(GlobTest::suite());
#ifndef POCO_NO_INOTIFY
	pSuite->addTest(DirectoryWatcherTest::suite());
#endif // POCO_NO_INOTIFY
	pSuite->addTest(DirectoryIteratorsTest::suite());

	return pSuite;
}
