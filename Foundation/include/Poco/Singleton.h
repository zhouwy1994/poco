//
// Singleton.h
//
// Library: Foundation
// Package: Core
// Module:  Singleton
//
// Definition of the Singleton template.
//
// Copyright (c) 2004-2006, Applied Informatics Software Engineering GmbH.
// and Contributors.
//
// SPDX-License-Identifier:	BSL-1.0
//


#ifndef Foundation_Singleton_INCLUDED
#define Foundation_Singleton_INCLUDED

namespace Poco {

template <class S>
class Singleton
	/// Declare constructor as private to prevent 
	/// object declaration through constructor
{
protected:
	Singleton()
	{
	}

	~Singleton()
	{
	}

public:
	static S* get()
		/// Return the singleton pointer object of S
	{
		static S instance;
		return &instance;
	}
};

/// Declare a singleton class through this macro
/// definition, for example:
/// class MySingleton : public POCO_SINGLETON(MySingleton)
/// ... Declare function
/// }
#define POCO_SINGLETON(T) \
Poco::Singleton<T> { \
	friend class Poco::Singleton<T>; \
private: \
	T() = default; \

} // namespace Poco


#endif // Foundation_Singleton_INCLUDED
