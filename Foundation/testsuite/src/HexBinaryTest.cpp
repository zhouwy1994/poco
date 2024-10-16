//
// HexBinaryTest.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "HexBinaryTest.h"
#include "Poco/CppUnit/TestCaller.h"
#include "Poco/CppUnit/TestSuite.h"
#include "Poco/HexBinaryEncoder.h"
#include "Poco/HexBinaryDecoder.h"
#include "Poco/Exception.h"
#include <sstream>


using Poco::HexBinaryEncoder;
using Poco::HexBinaryDecoder;
using Poco::DataFormatException;


HexBinaryTest::HexBinaryTest(const std::string& name): Poco::CppUnit::TestCase(name)
{
}


HexBinaryTest::~HexBinaryTest()
{
}


void HexBinaryTest::testEncoder()
{
	{
		std::ostringstream str;
		HexBinaryEncoder encoder(str);
		encoder << std::string("\00\01\02\03\04\05", 6);
		encoder.close();
		assertTrue (str.str() == "000102030405");
	}
	{
		std::ostringstream str;
		HexBinaryEncoder encoder(str);
		encoder << std::string("\00\01\02\03", 4);
		encoder.close();
		assertTrue (str.str() == "00010203");
	}
	{
		std::ostringstream str;
		HexBinaryEncoder encoder(str);
		encoder << "ABCDEF";
		encoder << char(0xaa) << char(0xbb);
		encoder.close();
		assertTrue (str.str() == "414243444546aabb");
	}
	{
		std::ostringstream str;
		HexBinaryEncoder encoder(str);
		encoder.rdbuf()->setUppercase();
		encoder << "ABCDEF";
		encoder << char(0xaa) << char(0xbb);
		encoder.close();
		assertTrue (str.str() == "414243444546AABB");
	}
}


void HexBinaryTest::testDecoder()
{
	{
		std::istringstream istr("000102030405");
		HexBinaryDecoder decoder(istr);
		assertTrue (decoder.good() && decoder.get() == 0);
		assertTrue (decoder.good() && decoder.get() == 1);
		assertTrue (decoder.good() && decoder.get() == 2);
		assertTrue (decoder.good() && decoder.get() == 3);
		assertTrue (decoder.good() && decoder.get() == 4);
		assertTrue (decoder.good() && decoder.get() == 5);
		assertTrue (decoder.good() && decoder.get() == -1);
	}
	{
		std::istringstream istr("0001020304");
		HexBinaryDecoder decoder(istr);
		assertTrue (decoder.good() && decoder.get() == 0);
		assertTrue (decoder.good() && decoder.get() == 1);
		assertTrue (decoder.good() && decoder.get() == 2);
		assertTrue (decoder.good() && decoder.get() == 3);
		assertTrue (decoder.good() && decoder.get() == 4);
		assertTrue (decoder.good() && decoder.get() == -1);
	}
	{
		std::istringstream istr("0a0bcdef");
		HexBinaryDecoder decoder(istr);
		assertTrue (decoder.good() && decoder.get() == 0x0a);
		assertTrue (decoder.good() && decoder.get() == 0x0b);
		assertTrue (decoder.good() && decoder.get() == 0xcd);
		assertTrue (decoder.good() && decoder.get() == 0xef);
		assertTrue (decoder.good() && decoder.get() == -1);
	}
	{
		std::istringstream istr("0A0BCDEF");
		HexBinaryDecoder decoder(istr);
		assertTrue (decoder.good() && decoder.get() == 0x0a);
		assertTrue (decoder.good() && decoder.get() == 0x0b);
		assertTrue (decoder.good() && decoder.get() == 0xcd);
		assertTrue (decoder.good() && decoder.get() == 0xef);
		assertTrue (decoder.good() && decoder.get() == -1);
	}
	{
		std::istringstream istr("00 01 02 03");
		HexBinaryDecoder decoder(istr);
		assertTrue (decoder.good() && decoder.get() == 0);
		assertTrue (decoder.good() && decoder.get() == 1);
		assertTrue (decoder.good() && decoder.get() == 2);
		assertTrue (decoder.good() && decoder.get() == 3);
		assertTrue (decoder.good() && decoder.get() == -1);
	}
	{
		std::istringstream istr("414243444546");
		HexBinaryDecoder decoder(istr);
		std::string s;
		decoder >> s;
		assertTrue (s == "ABCDEF");
		assertTrue (decoder.eof());
		assertTrue (!decoder.fail());
	}
	{
		std::istringstream istr("4041\r\n4243\r\n4445");
		HexBinaryDecoder decoder(istr);
		std::string s;
		decoder >> s;
		assertTrue (s == "@ABCDE");
		assertTrue (decoder.eof());
		assertTrue (!decoder.fail());
	}
	{
		std::istringstream istr("AABB#CCDD");
		HexBinaryDecoder decoder(istr);
		std::string s;
		try
		{
			decoder >> s;
			assertTrue (decoder.bad());
		}
		catch (DataFormatException&)
		{
		}
		assertTrue (!decoder.eof());
	}
}


void HexBinaryTest::testEncodeDecode()
{
	{
		std::stringstream str;
		HexBinaryEncoder encoder(str);
		encoder << "The quick brown fox ";
		encoder << "jumped over the lazy dog.";
		encoder.close();
		HexBinaryDecoder decoder(str);
		std::string s;
		int c = decoder.get();
		while (c != -1) { s += char(c); c = decoder.get(); }
		assertTrue (s == "The quick brown fox jumped over the lazy dog.");
	}
	{
		std::string src;
		for (int i = 0; i < 255; ++i) src += char(i);
		std::stringstream str;
		HexBinaryEncoder encoder(str);
		encoder.write(src.data(), (std::streamsize) src.size());
		encoder.close();
		HexBinaryDecoder decoder(str);
		std::string s;
		int c = decoder.get();
		while (c != -1) { s += char(c); c = decoder.get(); }
		assertTrue (s == src);
	}
}


void HexBinaryTest::setUp()
{
}


void HexBinaryTest::tearDown()
{
}


Poco::CppUnit::Test* HexBinaryTest::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("HexBinaryTest");

	CppUnit_addTest(pSuite, HexBinaryTest, testEncoder);
	CppUnit_addTest(pSuite, HexBinaryTest, testDecoder);
	CppUnit_addTest(pSuite, HexBinaryTest, testEncodeDecode);

	return pSuite;
}
