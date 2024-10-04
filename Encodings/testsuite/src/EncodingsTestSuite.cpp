//
// EncodingsTestSuite.cpp
//
// Copyright (c) 2018, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier: Apache-2.0
//


#include "EncodingsTestSuite.h"
#include "DoubleByteEncodingTest.h"


Poco::CppUnit::Test* EncodingsTestSuite::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("EncodingsTestSuite");

	pSuite->addTest(DoubleByteEncodingTest::suite());

	return pSuite;
}
