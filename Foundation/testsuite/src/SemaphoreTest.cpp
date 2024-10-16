//
// SemaphoreTest.cpp
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#include "SemaphoreTest.h"
#include "Poco/CppUnit/TestCaller.h"
#include "Poco/CppUnit/TestSuite.h"
#include "Poco/Thread.h"
#include "Poco/Runnable.h"
#include "Poco/Semaphore.h"
#include "Poco/Exception.h"


using Poco::Thread;
using Poco::Runnable;
using Poco::Semaphore;
using Poco::TimeoutException;


class SemaRunnable: public Runnable
{
public:
	SemaRunnable(int n, int max): _ran(false), _sema(n, max)
	{
	}

	void run()
	{
		_sema.wait();
		_ran = true;
	}

	bool ran() const
	{
		return _ran;
	}

	void set()
	{
		_sema.set();
	}

	void wait()
	{
		_sema.wait();
	}

	void wait(long milliseconds)
	{
		_sema.wait(milliseconds);
	}

	bool tryWait(long milliseconds)
	{
		return _sema.tryWait(milliseconds);
	}

private:
	bool _ran;
	Semaphore _sema;
};


SemaphoreTest::SemaphoreTest(const std::string& name): Poco::CppUnit::TestCase(name)
{
}


SemaphoreTest::~SemaphoreTest()
{
}


void SemaphoreTest::testInitZero()
{
	SemaRunnable r(0, 3);
	assertTrue (!r.tryWait(10));
	r.set();
	r.wait();
	try
	{
		r.wait(100);
		failmsg("must timeout");
	}
	catch (TimeoutException&)
	{
	}
	catch (...)
	{
		failmsg("wrong exception");
	}
	r.set();
	r.set();
	assertTrue (r.tryWait(0));
	r.wait();
	assertTrue (!r.tryWait(10));

	Thread t;
	t.start(r);
	Thread::sleep(100);
	assertTrue (!r.ran());
	r.set();
	t.join();
	assertTrue (r.ran());
	assertTrue (!r.tryWait(10));
}


void SemaphoreTest::testInitNonZero()
{
	SemaRunnable r(2, 2);
	r.wait();
	assertTrue (r.tryWait(10));
	assertTrue (!r.tryWait(10));
	r.set();
	assertTrue (r.tryWait(10));
	assertTrue (!r.tryWait(10));
}


void SemaphoreTest::setUp()
{
}


void SemaphoreTest::tearDown()
{
}


Poco::CppUnit::Test* SemaphoreTest::suite()
{
	Poco::CppUnit::TestSuite* pSuite = new Poco::CppUnit::TestSuite("SemaphoreTest");

	CppUnit_addTest(pSuite, SemaphoreTest, testInitZero);
	CppUnit_addTest(pSuite, SemaphoreTest, testInitNonZero);

	return pSuite;
}
