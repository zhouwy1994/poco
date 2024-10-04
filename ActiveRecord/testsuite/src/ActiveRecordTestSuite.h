//
// ActiveRecordTestSuite.h
//
// Definition of the ActiveRecordTestSuite class.
//
// Copyright (c) 2020, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef ActiveRecordTestSuite_INCLUDED
#define ActiveRecordTestSuite_INCLUDED


#include "Poco/CppUnit/TestSuite.h"


class ActiveRecordTestSuite
{
public:
	static Poco::CppUnit::Test* suite();
};


#endif // ActiveRecordTestSuite_INCLUDED
