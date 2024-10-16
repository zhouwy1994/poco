//
// UUIDTest.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "UUIDTest.h"
#include "Poco/CppUnit/TestCaller.h"
#include "Poco/CppUnit/TestSuite.h"
#include "Poco/UUID.h"
#include "Poco/Exception.h"


using Poco::UUID;


UUIDTest::UUIDTest(const std::string& name): Poco::CppUnit::TestCase(name)
{
}


UUIDTest::~UUIDTest()
{
}


void UUIDTest::testParse()
{
	UUID uuid("6ba7b810-9dad-11d1-80b4-00c04fd430c8");
	assertTrue (uuid.toString() == "6ba7b810-9dad-11d1-80b4-00c04fd430c8");

	uuid.parse("6BA7B810-9DAD-11D1-80B4-00C04FD430C8");
	assertTrue (uuid.toString() == "6ba7b810-9dad-11d1-80b4-00c04fd430c8");

	uuid.parse("6BA7B8109DAD11D180B400C04FD430C8");
	assertTrue (uuid.toString() == "6ba7b810-9dad-11d1-80b4-00c04fd430c8");

	try
	{
		uuid.parse("6xA7B8109DAD11D180B400C04FD430C8");
		fail("invalid UUID - must throw");
	}
	catch (Poco::SyntaxException&)
	{
	}

	try
	{
		uuid.parse("6xa7b810-9dad-11d1-80b4-00c04fd430c8");
		fail("invalid UUID - must throw");
	}
	catch (Poco::SyntaxException&)
	{
	}

	try
	{
		uuid.parse("6ba7b810-xdad-11d1-80b4-00c04fd430c8");
		fail("invalid UUID - must throw");
	}
	catch (Poco::SyntaxException&)
	{
	}

	try
	{
		uuid.parse("6ba7b810-9dad-x1d1-80b4-00c04fd430c8");
		fail("invalid UUID - must throw");
	}
	catch (Poco::SyntaxException&)
	{
	}

	try
	{
		uuid.parse("6ba7b810-9dad-11d1-x0b4-00c04fd430c8");
		fail("invalid UUID - must throw");
	}
	catch (Poco::SyntaxException&)
	{
	}

	try
	{
		uuid.parse("6ba7b810-9dad-11d1-80b4-00x04fd430c8");
		fail("invalid UUID - must throw");
	}
	catch (Poco::SyntaxException&)
	{
	}
}


void UUIDTest::testBuffer()
{
	UUID uuid("6ba7b810-9dad-11d1-80b4-00c04fd430c8");
	char buffer[16];
	uuid.copyTo(buffer);
	UUID uuid2;
	uuid2.copyFrom(buffer);
	assertTrue (uuid2.toString() == "6ba7b810-9dad-11d1-80b4-00c04fd430c8");
}


void UUIDTest::testCompare()
{
	UUID null;
	assertTrue (null.isNull());
	assertTrue (UUID::null().isNull());

	UUID uuid1 = null;
	UUID uuid2;
	assertTrue (uuid1.isNull());
	assertTrue (uuid1 == null);
	assertTrue (!(uuid1 != null));
	assertTrue (uuid1 >= null);
	assertTrue (uuid1 <= null);
	assertTrue (!(uuid1 > null));
	assertTrue (!(uuid1 < null));
	assertTrue (uuid1.toString() == "00000000-0000-0000-0000-000000000000");

	uuid1 = UUID::dns();
	assertTrue (!uuid1.isNull());
	assertTrue (uuid1 != null);
	assertTrue (!(uuid1 == null));
	assertTrue (uuid1 >= null);
	assertTrue (!(uuid1 <= null));
	assertTrue (uuid1 > null);
	assertTrue (!(uuid1 < null));
	assertTrue (uuid1.toString() == "6ba7b810-9dad-11d1-80b4-00c04fd430c8");

	assertTrue (null != uuid1);
	assertTrue (!(null == uuid1));
	assertTrue (!(null >= uuid1));
	assertTrue (null <= uuid1);
	assertTrue (!(null > uuid1));
	assertTrue (null < uuid1);

	uuid2 = uuid1;
	assertTrue (uuid2 == uuid1);
	assertTrue (!(uuid2 != uuid1));
	assertTrue (uuid2 >= uuid1);
	assertTrue (uuid2 <= uuid1);
	assertTrue (!(uuid2 > uuid1));
	assertTrue (!(uuid2 < uuid1));
}


void UUIDTest::testVersion()
{
	UUID uuid("db4fa7e9-9e62-4597-99e0-b1ec0b59800e");
	UUID::Version v = uuid.version();
	assertTrue (v == UUID::UUID_RANDOM);

	uuid.parse("6ba7b810-9dad-11d1-80b4-00c04fd430c8");
	v = uuid.version();
	assertTrue (v == UUID::UUID_TIME_BASED);

	uuid.parse("d2ee4220-3625-11d9-9669-0800200c9a66");
	v = uuid.version();
	assertTrue (v == UUID::UUID_TIME_BASED);

	uuid.parse("360d3652-4411-4786-bbe6-b9675b548559");
	v = uuid.version();
	assertTrue (v == UUID::UUID_RANDOM);
}


void UUIDTest::testVariant()
{
	UUID uuid("db4fa7e9-9e62-4597-99e0-b1ec0b59800e");
	int v = uuid.variant();
	assertTrue (v == 2);

	uuid.parse("6ba7b810-9dad-11d1-80b4-00c04fd430c8");
	v = uuid.variant();
	assertTrue (v == 2);

	uuid.parse("d2ee4220-3625-11d9-9669-0800200c9a66");
	v = uuid.variant();
	assertTrue (v == 2);

	uuid.parse("360d3652-4411-4786-bbe6-b9675b548559");
	v = uuid.variant();
	assertTrue (v == 2);
}


void UUIDTest::testSwap()
{
	UUID uuid1("db4fa7e9-9e62-4597-99e0-b1ec0b59800e");
	UUID uuid2("d2ee4220-3625-11d9-9669-0800200c9a66");
	uuid1.swap(uuid2);
	assertTrue (uuid1.toString() == "d2ee4220-3625-11d9-9669-0800200c9a66");
	assertTrue (uuid2.toString() == "db4fa7e9-9e62-4597-99e0-b1ec0b59800e");
}

void UUIDTest::testTryParse()
{
	UUID uuid;
	assertTrue (uuid.tryParse("6BA7B810-9DAD-11D1-80B4-00C04FD430C8"));
	assertTrue (uuid.toString() == "6ba7b810-9dad-11d1-80b4-00c04fd430c8");

	UUID notUuid;
	assertTrue (!notUuid.tryParse("not a uuid"));
	assertTrue (notUuid.isNull());
}

void UUIDTest::setUp()
{
}


void UUIDTest::tearDown()
{
}


Poco::CppUnit::Test* UUIDTest::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("UUIDTest");

	CppUnit_addTest(pSuite, UUIDTest, testParse);
	CppUnit_addTest(pSuite, UUIDTest, testBuffer);
	CppUnit_addTest(pSuite, UUIDTest, testCompare);
	CppUnit_addTest(pSuite, UUIDTest, testVersion);
	CppUnit_addTest(pSuite, UUIDTest, testVariant);
	CppUnit_addTest(pSuite, UUIDTest, testSwap);
	CppUnit_addTest(pSuite, UUIDTest, testTryParse);

	return pSuite;
}
