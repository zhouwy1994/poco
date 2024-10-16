//
// ManifestTest.h
//
// Definition of the ManifestTest class.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef ManifestTest_INCLUDED
#define ManifestTest_INCLUDED


#include "Poco/Foundation.h"
#include "Poco/CppUnit/TestCase.h"


class ManifestTest: public Poco::CppUnit::TestCase
{
public:
	ManifestTest(const std::string& name);
	~ManifestTest();

	void testManifest();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

private:
};


#endif // ManifestTest_INCLUDED
