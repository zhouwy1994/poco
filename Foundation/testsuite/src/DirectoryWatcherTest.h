//
// DirectoryWatcherTest.h
//
// Definition of the DirectoryWatcherTest class.
//
// Copyright (c) 2012, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef DirectoryWatcherTest_INCLUDED
#define DirectoryWatcherTest_INCLUDED


#include "Poco/Foundation.h"


#ifndef POCO_NO_INOTIFY


#include "Poco/DirectoryWatcher.h"
#include "Poco/Path.h"
#include "Poco/Mutex.h"
#include "Poco/CppUnit/TestCase.h"


class DirectoryWatcherTest: public Poco::CppUnit::TestCase
{
public:
	DirectoryWatcherTest(const std::string& name);
	~DirectoryWatcherTest();

	void testAdded();
	void testRemoved();
	void testModified();
	void testMoved();
	void testSuspend();
	void testResume();
	void testSuspendMultipleTimes();

	void setUp();
	void tearDown();

	static Poco::CppUnit::Test* suite();

protected:
	void onItemAdded(const Poco::DirectoryWatcher::DirectoryEvent& ev);
	void onItemRemoved(const Poco::DirectoryWatcher::DirectoryEvent& ev);
	void onItemModified(const Poco::DirectoryWatcher::DirectoryEvent& ev);
	void onItemMovedFrom(const Poco::DirectoryWatcher::DirectoryEvent& ev);
	void onItemMovedTo(const Poco::DirectoryWatcher::DirectoryEvent& ev);
	void onError(const Poco::Exception& exc);

	Poco::Path path() const;

private:
	struct DirEvent
	{
		Poco::DirectoryWatcher::DirectoryEventType type;
		std::string callback;
		std::string path;
	};
	std::vector<DirEvent> _events;
	bool _error;
	Poco::Mutex _mutex;
};


#endif // POCO_NO_INOTIFY


#endif // DirectoryWatcherTest_INCLUDED


