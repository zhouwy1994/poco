//
// CryptTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "CryptTestSuite.h"
#include "MD4EngineTest.h"
#include "MD5EngineTest.h"
#include "SHA1EngineTest.h"
#include "SHA2EngineTest.h"
#include "HMACEngineTest.h"
#include "PBKDF2EngineTest.h"
#include "DigestStreamTest.h"
#include "RandomTest.h"
#include "RandomStreamTest.h"


Poco::CppUnit::Test* CryptTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("CryptTestSuite");

	pSuite->addTest(MD4EngineTest::suite());
	pSuite->addTest(MD5EngineTest::suite());
	pSuite->addTest(SHA1EngineTest::suite());
	pSuite->addTest(SHA2EngineTest::suite());
	pSuite->addTest(HMACEngineTest::suite());
	pSuite->addTest(PBKDF2EngineTest::suite());
	pSuite->addTest(DigestStreamTest::suite());
	pSuite->addTest(RandomTest::suite());
	pSuite->addTest(RandomStreamTest::suite());

	return pSuite;
}
