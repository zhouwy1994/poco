//
// SharedLibraryTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "SharedLibraryTestSuite.h"
#include "ClassLoaderTest.h"
#include "ManifestTest.h"
#include "SharedLibraryTest.h"


Poco::CppUnit::Test* SharedLibraryTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("SharedLibraryTestSuite");

	pSuite->addTest(ManifestTest::suite());

#if !defined(_WIN32) || defined(_DLL)
	pSuite->addTest(SharedLibraryTest::suite());
	pSuite->addTest(ClassLoaderTest::suite());
#endif

	return pSuite;
}
