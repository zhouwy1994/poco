//
// MD5EngineTest.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "MD5EngineTest.h"
#include "Poco/CppUnit/TestCaller.h"
#include "Poco/CppUnit/TestSuite.h"
#include "Poco/MD5Engine.h"


using Poco::MD5Engine;
using Poco::DigestEngine;


MD5EngineTest::MD5EngineTest(const std::string& name): Poco::CppUnit::TestCase(name)
{
}


MD5EngineTest::~MD5EngineTest()
{
}


void MD5EngineTest::testMD5()
{
	MD5Engine engine;

	// test vectors from RFC 1321

	engine.update("");
	assertTrue (DigestEngine::digestToHex(engine.digest()) == "d41d8cd98f00b204e9800998ecf8427e");

	engine.update("a");
	assertTrue (DigestEngine::digestToHex(engine.digest()) == "0cc175b9c0f1b6a831c399e269772661");

	engine.update("abc");
	assertTrue (DigestEngine::digestToHex(engine.digest()) == "900150983cd24fb0d6963f7d28e17f72");

	engine.update("message digest");
	assertTrue (DigestEngine::digestToHex(engine.digest()) == "f96b697d7cb7938d525a2f31aaf161d0");

	engine.update("abcdefghijklmnopqrstuvwxyz");
	assertTrue (DigestEngine::digestToHex(engine.digest()) == "c3fcd3d76192e4007dfb496cca67e13b");

	engine.update("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
	engine.update("abcdefghijklmnopqrstuvwxyz0123456789");
	assertTrue (DigestEngine::digestToHex(engine.digest()) == "d174ab98d277d9f5a5611c2c9f419d9f");

	engine.update("12345678901234567890123456789012345678901234567890123456789012345678901234567890");
	assertTrue (DigestEngine::digestToHex(engine.digest()) == "57edf4a22be3c955ac49da2e2107b67a");
}


void MD5EngineTest::testConstantTimeEquals()
{
	DigestEngine::Digest d1 = DigestEngine::digestFromHex("d41d8cd98f00b204e9800998ecf8427e");
	DigestEngine::Digest d2 = DigestEngine::digestFromHex("d41d8cd98f00b204e9800998ecf8427e");
	DigestEngine::Digest d3 = DigestEngine::digestFromHex("0cc175b9c0f1b6a831c399e269772661");

	assertTrue (DigestEngine::constantTimeEquals(d1, d2));
	assertTrue (!DigestEngine::constantTimeEquals(d1, d3));
}


void MD5EngineTest::setUp()
{
}


void MD5EngineTest::tearDown()
{
}


Poco::CppUnit::Test* MD5EngineTest::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("MD5EngineTest");

	CppUnit_addTest(pSuite, MD5EngineTest, testMD5);
	CppUnit_addTest(pSuite, MD5EngineTest, testConstantTimeEquals);

	return pSuite;
}
