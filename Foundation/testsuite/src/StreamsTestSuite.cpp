//
// StreamsTestSuite.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "StreamsTestSuite.h"
#include "Base32Test.h"
#include "Base64Test.h"
#include "HexBinaryTest.h"
#include "StreamCopierTest.h"
#include "CountingStreamTest.h"
#include "NullStreamTest.h"
#include "ZLibTest.h"
#include "StreamTokenizerTest.h"
#include "BinaryReaderWriterTest.h"
#include "LineEndingConverterTest.h"
#include "TeeStreamTest.h"
#include "FileStreamTest.h"
#include "MemoryStreamTest.h"
#include "FIFOBufferStreamTest.h"
#include "DataURIStreamTest.h"


Poco::CppUnit::Test* StreamsTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("StreamsTestSuite");

	pSuite->addTest(Base32Test::suite());
	pSuite->addTest(Base64Test::suite());
	pSuite->addTest(HexBinaryTest::suite());
	pSuite->addTest(StreamCopierTest::suite());
	pSuite->addTest(CountingStreamTest::suite());
	pSuite->addTest(NullStreamTest::suite());
	pSuite->addTest(ZLibTest::suite());
	pSuite->addTest(StreamTokenizerTest::suite());
	pSuite->addTest(BinaryReaderWriterTest::suite());
	pSuite->addTest(LineEndingConverterTest::suite());
	pSuite->addTest(TeeStreamTest::suite());
	pSuite->addTest(FileStreamTest::suite());
	pSuite->addTest(MemoryStreamTest::suite());
	pSuite->addTest(FIFOBufferStreamTest::suite());
	pSuite->addTest(DataURIStreamTest::suite());

	return pSuite;
}
