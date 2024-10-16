//
// HTTPSStreamFactoryTest.cpp
//
// Copyright (c) 2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "HTTPSStreamFactoryTest.h"
#include "Poco/CppUnit/TestCaller.h"
#include "Poco/CppUnit/TestSuite.h"
#include "Poco/Net/HTTPSStreamFactory.h"
#include "Poco/Net/NetException.h"
#include "Poco/Util/Application.h"
#include "Poco/Util/AbstractConfiguration.h"
#include "Poco/URI.h"
#include "Poco/Exception.h"
#include "Poco/StreamCopier.h"
#include "HTTPSTestServer.h"
#include <sstream>
#include <memory>


using Poco::Net::HTTPSStreamFactory;
using Poco::Net::NetException;
using Poco::Net::HTTPException;
using Poco::Util::Application;
using Poco::URI;
using Poco::StreamCopier;


HTTPSStreamFactoryTest::HTTPSStreamFactoryTest(const std::string& name): Poco::CppUnit::TestCase(name)
{
}


HTTPSStreamFactoryTest::~HTTPSStreamFactoryTest()
{
}


void HTTPSStreamFactoryTest::testNoRedirect()
{
	HTTPSTestServer server;
	HTTPSStreamFactory factory;
	URI uri("https://127.0.0.1/large");
	uri.setPort(server.port());
	std::unique_ptr<std::istream> pStr(factory.open(uri));
	std::ostringstream ostr;
	StreamCopier::copyStream(*pStr.get(), ostr);
	assertTrue (ostr.str() == HTTPSTestServer::LARGE_BODY);
}


void HTTPSStreamFactoryTest::testEmptyPath()
{
	HTTPSTestServer server;
	HTTPSStreamFactory factory;
	URI uri("https://127.0.0.1");
	uri.setPort(server.port());
	std::unique_ptr<std::istream> pStr(factory.open(uri));
	std::ostringstream ostr;
	StreamCopier::copyStream(*pStr.get(), ostr);
	assertTrue (ostr.str() == HTTPSTestServer::SMALL_BODY);
}


void HTTPSStreamFactoryTest::testRedirect()
{
	HTTPSTestServer server;
	HTTPSStreamFactory factory;
	URI uri("https://127.0.0.1/redirect");
	uri.setPort(server.port());
	std::unique_ptr<std::istream> pStr(factory.open(uri));
	std::ostringstream ostr;
	StreamCopier::copyStream(*pStr.get(), ostr);
	assertTrue (ostr.str() == HTTPSTestServer::LARGE_BODY);
}


void HTTPSStreamFactoryTest::testProxy()
{
	HTTPSTestServer server;
	HTTPSStreamFactory factory(
		Application::instance().config().getString("testsuite.proxy.host"),
		Application::instance().config().getInt("testsuite.proxy.port")
	);
	URI uri("https://secure.appinf.com/public/poco/NetSSL.txt");
	std::unique_ptr<std::istream> pStr(factory.open(uri));
	std::ostringstream ostr;
	StreamCopier::copyStream(*pStr.get(), ostr);
	assertTrue (ostr.str().length() > 0);
}


void HTTPSStreamFactoryTest::testError()
{
	HTTPSTestServer server;
	HTTPSStreamFactory factory;
	URI uri("https://127.0.0.1/notfound");
	uri.setPort(server.port());
	try
	{
		std::istream* pStr = factory.open(uri);
		fail("not found - must throw");
	}
	catch (HTTPException& exc)
	{
		std::string m = exc.displayText();
	}
}


void HTTPSStreamFactoryTest::setUp()
{
}


void HTTPSStreamFactoryTest::tearDown()
{
}


Poco::CppUnit::Test* HTTPSStreamFactoryTest::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("HTTPSStreamFactoryTest");

	CppUnit_addTest(pSuite, HTTPSStreamFactoryTest, testNoRedirect);
	CppUnit_addTest(pSuite, HTTPSStreamFactoryTest, testEmptyPath);
	CppUnit_addTest(pSuite, HTTPSStreamFactoryTest, testRedirect);
	CppUnit_addTest(pSuite, HTTPSStreamFactoryTest, testProxy);
	CppUnit_addTest(pSuite, HTTPSStreamFactoryTest, testError);

	return pSuite;
}
